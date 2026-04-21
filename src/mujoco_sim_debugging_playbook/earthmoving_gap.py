from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_earthmoving_gap_report(
    calibration_summary_path: str | Path,
    sensitivity_summary_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    calibration = json.loads(Path(calibration_summary_path).read_text())
    sensitivity = json.loads(Path(sensitivity_summary_path).read_text())
    top_sensitivities = sensitivity["sensitivities"][:5]
    items = []
    for row in calibration["rows"]:
        errors = row["component_errors"]
        dominant_gap = max(errors, key=lambda key: errors[key])
        items.append(
            {
                "scenario": row["scenario"],
                "calibration_error": row["calibration_error"],
                "dominant_gap_metric": dominant_gap,
                "dominant_gap_error": errors[dominant_gap],
                "recommended_action": _recommend_action(dominant_gap, top_sensitivities),
                "calibrated_soil": row["soil"],
            }
        )

    payload = {
        "summary": {
            "scenario_count": len(items),
            "mean_calibration_error": sum(item["calibration_error"] for item in items) / max(len(items), 1),
            "top_global_sensitivity": top_sensitivities[0] if top_sensitivities else None,
        },
        "items": sorted(items, key=lambda item: item["calibration_error"], reverse=True),
        "top_sensitivities": top_sensitivities,
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    summary_path = output / "gap_report.json"
    report_path = output / "report.md"
    summary_path.write_text(json.dumps(payload, indent=2))
    _write_report(payload, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_gap",
        config={
            "calibration_summary": str(calibration_summary_path),
            "sensitivity_summary": str(sensitivity_summary_path),
        },
        inputs=[calibration_summary_path, sensitivity_summary_path],
        outputs=[summary_path, report_path],
        metadata=payload["summary"],
    )
    return payload


def _recommend_action(metric: str, sensitivities: list[dict[str, Any]]) -> str:
    related = [row for row in sensitivities if row["metric"] == metric]
    if related:
        parameter = related[0]["soil_parameter"]
        return f"Prioritize field measurement and calibration of `{parameter}` because it strongly drives `{metric}`."
    if metric == "terrain_profile_rmse":
        return "Add richer terrain-profile observations before and after the pass."
    if metric == "target_zone_volume":
        return "Improve delivered-material measurement around the target berm region."
    return f"Collect additional observations for `{metric}` and rerun calibration."


def _write_report(payload: dict[str, Any], output_path: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# Earthmoving Sim-to-Field Gap Report",
        "",
        f"Scenarios: `{summary['scenario_count']}`",
        f"Mean calibration error: `{summary['mean_calibration_error']:.4f}`",
        "",
        "## Scenario gaps",
        "",
        "| scenario | calibration_error | dominant_gap | gap_error | recommended_action |",
        "| --- | ---: | --- | ---: | --- |",
    ]
    for item in payload["items"]:
        lines.append(
            f"| {item['scenario']} | {item['calibration_error']:.4f} | {item['dominant_gap_metric']} | "
            f"{item['dominant_gap_error']:.4f} | {item['recommended_action']} |"
        )
    lines.extend(["", "## Top sensitivity signals", "", "| soil_parameter | metric | correlation |", "| --- | --- | ---: |"])
    for row in payload["top_sensitivities"]:
        lines.append(f"| {row['soil_parameter']} | {row['metric']} | {row['pearson_correlation']:.4f} |")
    output_path.write_text("\n".join(lines))
