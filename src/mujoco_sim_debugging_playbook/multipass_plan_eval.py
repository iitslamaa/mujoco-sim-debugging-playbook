from __future__ import annotations

import json
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np

from mujoco_sim_debugging_playbook.earthmoving import (
    BladePlan,
    EarthmovingScenario,
    load_earthmoving_config,
    scenario_from_dict,
)
from mujoco_sim_debugging_playbook.provenance import write_manifest
from mujoco_sim_debugging_playbook.terrain import BladeState, TerrainGrid, apply_blade_pass, build_target_berm


def build_multipass_plan_eval(
    *,
    benchmark_config_path: str | Path,
    jobsite_config_path: str | Path,
    scenario_name: str,
    output_dir: str | Path,
) -> dict[str, Any]:
    config = load_earthmoving_config(benchmark_config_path)
    jobsite = _read_json(jobsite_config_path)
    scenario_payload = next((item for item in config["scenarios"] if item["name"] == scenario_name), None)
    if scenario_payload is None:
        raise ValueError(f"unknown earthmoving scenario: {scenario_name}")
    scenario = scenario_from_dict(scenario_payload)
    machine = jobsite["machine_profile"]
    targets = jobsite["targets"]

    candidates = _candidate_sequences(scenario)
    rows = [_evaluate_sequence(name, scenario, plans, machine, targets) for name, plans in candidates.items()]
    rows.sort(key=lambda row: row["score"], reverse=True)
    payload = {
        "scenario": scenario_name,
        "summary": {
            "candidate_count": len(rows),
            "best_candidate": rows[0],
            "target_productivity_m3_per_hr": targets["min_productivity_m3_per_hr"],
        },
        "rows": rows,
        "recommendation": _recommendation(rows[0], targets),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "multipass_plan_eval.json"
    md_path = output / "multipass_plan_eval.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_multipass_plan_eval(payload))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="multipass_plan_eval",
        config={"scenario": scenario_name},
        inputs=[benchmark_config_path, jobsite_config_path],
        outputs=[json_path, md_path],
        metadata=payload["summary"],
    )
    return payload


def render_multipass_plan_eval(payload: dict[str, Any]) -> str:
    best = payload["summary"]["best_candidate"]
    lines = [
        "# Multi-Pass Plan Evaluation",
        "",
        f"Scenario: `{payload['scenario']}`",
        f"Best candidate: `{best['candidate']}`",
        f"Best decision: `{best['decision']}`",
        f"Best productivity: `{best['productivity_m3_per_hr']:.2f}` m3/hr",
        "",
        "## Candidate Comparison",
        "",
        "| candidate | decision | passes | productivity_m3_hr | cycle_time_s | moved_volume | target_capture | terrain_rmse | score |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['candidate']} | {row['decision']} | {row['pass_count']} | "
            f"{row['productivity_m3_per_hr']:.2f} | {row['cycle_time_s']:.2f} | "
            f"{row['moved_volume']:.6f} | {row['target_capture_ratio']:.3f} | "
            f"{row['terrain_profile_rmse']:.6f} | {row['score']:.3f} |"
        )
    lines.extend(["", "## Recommendation", "", payload["recommendation"]])
    return "\n".join(lines)


def _candidate_sequences(scenario: EarthmovingScenario) -> dict[str, list[BladePlan]]:
    base = scenario.blade
    return {
        "single_pass_baseline": [base],
        "single_pass_wide_cut": [
            replace(base, y=base.y, depth=base.depth * 0.45, width=base.width * 1.28),
        ],
        "two_pass_offset_cleanup": [
            replace(base, y=base.y - 0.035, depth=base.depth * 0.90, width=base.width * 0.92),
            replace(base, y=base.y + 0.035, depth=base.depth * 0.90, width=base.width * 0.92),
        ],
        "two_pass_deeper_finish": [
            replace(base, y=base.y, depth=base.depth * 0.80, width=base.width),
            replace(base, y=base.y, depth=base.depth * 1.18, width=base.width * 1.08),
        ],
    }


