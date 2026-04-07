from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_alert_packet(
    *,
    dashboard_snapshot_actions_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    actions = _read_json(dashboard_snapshot_actions_path)

    alerts: list[dict[str, Any]] = []
    for action in actions.get("actions", []):
        severity = "critical" if action["priority"] == "P0" else "warning"
        alerts.append(
            {
                "severity": severity,
                "title": action["title"],
                "owner": action["owner"],
            }
        )

    payload = {
        "summary": {
            "alert_count": len(alerts),
            "critical_count": sum(1 for alert in alerts if alert["severity"] == "critical"),
            "warning_count": sum(1 for alert in alerts if alert["severity"] == "warning"),
            "handoff_owner": actions["summary"]["handoff_owner"],
            "current_status": actions["summary"]["current_status"],
        },
        "alerts": alerts,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "alert_packet.json").write_text(json.dumps(payload, indent=2))
    (output / "alert_packet.md").write_text(render_dashboard_snapshot_alert_packet_markdown(payload))
    return payload


def render_dashboard_snapshot_alert_packet_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Alert Packet",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Alerts: `{payload['summary']['alert_count']}`",
        f"- Critical: `{payload['summary']['critical_count']}`",
        f"- Warning: `{payload['summary']['warning_count']}`",
        "",
    ]
    for alert in payload["alerts"]:
        lines.append(
            f"- [{alert['severity']}] {alert['title']} "
            f"(owner: `{alert['owner']}`)"
        )
    return "\n".join(lines)
