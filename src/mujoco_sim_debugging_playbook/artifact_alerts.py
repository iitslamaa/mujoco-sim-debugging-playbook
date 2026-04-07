from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_alerts(
    *,
    artifact_actions_path: str | Path,
    artifact_exec_summary_path: str | Path,
    artifact_delivery_path: str | Path,
    artifact_capacity_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    actions = _read_json(artifact_actions_path)
    exec_summary = _read_json(artifact_exec_summary_path)
    delivery = _read_json(artifact_delivery_path)
    capacity = _read_json(artifact_capacity_path)

    alerts = []

    alerts.append(
        {
            "severity": "critical" if exec_summary["summary"]["status"] == "fail" else "warning",
            "title": "Artifact readiness is failing",
            "message": (
                f"Current artifact status is {exec_summary['summary']['status']} with "
                f"{exec_summary['summary']['failure_count']} failures."
            ),
        }
    )

    breach_phase = next((phase for phase in delivery["phases"] if phase["status"] == "breach"), None)
    if breach_phase:
        alerts.append(
            {
                "severity": "critical",
                "title": "Recovery phase in breach",
                "message": (
                    f"{breach_phase['name']} is in breach and due on {breach_phase['due_date']}."
                ),
            }
        )

    overloaded = next((owner for owner in capacity["owners"] if owner["status"] == "overloaded"), None)
    if overloaded:
        alerts.append(
            {
                "severity": "warning",
                "title": "Owner overloaded",
                "message": (
                    f"{overloaded['owner']} is overloaded with {overloaded['command_count']} commands."
                ),
            }
        )

    for action in actions["actions"][:2]:
        alerts.append(
            {
                "severity": "info",
                "title": f"Next action: {action['priority']}",
                "message": f"{action['owner']} should take {action['target']} in phase {action['phase']}.",
            }
        )

    payload = {
        "summary": {
            "alert_count": len(alerts),
            "critical_count": sum(1 for alert in alerts if alert["severity"] == "critical"),
            "warning_count": sum(1 for alert in alerts if alert["severity"] == "warning"),
            "info_count": sum(1 for alert in alerts if alert["severity"] == "info"),
        },
        "alerts": alerts,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_alerts.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_alerts.md").write_text(render_artifact_alerts_markdown(payload))
    return payload


def render_artifact_alerts_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Alerts",
        "",
        f"- Alerts: `{payload['summary']['alert_count']}`",
        f"- Critical: `{payload['summary']['critical_count']}`",
        f"- Warning: `{payload['summary']['warning_count']}`",
        f"- Info: `{payload['summary']['info_count']}`",
        "",
        "| severity | title | message |",
        "| --- | --- | --- |",
    ]
    for alert in payload["alerts"]:
        lines.append(f"| {alert['severity']} | {alert['title']} | {alert['message']} |")
    return "\n".join(lines)
