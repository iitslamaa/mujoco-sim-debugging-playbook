from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mujoco_sim_debugging_playbook.earthmoving import (
    EarthmovingResult,
    EarthmovingScenario,
    EarthmovingSimulation,
    load_earthmoving_config,
    result_to_dict,
    scenario_from_dict,
)
from mujoco_sim_debugging_playbook.environment import capture_environment_report
from mujoco_sim_debugging_playbook.provenance import write_manifest
from mujoco_sim_debugging_playbook.terrain import SoilConfig


def run_earthmoving_benchmark(config_path: str | Path) -> dict[str, Any]:
    payload = load_earthmoving_config(config_path)
    output_dir = Path(payload["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    results: list[EarthmovingResult] = []
    for scenario_payload in payload["scenarios"]:
        scenario = scenario_from_dict(scenario_payload)
        result = EarthmovingSimulation(scenario).run()
        results.append(result)
        _plot_terrain_triptych(result, output_dir / f"{result.scenario}_terrain.png")

    rows = [_row_from_result(result) for result in results]
    summary_path = output_dir / "earthmoving_summary.json"
    report_path = output_dir / "report.md"
    summary_path.write_text(json.dumps({
        "name": payload["name"],
        "rows": rows,
        "results": [result_to_dict(result) for result in results],
        "environment": capture_environment_report(Path.cwd()),
    }, indent=2))
    _plot_metric_bars(rows, output_dir)
    _write_report(rows, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output_dir,
        run_type="earthmoving_benchmark",
        config=payload,
        inputs=[config_path],
        outputs=[summary_path, report_path, *[str(path) for path in output_dir.glob("*.png")]],
        metadata={"scenario_count": len(rows)},
    )
    return {"rows": rows, "output_dir": str(output_dir)}


def randomized_soil_variants(
    scenario: EarthmovingScenario,
    seed: int,
    episodes: int,
    variation: float,
) -> list[EarthmovingScenario]:
    rng = np.random.default_rng(seed)
    variants = []
    for index in range(episodes):
        soil = scenario.soil
        scale = lambda value: float(value * rng.uniform(1.0 - variation, 1.0 + variation))
        variants.append(
            replace(
                scenario,
                name=f"{scenario.name}_randomized_{index:03d}",
                soil=SoilConfig(
                    cohesion=max(0.0, scale(soil.cohesion)),
                    friction_angle_deg=float(np.clip(scale(soil.friction_angle_deg), 5.0, 50.0)),
                    compaction_rate=float(np.clip(scale(soil.compaction_rate), 0.0, 0.8)),
                    blade_coupling=float(np.clip(scale(soil.blade_coupling), 0.05, 1.0)),
                    spillover_rate=float(np.clip(scale(soil.spillover_rate), 0.0, 1.0)),
                ),
            )
        )
    return variants


def _row_from_result(result: EarthmovingResult) -> dict[str, Any]:
    metrics = result.metrics
    return {
        "scenario": result.scenario,
        "moved_volume": metrics.moved_volume,
        "compacted_volume": metrics.compacted_volume,
        "volume_conservation_error": metrics.volume_conservation_error,
        "terrain_profile_rmse": metrics.terrain_profile_rmse,
        "target_zone_volume": metrics.target_zone_volume,
        "cut_centroid_x": metrics.cut_centroid_x,
        "cut_centroid_y": metrics.cut_centroid_y,
        "deposit_centroid_x": metrics.deposit_centroid_x,
        "deposit_centroid_y": metrics.deposit_centroid_y,
        "deposit_forward_progress": metrics.deposit_forward_progress,
        "material_moved_per_second": metrics.material_moved_per_second,
        "runtime_s": metrics.runtime_s,
    }


def _plot_terrain_triptych(result: EarthmovingResult, path: Path) -> None:
    terrains = [
        ("Initial", result.initial_terrain),
        ("Final", result.final_terrain),
        ("Target", result.target_terrain),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharex=True, sharey=True)
    vmax = max(float(np.asarray(item[1]["heights"]).max()) for item in terrains)
    for axis, (title, terrain) in zip(axes, terrains):
        xs = np.asarray(terrain["xs"])
        ys = np.asarray(terrain["ys"])
        heights = np.asarray(terrain["heights"]).T
        mesh = axis.pcolormesh(xs, ys, heights, shading="auto", vmin=0.0, vmax=vmax)
        axis.set_title(title)
        axis.set_xlabel("x (m)")
        axis.set_ylabel("y (m)")
    fig.colorbar(mesh, ax=axes, label="height (m)", shrink=0.8)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _plot_metric_bars(rows: list[dict[str, Any]], output_dir: Path) -> None:
    metrics = [
        ("moved_volume", "Moved volume"),
        ("deposit_forward_progress", "Deposit forward progress"),
        ("terrain_profile_rmse", "Terrain RMSE"),
        ("volume_conservation_error", "Volume conservation error"),
        ("runtime_s", "Runtime"),
    ]
    scenarios = [row["scenario"] for row in rows]
    for key, title in metrics:
        fig, axis = plt.subplots(figsize=(8, 4.4))
        axis.bar(scenarios, [row[key] for row in rows], color="#2563eb")
        axis.set_title(f"Earthmoving benchmark: {title}")
        axis.set_ylabel(key)
        axis.tick_params(axis="x", rotation=20)
        axis.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(output_dir / f"{key}.png", dpi=180)
        plt.close(fig)


def _write_report(rows: list[dict[str, Any]], output_path: Path) -> None:
    lines = [
        "# Earthmoving Benchmark",
        "",
        "Construction-machine blade scenarios evaluated against terrain deformation, target berm, material displacement, conservation, and runtime metrics.",
        "",
        "| scenario | moved_volume | target_zone_volume | deposit_progress_m | terrain_rmse | volume_error | runtime_s |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in sorted(rows, key=lambda item: item["terrain_profile_rmse"]):
        lines.append(
            f"| {row['scenario']} | {row['moved_volume']:.6f} | {row['target_zone_volume']:.6f} | "
            f"{row['deposit_forward_progress']:.4f} | "
            f"{row['terrain_profile_rmse']:.6f} | {row['volume_conservation_error']:.6f} | {row['runtime_s']:.4f} |"
        )
    best = min(rows, key=lambda item: item["terrain_profile_rmse"])
    lines.extend(
        [
            "",
            f"Best terrain-profile match: `{best['scenario']}` with `{best['terrain_profile_rmse']:.6f}` RMSE.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines))
