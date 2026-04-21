from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_earthmoving_review_packet(
    *,
    benchmark_summary_path: str | Path,
    calibration_summary_path: str | Path,
    scale_summary_path: str | Path,
    sensitivity_summary_path: str | Path,
    gate_path: str | Path,
    gap_report_path: str | Path,
    jobsite_eval_path: str | Path | None = None,
    output_dir: str | Path,
) -> dict[str, Any]:
    benchmark = _read_json(benchmark_summary_path)
    calibration = _read_json(calibration_summary_path)
    scale = _read_json(scale_summary_path)
    sensitivity = _read_json(sensitivity_summary_path)
    gate = _read_json(gate_path)
    gap = _read_json(gap_report_path)
    jobsite = _read_json(jobsite_eval_path) if jobsite_eval_path and Path(jobsite_eval_path).exists() else None

    best_scenario = min(benchmark["rows"], key=lambda row: row["terrain_profile_rmse"])
    hardest_scenario = max(benchmark["rows"], key=lambda row: row["terrain_profile_rmse"])
    top_gap = gap["items"][0] if gap["items"] else None
    top_sensitivity = sensitivity["summary"]["top_sensitivity"]
    payload = {
        "summary": {
            "gate_status": gate["status"],
            "scenario_count": len(benchmark["rows"]),
            "scale_episode_count": scale["summary"]["episode_count"],
            "episodes_per_second": scale["summary"]["episodes_per_second"],
            "best_scenario": best_scenario["scenario"],
            "hardest_scenario": hardest_scenario["scenario"],
            "mean_deposit_forward_progress": _mean(row.get("deposit_forward_progress", 0.0) for row in benchmark["rows"]),
            "mean_calibration_error": gap["summary"]["mean_calibration_error"],
            "top_sensitivity": top_sensitivity,
            "jobsite_decision": jobsite["summary"]["overall_decision"] if jobsite else "not_evaluated",
            "release_candidate_count": jobsite["summary"]["release_candidate_count"] if jobsite else 0,
            "mean_productivity_m3_per_hr": jobsite["summary"]["mean_productivity_m3_per_hr"] if jobsite else 0.0,
        },
        "readiness_signals": [
            _signal("Quality gate", gate["status"], "Earthmoving realism and throughput thresholds"),
            _signal(
                "Jobsite decision",
                jobsite["summary"]["overall_decision"] if jobsite else "not evaluated",
                "Cycle-time, productivity, placement, and rework-risk scorecard",
            ),
            _signal("Scale throughput", f"{scale['summary']['episodes_per_second']:.2f} episodes/s", "Randomized batch evaluation speed"),
            _signal("Best terrain match", best_scenario["scenario"], f"RMSE {best_scenario['terrain_profile_rmse']:.5f}"),
            _signal("Mean deposit progress", f"{_mean(row.get('deposit_forward_progress', 0.0) for row in benchmark['rows']):.3f} m", "Centroid displacement from cut region to deposit region"),
            _signal("Largest sim-to-field gap", top_gap["scenario"] if top_gap else "none", top_gap["recommended_action"] if top_gap else "No gap items"),
        ],
        "scenario_table": [
            {
                "scenario": row["scenario"],
                "moved_volume": row["moved_volume"],
                "target_zone_volume": row.get("target_zone_volume", 0.0),
                "deposit_forward_progress": row.get("deposit_forward_progress", 0.0),
                "terrain_profile_rmse": row["terrain_profile_rmse"],
                "volume_conservation_error": row["volume_conservation_error"],
                "runtime_s": row["runtime_s"],
            }
            for row in sorted(benchmark["rows"], key=lambda item: item["terrain_profile_rmse"])
        ],
        "calibration_table": [
            {
                "scenario": row["scenario"],
                "calibration_error": row["calibration_error"],
                "dominant_component": max(row["component_errors"], key=lambda key: row["component_errors"][key]),
                "soil": row["soil"],
            }
            for row in calibration["rows"]
        ],
        "top_sensitivities": sensitivity["sensitivities"][:8],
        "gap_items": gap["items"],
        "jobsite_eval": jobsite,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    packet_path = output / "review_packet.json"
    report_path = output / "review_packet.md"
    packet_path.write_text(json.dumps(payload, indent=2))
    report_path.write_text(render_review_packet_markdown(payload))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_review_packet",
        config={
            "benchmark_summary": str(benchmark_summary_path),
            "calibration_summary": str(calibration_summary_path),
            "scale_summary": str(scale_summary_path),
            "sensitivity_summary": str(sensitivity_summary_path),
            "gate": str(gate_path),
            "gap_report": str(gap_report_path),
            "jobsite_eval": str(jobsite_eval_path) if jobsite_eval_path else None,
        },
        inputs=[
            benchmark_summary_path,
            calibration_summary_path,
            scale_summary_path,
            sensitivity_summary_path,
            gate_path,
            gap_report_path,
            *([jobsite_eval_path] if jobsite_eval_path else []),
        ],
        outputs=[packet_path, report_path],
        metadata=payload["summary"],
    )
    return payload


