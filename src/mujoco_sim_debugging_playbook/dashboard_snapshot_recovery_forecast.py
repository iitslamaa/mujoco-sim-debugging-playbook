from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_recovery_forecast(
    *,
    dashboard_snapshot_readiness_gate_path: str | Path,
    dashboard_snapshot_resolution_plan_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    readiness_gate = _read_json(dashboard_snapshot_readiness_gate_path)
    resolution_plan = _read_json(dashboard_snapshot_resolution_plan_path)

    status = readiness_gate["summary"]["status"]
    critical_count = resolution_plan["summary"]["critical_count"]
    phase_count = resolution_plan["summary"]["phase_count"]

    projected_next_status = status
    if status == "fail" and critical_count <= 1 and phase_count >= 1:
        projected_next_status = "warn"
    if status == "warn" and critical_count == 0:
        projected_next_status = "pass"

    confidence = "medium"
    if status == "fail" and projected_next_status == "warn":
        confidence = "medium"
    elif projected_next_status == "pass":
        confidence = "high"

    payload = {
        "summary": {
            "current_status": status,
            "projected_next_status": projected_next_status,
            "confidence": confidence,
            "phase_count": phase_count,
            "critical_count": critical_count,
        },
        "rationale": [
            f"Current readiness is {status}.",
            f"The active plan has {phase_count} phases.",
            f"Critical alert count is {critical_count}.",
        ],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "recovery_forecast.json").write_text(json.dumps(payload, indent=2))
    (output / "recovery_forecast.md").write_text(render_dashboard_snapshot_recovery_forecast_markdown(payload))
    return payload


def render_dashboard_snapshot_recovery_forecast_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Recovery Forecast",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected next status: `{payload['summary']['projected_next_status']}`",
        f"- Confidence: `{payload['summary']['confidence']}`",
        f"- Phases: `{payload['summary']['phase_count']}`",
        f"- Critical alerts: `{payload['summary']['critical_count']}`",
        "",
        "## Rationale",
        "",
    ]
    for item in payload["rationale"]:
        lines.append(f"- {item}")
    return "\n".join(lines)