def _evaluate_sequence(
    name: str,
    scenario: EarthmovingScenario,
    plans: list[BladePlan],
    machine: dict[str, Any],
    targets: dict[str, float],
) -> dict[str, Any]:
    start = time.perf_counter()
    terrain = TerrainGrid(scenario.terrain)
    initial = terrain.copy()
    target = build_target_berm(
        scenario.terrain,
        target_center_x=scenario.target_center_x,
        target_width=scenario.target_width,
        target_height=scenario.target_height,
    )
    moved_volume = 0.0
    compacted_volume = 0.0
    volume_error = 0.0
    total_distance = 0.0
    blade_paths: list[list[dict[str, float]]] = []

    for plan in plans:
        states = _blade_path(plan)
        summary = apply_blade_pass(terrain, states, scenario.soil)
        moved_volume += summary["moved_volume"]
        compacted_volume += summary["compacted_volume"]
        volume_error += abs(summary["volume_error"])
        total_distance += _path_distance([state.__dict__ for state in states])
        blade_paths.append([state.__dict__ for state in states])

    runtime_s = max(time.perf_counter() - start, 1e-9)
    target_zone_volume = _target_zone_volume(terrain, scenario.target_center_x, scenario.target_width)
    target_capture_ratio = target_zone_volume / max(moved_volume, 1e-9)
    terrain_rmse = terrain.profile_error(target)
    cycle_time_s = _cycle_time(total_distance, len(plans), machine)
    scaled_volume_m3 = moved_volume * machine["volume_scale_factor"]
    productivity_m3_per_hr = scaled_volume_m3 / cycle_time_s * 3600.0
    deposit_progress = _deposit_forward_progress(initial, terrain)
    checks = {
        "productivity": productivity_m3_per_hr >= targets["min_productivity_m3_per_hr"],
        "target_capture": target_capture_ratio >= targets["min_target_capture_ratio"],
        "terrain_rmse": terrain_rmse <= targets["max_terrain_rmse"],
        "volume_conservation": volume_error <= targets["max_volume_conservation_error"],
        "deposit_progress": deposit_progress >= targets["min_deposit_forward_progress_m"],
    }
    score = _score(productivity_m3_per_hr, target_capture_ratio, terrain_rmse, volume_error, targets)
    return {
        "candidate": name,
        "decision": "release_candidate" if all(checks.values()) else "tune_before_field",
        "failed_checks": [key for key, value in checks.items() if not value],
        "pass_count": len(plans),
        "moved_volume": moved_volume,
        "compacted_volume": compacted_volume,
        "volume_conservation_error": volume_error,
        "terrain_profile_rmse": terrain_rmse,
        "target_zone_volume": target_zone_volume,
        "target_capture_ratio": target_capture_ratio,
        "deposit_forward_progress": deposit_progress,
        "cycle_time_s": cycle_time_s,
        "productivity_m3_per_hr": productivity_m3_per_hr,
        "score": score,
        "runtime_s": runtime_s,
        "blade_paths": blade_paths,
    }


def _blade_path(blade: BladePlan) -> list[BladeState]:
    xs = np.linspace(blade.start_x, blade.end_x, blade.steps)
    return [BladeState(x=float(x), y=blade.y, yaw=blade.yaw, width=blade.width, depth=blade.depth) for x in xs]


def _cycle_time(total_distance: float, pass_count: int, machine: dict[str, Any]) -> float:
    return (
        total_distance / machine["blade_speed_mps"]
        + total_distance / machine["return_speed_mps"]
        + pass_count * (machine["turnaround_s"] + machine["dump_settle_s"])
    )


def _score(
    productivity: float,
    target_capture: float,
    terrain_rmse: float,
    volume_error: float,
    targets: dict[str, float],
) -> float:
    productivity_term = productivity / max(targets["min_productivity_m3_per_hr"], 1e-9)
    capture_term = target_capture / max(targets["min_target_capture_ratio"], 1e-9)
    rmse_penalty = terrain_rmse / max(targets["max_terrain_rmse"], 1e-9)
    volume_penalty = volume_error / max(targets["max_volume_conservation_error"], 1e-9)
    return float(productivity_term + 0.35 * capture_term - 0.25 * rmse_penalty - 0.15 * volume_penalty)


def _target_zone_volume(terrain: TerrainGrid, center_x: float, width: float) -> float:
    mask = np.abs(terrain.xs[:, None] - center_x) <= width
    excess = np.clip(terrain.heights - terrain.config.base_height, 0.0, None)
    return float(np.sum(np.where(mask, excess, 0.0)) * terrain.cell_area)


def _deposit_forward_progress(initial: TerrainGrid, final: TerrainGrid) -> float:
    cut_weights = np.clip(initial.heights - final.heights, 0.0, None)
    deposit_weights = np.clip(final.heights - initial.heights, 0.0, None)
    return _centroid_x(final, deposit_weights) - _centroid_x(initial, cut_weights)


def _centroid_x(terrain: TerrainGrid, weights: np.ndarray) -> float:
    total = float(np.sum(weights))
    if total <= 1e-12:
        return 0.0
    return float(np.sum(terrain.xs[:, None] * weights) / total)


def _path_distance(blade_path: list[dict[str, float]]) -> float:
    distance = 0.0
    for left, right in zip(blade_path, blade_path[1:]):
        dx = right["x"] - left["x"]
        dy = right["y"] - left["y"]
        distance += (dx * dx + dy * dy) ** 0.5
    return distance


def _recommendation(best: dict[str, Any], targets: dict[str, float]) -> str:
    if best["decision"] == "release_candidate":
        return (
            f"Promote `{best['candidate']}` to replay and robustness testing: it clears the configured "
            f"{targets['min_productivity_m3_per_hr']:.2f} m3/hr productivity target and the placement gates."
        )
    return (
        f"Use `{best['candidate']}` as the next tuning baseline, but keep it out of field-trial readiness until "
        f"failed checks are resolved: {', '.join(best['failed_checks'])}."
    )


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
