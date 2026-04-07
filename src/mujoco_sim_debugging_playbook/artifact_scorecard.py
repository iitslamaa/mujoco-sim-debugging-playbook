from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_scorecard(
    *,
    artifact_closeout_path: str | Path,
    artifact_exec_summary_path: str | Path,
    artifact_alerts_path: str | Path,
    artifact_actions_path: str | Path,
    artifact_history_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    closeout = _read_json(artifact_closeout_path)
    exec_summary = _read_json(artifact_exec_summary_path)
    alerts = _read_json(artifact_alerts_path)
    actions = _read_json(artifact_actions_path)
    history = _read_json(artifact_history_path)

    metrics = [
        {"name": "current_status", "value": closeout["summary"]["current_status"]},
        {"name": "closeout_status", "value": closeout["summary"]["status"]},
        {"name": "projected_terminal_status", "value": closeout["summary"]["projected_terminal_status"]},
        {"name": "failure_count", "value": exec_summary["summary"]["failure_count"]},
        {"name": "top_risk_score", "value": round(exec_summary["summary"]["top_risk_score"], 3)},
        {"name": "critical_alert_count", "value": alerts["summary"]["critical_count"]},
        {"name": "remaining_action_count", "value": closeout["summary"]["remaining_action_count"]},
        {"name": "status_direction", "value": history["summary"]["status_direction"]},
    ]

    payload = {
        "summary": {
            "metric_count": len(metrics),
            "current_status": closeout["summary"]["current_status"],
            "closeout_status": closeout["summary"]["status"],
            "projected_terminal_status": closeout["summary"]["projected_terminal_status"],
        },
        "metrics": metrics,
        "top_actions": actions["actions"][:3],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_scorecard.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_scorecard.md").write_text(render_artifact_scorecard_markdown(payload))
    return payload


def render_artifact_scorecard_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Scorecard",
        "",
        f"- Metrics: `{payload['summary']['metric_count']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Closeout status: `{payload['summary']['closeout_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        "",
        "| metric | value |",
        "| --- | --- |",
    ]
    for metric in payload["metrics"]:
        lines.append(f"| {metric['name']} | {metric['value']} |")
    lines.extend(["", "## Top Actions", ""])
    for action in payload["top_actions"]:
        lines.append(f"- {action['priority']} {action['target']} -> {action['owner']}")
    return "\n".join(lines)
