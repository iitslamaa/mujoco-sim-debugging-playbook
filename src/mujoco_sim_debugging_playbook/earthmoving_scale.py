from __future__ import annotations

import json
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from statistics import mean
from typing import Any

from mujoco_sim_debugging_playbook.earthmoving import EarthmovingSimulation, load_earthmoving_config, scenario_from_dict
from mujoco_sim_debugging_playbook.earthmoving_benchmark import randomized_soil_variants
from mujoco_sim_debugging_playbook.provenance import write_manifest


def run_earthmoving_scale_study(
    config_path: str | Path,
    output_dir: str | Path,
    episodes_per_scenario: int,
    seed: int,
    workers: int = 1,
    variation: float = 0.25,
) -> dict[str, Any]:
    benchmark = load_earthmoving_config(config_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    scenarios = []
    for scenario_index, scenario_payload in enumerate(benchmark["scenarios"]):
        base = scenario_from_dict(scenario_payload)
        scenarios.extend(
            randomized_soil_variants(
                base,
                seed=seed + scenario_index * 1009,
                episodes=episodes_per_scenario,
                variation=variation,
            )
        )

    start = time.perf_counter()
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            rows = list(executor.map(_run_scale_episode, scenarios))
    else:
        rows = [_run_scale_episode(scenario) for scenario in scenarios]
    wall_time_s = max(time.perf_counter() - start, 1e-9)
    summary = _summarize(rows, wall_time_s, workers)

    summary_path = output / "scale_summary.json"
    report_path = output / "report.md"
    summary_path.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2))
    _write_report(summary, rows, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_scale",
        config={
            "config_path": str(config_path),
            "episodes_per_scenario": episodes_per_scenario,
            "seed": seed,
            "workers": workers,
            "variation": variation,
        },
        inputs=[config_path],
        outputs=[summary_path, report_path],
        metadata=summary,
    )
    return {"summary": summary, "rows": rows, "output_dir": str(output)}


def _run_scale_episode(scenario: Any) -> dict[str, Any]:
    result = EarthmovingSimulation(scenario).run()
    metrics = result.metrics
    base_name = scenario.name.rsplit("_randomized_", 1)[0]
    return {
        "scenario": scenario.name,
        "base_scenario": base_name,
        "moved_volume": metrics.moved_volume,
        "target_zone_volume": metrics.target_zone_volume,
        "terrain_profile_rmse": metrics.terrain_profile_rmse,
        "volume_conservation_error": metrics.volume_conservation_error,
        "runtime_s": metrics.runtime_s,
    }


def _summarize(rows: list[dict[str, Any]], wall_time_s: float, workers: int) -> dict[str, Any]:
    runtimes = [row["runtime_s"] for row in rows]
    profile_errors = [row["terrain_profile_rmse"] for row in rows]
    return {
        "episode_count": len(rows),
        "workers": workers,
        "wall_time_s": wall_time_s,
        "episodes_per_second": len(rows) / wall_time_s,
        "mean_runtime_s": mean(runtimes) if runtimes else 0.0,
        "max_runtime_s": max(runtimes) if runtimes else 0.0,
        "mean_terrain_profile_rmse": mean(profile_errors) if profile_errors else 0.0,
        "max_terrain_profile_rmse": max(profile_errors) if profile_errors else 0.0,
    }


def _write_report(summary: dict[str, Any], rows: list[dict[str, Any]], output_path: Path) -> None:
    by_scenario: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_scenario.setdefault(row["base_scenario"], []).append(row)

    lines = [
        "# Earthmoving Scale Study",
        "",
        f"Episodes: `{summary['episode_count']}`",
        f"Workers: `{summary['workers']}`",
        f"Throughput: `{summary['episodes_per_second']:.2f}` episodes/s",
        f"Mean episode runtime: `{summary['mean_runtime_s']:.5f}` s",
        "",
        "| base_scenario | episodes | mean_moved_volume | mean_terrain_rmse | max_volume_error |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, scenario_rows in sorted(by_scenario.items()):
        lines.append(
            f"| {name} | {len(scenario_rows)} | "
            f"{mean(row['moved_volume'] for row in scenario_rows):.6f} | "
            f"{mean(row['terrain_profile_rmse'] for row in scenario_rows):.6f} | "
            f"{max(row['volume_conservation_error'] for row in scenario_rows):.6f} |"
        )
    output_path.write_text("\n".join(lines))
