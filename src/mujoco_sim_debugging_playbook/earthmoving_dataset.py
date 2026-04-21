from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from mujoco_sim_debugging_playbook.earthmoving import EarthmovingSimulation, load_earthmoving_config, scenario_from_dict
from mujoco_sim_debugging_playbook.earthmoving_benchmark import randomized_soil_variants
from mujoco_sim_debugging_playbook.provenance import write_manifest


FEATURE_NAMES = [
    "cohesion",
    "friction_angle_deg",
    "compaction_rate",
    "blade_coupling",
    "spillover_rate",
    "blade_width",
    "blade_depth",
    "blade_distance",
    "pile_radius",
    "pile_height",
]

LABEL_NAMES = [
    "moved_volume",
    "terrain_profile_rmse",
    "volume_conservation_error",
    "runtime_s",
]


def generate_earthmoving_dataset(
    *,
    config_path: str | Path,
    output_dir: str | Path,
    episodes_per_scenario: int,
    seed: int,
    variation: float,
) -> dict[str, Any]:
    config = load_earthmoving_config(config_path)
    rows = []
    features = []
    labels = []
    for scenario_index, scenario_payload in enumerate(config["scenarios"]):
        base = scenario_from_dict(scenario_payload)
        variants = randomized_soil_variants(
            base,
            seed=seed + scenario_index * 3571,
            episodes=episodes_per_scenario,
            variation=variation,
        )
        for variant in variants:
            result = EarthmovingSimulation(variant).run()
            feature_row = _feature_row(variant)
            label_row = _label_row(result.metrics)
            features.append(feature_row)
            labels.append(label_row)
            rows.append(
                {
                    "scenario": variant.name,
                    "base_scenario": base.name,
                    "features": dict(zip(FEATURE_NAMES, feature_row)),
                    "labels": dict(zip(LABEL_NAMES, label_row)),
                }
            )

    feature_array = np.asarray(features, dtype=np.float64)
    label_array = np.asarray(labels, dtype=np.float64)
    normalization = _normalization(feature_array, label_array)
    summary = {
        "row_count": len(rows),
        "feature_names": FEATURE_NAMES,
        "label_names": LABEL_NAMES,
        "feature_mean": normalization["feature_mean"].tolist(),
        "feature_std": normalization["feature_std"].tolist(),
        "label_mean": normalization["label_mean"].tolist(),
        "label_std": normalization["label_std"].tolist(),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    dataset_path = output / "earthmoving_dataset.npz"
    summary_path = output / "dataset_summary.json"
    report_path = output / "report.md"
    np.savez_compressed(
        dataset_path,
        features=feature_array,
        labels=label_array,
        feature_names=np.asarray(FEATURE_NAMES),
        label_names=np.asarray(LABEL_NAMES),
    )
    summary_path.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2))
    _write_report(summary, rows, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_dataset",
        config={
            "config_path": str(config_path),
            "episodes_per_scenario": episodes_per_scenario,
            "seed": seed,
            "variation": variation,
        },
        inputs=[config_path],
        outputs=[dataset_path, summary_path, report_path],
        metadata={"row_count": len(rows), "feature_count": len(FEATURE_NAMES), "label_count": len(LABEL_NAMES)},
    )
    return {"summary": summary, "rows": rows, "output_dir": str(output)}


def _feature_row(scenario: Any) -> list[float]:
    blade = scenario.blade
    soil = scenario.soil
    terrain = scenario.terrain
    return [
        soil.cohesion,
        soil.friction_angle_deg,
        soil.compaction_rate,
        soil.blade_coupling,
        soil.spillover_rate,
        blade.width,
        blade.depth,
        abs(blade.end_x - blade.start_x),
        terrain.pile_radius,
        terrain.pile_height,
    ]


def _label_row(metrics: Any) -> list[float]:
    return [
        metrics.moved_volume,
        metrics.terrain_profile_rmse,
        metrics.volume_conservation_error,
        metrics.runtime_s,
    ]


def _normalization(features: np.ndarray, labels: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "feature_mean": features.mean(axis=0),
        "feature_std": np.maximum(features.std(axis=0), 1e-9),
        "label_mean": labels.mean(axis=0),
        "label_std": np.maximum(labels.std(axis=0), 1e-9),
    }


def _write_report(summary: dict[str, Any], rows: list[dict[str, Any]], output_path: Path) -> None:
    lines = [
        "# Earthmoving ML Dataset",
        "",
        f"Rows: `{summary['row_count']}`",
        f"Features: `{len(summary['feature_names'])}`",
        f"Labels: `{len(summary['label_names'])}`",
        "",
        "## Feature Schema",
        "",
    ]
    for name in summary["feature_names"]:
        lines.append(f"- `{name}`")
    lines.extend(["", "## Label Schema", ""])
    for name in summary["label_names"]:
        lines.append(f"- `{name}`")
    lines.extend(["", "## Sample Rows", "", "| scenario | moved_volume | terrain_rmse | volume_error |", "| --- | ---: | ---: | ---: |"])
    for row in rows[:8]:
        labels = row["labels"]
        lines.append(
            f"| {row['scenario']} | {labels['moved_volume']:.6f} | "
            f"{labels['terrain_profile_rmse']:.6f} | {labels['volume_conservation_error']:.6f} |"
        )
    output_path.write_text("\n".join(lines))
