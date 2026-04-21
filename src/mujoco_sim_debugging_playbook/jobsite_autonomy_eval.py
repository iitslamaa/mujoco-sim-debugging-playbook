from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_jobsite_autonomy_eval(
    *,
    benchmark_summary_path: str | Path,
    eval_config_path: str | Path,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    benchmark = _read_json(benchmark_summary_path)
    config = _read_json(eval_config_path)
    machine = config["machine_profile"]
    targets = config["targets"]
    output = Path(output_dir or config["output_dir"])
    output.mkdir(parents=True, exist_ok=True)

    rows = [_score_result(result, machine, targets) for result in benchmark["results"]]
    summary = _summarize(rows, targets, machine)
    payload = {
        "name": config["name"],
        "machine_profile": machine,
        "targets": targets,
        "summary": summary,
        "rows": rows,
        "operator_notes": _operator_notes(rows),
    }

    json_path = output / "jobsite_autonomy_eval.json"
    report_path = output / "report.md"
    json_path.write_text(json.dumps(payload, indent=2))
    report_path.write_text(render_jobsite_autonomy_eval_markdown(payload))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="jobsite_autonomy_eval",
        config=config,
        inputs=[benchmark_summary_path, eval_config_path],
        outputs=[json_path, report_path],
        metadata=summary,
    )
    return payload


def render_jobsite_autonomy_eval_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Jobsite Autonomy Evaluation",
        "",
        "Deployment-style scorecard that turns terrain simulation outputs into cycle-time, productivity, placement, and rework-risk signals.",
        "",
        f"- Overall decision: `{summary['overall_decision']}`",
        f"- Release-candidate scenarios: `{summary['release_candidate_count']}` / `{summary['scenario_count']}`",
        f"- Mean scaled productivity: `{summary['mean_productivity_m3_per_hr']:.2f}` m3/hr",
        f"- Mean target capture: `{summary['mean_target_capture_ratio']:.3f}`",
        f"- Top bottleneck: `{summary['top_bottleneck']}`",
        "",
        "## Scenario Scorecard",
        "",
        "| scenario | decision | productivity_m3_hr | cycle_time_s | target_capture | rework_risk | bottleneck |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['scenario']} | {row['decision']} | {row['productivity_m3_per_hr']:.2f} | "
            f"{row['cycle_time_s']:.2f} | {row['target_capture_ratio']:.3f} | "
            f"{row['rework_risk_score']:.2f} | {row['bottleneck']} |"
        )

    lines.extend(["", "## Operator Notes", ""])
    for note in payload["operator_notes"]:
        lines.append(f"- {note}")
    return "\n".join(lines)


def _score_result(result: dict[str, Any], machine: dict[str, Any], targets: dict[str, Any]) -> dict[str, Any]:
    metrics = result["metrics"]
    blade_path = result["blade_path"]
    pass_distance = _path_distance(blade_path)
    cycle_time_s = (
        pass_distance / machine["blade_speed_mps"]
        + pass_distance / machine["return_speed_mps"]
        + machine["turnaround_s"]
        + machine["dump_settle_s"]
    )
    scaled_volume_m3 = metrics["moved_volume"] * machine["volume_scale_factor"]
    productivity_m3_per_hr = scaled_volume_m3 / cycle_time_s * 3600.0
    target_capture_ratio = metrics["target_zone_volume"] / max(metrics["moved_volume"], 1e-9)
    checks = {
        "productivity": productivity_m3_per_hr >= targets["min_productivity_m3_per_hr"],
        "target_capture": target_capture_ratio >= targets["min_target_capture_ratio"],
        "terrain_rmse": metrics["terrain_profile_rmse"] <= targets["max_terrain_rmse"],
        "volume_conservation": metrics["volume_conservation_error"] <= targets["max_volume_conservation_error"],
        "deposit_progress": metrics["deposit_forward_progress"] >= targets["min_deposit_forward_progress_m"],
    }
    failed = [name for name, passed in checks.items() if not passed]
    rework_risk_score = _rework_risk_score(metrics, target_capture_ratio, targets)
    bottleneck = _bottleneck(metrics, target_capture_ratio, productivity_m3_per_hr, targets)
    return {
        "scenario": result["scenario"],
        "decision": "release_candidate" if not failed else "tune_before_field",
        "failed_checks": failed,
        "pass_distance_m": pass_distance,
        "cycle_time_s": cycle_time_s,
        "scaled_moved_volume_m3": scaled_volume_m3,
        "productivity_m3_per_hr": productivity_m3_per_hr,
        "target_capture_ratio": target_capture_ratio,
        "rework_risk_score": rework_risk_score,
        "bottleneck": bottleneck,
        "checks": checks,
    }