def render_review_packet_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Earthmoving Review Packet",
        "",
        f"- Gate status: `{summary['gate_status']}`",
        f"- Scenarios: `{summary['scenario_count']}`",
        f"- Scale episodes: `{summary['scale_episode_count']}`",
        f"- Throughput: `{summary['episodes_per_second']:.2f}` episodes/s",
        f"- Best scenario: `{summary['best_scenario']}`",
        f"- Hardest scenario: `{summary['hardest_scenario']}`",
        f"- Mean deposit progress: `{summary['mean_deposit_forward_progress']:.3f}` m",
        f"- Mean calibration error: `{summary['mean_calibration_error']:.4f}`",
        f"- Jobsite decision: `{summary['jobsite_decision']}`",
        f"- Mean scaled productivity: `{summary['mean_productivity_m3_per_hr']:.2f}` m3/hr",
        "",
        "## Readiness Signals",
        "",
        "| signal | value | detail |",
        "| --- | --- | --- |",
    ]
    for signal in payload["readiness_signals"]:
        lines.append(f"| {signal['name']} | {signal['value']} | {signal['detail']} |")

    lines.extend(["", "## Scenario Results", "", "| scenario | moved_volume | deposit_progress_m | terrain_rmse | volume_error | runtime_s |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for row in payload["scenario_table"]:
        lines.append(
            f"| {row['scenario']} | {row['moved_volume']:.6f} | {row['deposit_forward_progress']:.4f} | {row['terrain_profile_rmse']:.6f} | "
            f"{row['volume_conservation_error']:.6f} | {row['runtime_s']:.5f} |"
        )

    if payload.get("jobsite_eval"):
        lines.extend(
            [
                "",
                "## Jobsite Autonomy Scorecard",
                "",
                "| scenario | decision | productivity_m3_hr | cycle_time_s | target_capture | bottleneck |",
                "| --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for row in payload["jobsite_eval"]["rows"]:
            lines.append(
                f"| {row['scenario']} | {row['decision']} | {row['productivity_m3_per_hr']:.2f} | "
                f"{row['cycle_time_s']:.2f} | {row['target_capture_ratio']:.3f} | {row['bottleneck']} |"
            )

    lines.extend(["", "## Top Sensitivities", "", "| soil_parameter | metric | correlation |", "| --- | --- | ---: |"])
    for row in payload["top_sensitivities"]:
        lines.append(f"| {row['soil_parameter']} | {row['metric']} | {row['pearson_correlation']:.4f} |")

    lines.extend(["", "## Sim-to-Field Gap Actions", "", "| scenario | dominant_gap | recommendation |", "| --- | --- | --- |"])
    for item in payload["gap_items"]:
        lines.append(f"| {item['scenario']} | {item['dominant_gap_metric']} | {item['recommended_action']} |")
    return "\n".join(lines)


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _signal(name: str, value: str, detail: str) -> dict[str, str]:
    return {"name": name, "value": value, "detail": detail}


def _mean(values: Any) -> float:
    items = [float(value) for value in values]
    return sum(items) / len(items) if items else 0.0
