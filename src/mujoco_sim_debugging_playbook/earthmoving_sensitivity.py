from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any

import numpy as np

from mujoco_sim_debugging_playbook.earthmoving import EarthmovingSimulation, load_earthmoving_config, scenario_from_dict
from mujoco_sim_debugging_playbook.earthmoving_benchmark import randomized_soil_variants
from mujoco_sim_debugging_playbook.provenance import write_manifest


SOIL_KEYS = ["cohesion", "friction_angle_deg", "compaction_rate", "blade_coupling", "spillover_rate"]
METRIC_KEYS = ["moved_volume", "terrain_profile_rmse", "volume_conservation_error", "runtime_s"]


def run_earthmoving_sensitivity(
    config_path: str | Path,
    output_dir: str | Path,
    episodes_per_scenario: int,
    seed: int,
    variation: float,
) -> dict[str, Any]:
    config = load_earthmoving_config(config_path)
    rows = []
    for scenario_index, scenario_payload in enumerate(config["scenarios"]):
        base = scenario_from_dict(scenario_payload)
        variants = randomized_soil_variants(
            base,
            seed=seed + scenario_index * 7919,
            episodes=episodes_per_scenario,
            variation=variation,
        )
        for variant in variants:
            result = EarthmovingSimulation(variant).run()
            rows.append(
                {
                    "scenario": variant.name,
                    "base_scenario": base.name,
                    **{key: getattr(variant.soil, key) for key in SOIL_KEYS},
                    **{key: getattr(result.metrics, key) for key in METRIC_KEYS},
                }
            )

    sensitivities = _correlations(rows)
    summary = _summarize(rows, sensitivities)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    summary_path = output / "sensitivity_summary.json"
    report_path = output / "report.md"
    summary_path.write_text(json.dumps({"summary": summary, "sensitivities": sensitivities, "rows": rows}, indent=2))
    _write_report(summary, sensitivities, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_sensitivity",
        config={
            "config_path": str(config_path),
            "episodes_per_scenario": episodes_per_scenario,
            "seed": seed,
            "variation": variation,
        },
        inputs=[config_path],
        outputs=[summary_path, report_path],
        metadata=summary,
    )
    return {"summary": summary, "sensitivities": sensitivities, "rows": rows, "output_dir": str(output)}


def _correlations(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    values = {key: np.asarray([float(row[key]) for row in rows]) for key in [*SOIL_KEYS, *METRIC_KEYS]}
    results = []
    for soil_key in SOIL_KEYS:
        for metric_key in METRIC_KEYS:
            corr = _safe_corrcoef(values[soil_key], values[metric_key])
            results.append(
                {
                    "soil_parameter": soil_key,
                    "metric": metric_key,
                    "pearson_correlation": corr,
                    "abs_correlation": abs(corr),
                }
            )
    return sorted(results, key=lambda item: item["abs_correlation"], reverse=True)


def _safe_corrcoef(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 2 or np.std(left) <= 1e-12 or np.std(right) <= 1e-12:
        return 0.0
    return float(np.corrcoef(left, right)[0, 1])


def _summarize(rows: list[dict[str, Any]], sensitivities: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "episode_count": len(rows),
        "mean_moved_volume": mean(row["moved_volume"] for row in rows) if rows else 0.0,
        "mean_terrain_profile_rmse": mean(row["terrain_profile_rmse"] for row in rows) if rows else 0.0,
        "top_sensitivity": sensitivities[0] if sensitivities else None,
    }


def _write_report(summary: dict[str, Any], sensitivities: list[dict[str, Any]], output_path: Path) -> None:
    lines = [
        "# Earthmoving Sensitivity",
        "",
        f"Episodes: `{summary['episode_count']}`",
        f"Mean moved volume: `{summary['mean_moved_volume']:.6f}`",
        f"Mean terrain RMSE: `{summary['mean_terrain_profile_rmse']:.6f}`",
        "",
        "| soil_parameter | metric | correlation |",
        "| --- | --- | ---: |",
    ]
    for row in sensitivities[:10]:
        lines.append(
            f"| {row['soil_parameter']} | {row['metric']} | {row['pearson_correlation']:.4f} |"
        )
    output_path.write_text("\n".join(lines))
