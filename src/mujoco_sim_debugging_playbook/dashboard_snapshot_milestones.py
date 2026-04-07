from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_milestones(
    *,
    dashboard_snapshot_recovery_forecast_path: str | Path,
    dashboard_snapshot_scorecard_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    recovery_forecast = _read_json(dashboard_snapshot_recovery_forecast_path)
    scorecard = _read_json(dashboard_snapshot_scorecard_path)

    summary = scorecard["summary"]
    milestones = [
        {"label": "Current", "status": recovery_forecast["summary"]["current_status"]},
        {"label": "Next", "status": recovery_forecast["summary"]["projected_next_status"]},
        {"label": "Terminal", "status": summary["projected_terminal_status"]},
    ]

    payload = {
        "summary": {
            "milestone_count": len(milestones),
            "current_status": recovery_forecast["summary"]["current_status"],
            "projected_next_status": recovery_forecast["summary"]["projected_next_status"],
            "terminal_status": summary["projected_terminal_status"],
            "confidence": recovery_forecast["summary"]["confidence"],
        },
        "milestones": milestones,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "milestones.json").write_text(json.dumps(payload, indent=2))
    (output / "milestones.md").write_text(render_dashboard_snapshot_milestones_markdown(payload))
    return payload


def render_dashboard_snapshot_milestones_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Milestones",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected next status: `{payload['summary']['projected_next_status']}`",
        f"- Terminal status: `{payload['summary']['terminal_status']}`",
        f"- Confidence: `{payload['summary']['confidence']}`",
        f"- Milestones: `{payload['summary']['milestone_count']}`",
        "",
    ]
    for milestone in payload["milestones"]:
        lines.append(f"- {milestone['label']}: `{milestone['status']}`")
    return "\n".join(lines)