def _summarize(rows: list[dict[str, Any]], targets: dict[str, Any], machine: dict[str, Any]) -> dict[str, Any]:
    release_count = sum(row["decision"] == "release_candidate" for row in rows)
    bottlenecks = [row["bottleneck"] for row in rows if row["bottleneck"] != "none"]
    top_bottleneck = max(set(bottlenecks), key=bottlenecks.count) if bottlenecks else "none"
    mean_productivity = _mean(row["productivity_m3_per_hr"] for row in rows)
    mean_capture = _mean(row["target_capture_ratio"] for row in rows)
    overall = "field_trial_ready" if release_count == len(rows) else "needs_calibration_before_field_trial"
    return {
        "overall_decision": overall,
        "scenario_count": len(rows),
        "release_candidate_count": release_count,
        "mean_productivity_m3_per_hr": mean_productivity,
        "mean_target_capture_ratio": mean_capture,
        "top_bottleneck": top_bottleneck,
        "target_productivity_m3_per_hr": targets["min_productivity_m3_per_hr"],
        "machine_profile": machine["label"],
    }


def _operator_notes(rows: list[dict[str, Any]]) -> list[str]:
    notes = []
    for row in rows:
        if row["decision"] == "release_candidate":
            notes.append(
                f"{row['scenario']}: candidate for a supervised field trial; preserve the replay bundle as the release baseline."
            )
        else:
            notes.append(
                f"{row['scenario']}: tune before field work; primary bottleneck is {row['bottleneck']} "
                f"with failed checks {', '.join(row['failed_checks'])}."
            )
    return notes


def _path_distance(blade_path: list[dict[str, float]]) -> float:
    if len(blade_path) < 2:
        return 0.0
    distance = 0.0
    for left, right in zip(blade_path, blade_path[1:]):
        dx = right["x"] - left["x"]
        dy = right["y"] - left["y"]
        distance += (dx * dx + dy * dy) ** 0.5
    return distance


def _rework_risk_score(metrics: dict[str, float], target_capture_ratio: float, targets: dict[str, float]) -> float:
    rmse_term = min(metrics["terrain_profile_rmse"] / max(targets["max_terrain_rmse"], 1e-9), 2.0)
    capture_term = min(targets["min_target_capture_ratio"] / max(target_capture_ratio, 1e-9), 2.0)
    volume_term = min(metrics["volume_conservation_error"] / max(targets["max_volume_conservation_error"], 1e-9), 2.0)
    return round((0.45 * rmse_term + 0.35 * capture_term + 0.20 * volume_term) / 2.0, 3)


def _bottleneck(
    metrics: dict[str, float],
    target_capture_ratio: float,
    productivity_m3_per_hr: float,
    targets: dict[str, float],
) -> str:
    candidates = {
        "target_placement": targets["min_target_capture_ratio"] - target_capture_ratio,
        "terrain_shape_error": metrics["terrain_profile_rmse"] - targets["max_terrain_rmse"],
        "volume_accounting": metrics["volume_conservation_error"] - targets["max_volume_conservation_error"],
        "deposit_progress": targets["min_deposit_forward_progress_m"] - metrics["deposit_forward_progress"],
        "cycle_productivity": targets["min_productivity_m3_per_hr"] - productivity_m3_per_hr,
    }
    positive = {name: value for name, value in candidates.items() if value > 0}
    return max(positive, key=positive.get) if positive else "none"


def _mean(values: Any) -> float:
    items = [float(value) for value in values]
    return sum(items) / len(items) if items else 0.0


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
