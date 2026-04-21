from __future__ import annotations

import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.earthmoving import EarthmovingScenario, EarthmovingSimulation, load_earthmoving_config, scenario_from_dict
from mujoco_sim_debugging_playbook.provenance import write_manifest
from mujoco_sim_debugging_playbook.terrain import SoilConfig


def load_field_logs(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def calibrate_earthmoving_soil(
    benchmark_config_path: str | Path,
    field_logs_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    benchmark = load_earthmoving_config(benchmark_config_path)
    logs = load_field_logs(field_logs_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    scenarios = {item["name"]: scenario_from_dict(item) for item in benchmark["scenarios"]}
    rows = []
    for log in logs["logs"]:
        scenario = scenarios[log["scenario"]]
        candidates = _candidate_soils(scenario.soil)
        best = min(
            (_evaluate_candidate(scenario, soil, log) for soil in candidates),
            key=lambda item: item["calibration_error"],
        )
        rows.append(best)

    summary_path = output / "calibration_summary.json"
    report_path = output / "report.md"
    payload = {"name": "earthmoving_calibration", "rows": rows, "field_logs": logs["logs"]}
    summary_path.write_text(json.dumps(payload, indent=2))
    _write_report(rows, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_calibration",
        config={"benchmark_config": str(benchmark_config_path), "field_logs": str(field_logs_path)},
        inputs=[benchmark_config_path, field_logs_path],
        outputs=[summary_path, report_path],
        metadata={"log_count": len(rows)},
    )
    return {"rows": rows, "output_dir": str(output)}


def _candidate_soils(base: SoilConfig) -> list[SoilConfig]:
    candidates = []
    cohesion_scales = [0.7, 1.0, 1.3]
    coupling_scales = [0.75, 1.0, 1.25]
    compaction_scales = [0.75, 1.0, 1.25]
    for cohesion_scale in cohesion_scales:
        for coupling_scale in coupling_scales:
            for compaction_scale in compaction_scales:
                candidates.append(
                    SoilConfig(
                        cohesion=max(0.0, base.cohesion * cohesion_scale),
                        friction_angle_deg=base.friction_angle_deg,
                        compaction_rate=min(0.8, base.compaction_rate * compaction_scale),
                        blade_coupling=min(1.0, base.blade_coupling * coupling_scale),
                        spillover_rate=base.spillover_rate,
                    )
                )
    return candidates


def _evaluate_candidate(scenario: EarthmovingScenario, soil: SoilConfig, log: dict[str, Any]) -> dict[str, Any]:
    candidate = replace(scenario, soil=soil)
    result = EarthmovingSimulation(candidate).run()
    metrics = result.metrics
    moved_error = _relative_error(metrics.moved_volume, log["observed_moved_volume"])
    target_error = _relative_error(metrics.target_zone_volume, log["observed_target_zone_volume"])
    profile_error = _relative_error(metrics.terrain_profile_rmse, log["observed_terrain_profile_rmse"])
    return {
        "scenario": scenario.name,
        "soil": asdict(soil),
        "simulated": asdict(metrics),
        "observed": {
            "moved_volume": log["observed_moved_volume"],
            "target_zone_volume": log["observed_target_zone_volume"],
            "terrain_profile_rmse": log["observed_terrain_profile_rmse"],
        },
        "component_errors": {
            "moved_volume": moved_error,
            "target_zone_volume": target_error,
            "terrain_profile_rmse": profile_error,
        },
        "calibration_error": 0.45 * moved_error + 0.35 * target_error + 0.2 * profile_error,
    }


def _relative_error(simulated: float, observed: float) -> float:
    return abs(simulated - observed) / max(abs(observed), 1e-9)


def _write_report(rows: list[dict[str, Any]], output_path: Path) -> None:
    lines = [
        "# Earthmoving Calibration",
        "",
        "Grid-search calibration of soil/deformation parameters against observed field-log metrics.",
        "",
        "| scenario | calibration_error | cohesion | coupling | compaction | moved_err | target_err | profile_err |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        soil = row["soil"]
        errors = row["component_errors"]
        lines.append(
            f"| {row['scenario']} | {row['calibration_error']:.4f} | {soil['cohesion']:.3f} | "
            f"{soil['blade_coupling']:.3f} | {soil['compaction_rate']:.3f} | "
            f"{errors['moved_volume']:.3f} | {errors['target_zone_volume']:.3f} | {errors['terrain_profile_rmse']:.3f} |"
        )
    output_path.write_text("\n".join(lines))
