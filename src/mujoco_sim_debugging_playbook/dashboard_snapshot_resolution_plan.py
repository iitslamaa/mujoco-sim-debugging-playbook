from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_resolution_plan(
    *,
    dashboard_snapshot_alert_packet_path: str | Path,
    dashboard_snapshot_actions_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    alert_packet = _read_json(dashboard_snapshot_alert_packet_path)
    actions = _read_json(dashboard_snapshot_actions_path)

    phases = []
    p0_actions = [action for action in actions.get("actions", []) if action["priority"] == "P0"]
    p1_actions = [action for action in actions.get("actions", []) if action["priority"] == "P1"]

    if p0_actions:
        phases.append(
            {
                "name": "Immediate stabilization",
                "priority": "P0",
                "items": [action["title"] for action in p0_actions],
            }
        )
    if p1_actions:
        phases.append(
            {
                "name": "Follow-up cleanup",
                "priority": "P1",
                "items": [action["title"] for action in p1_actions],
            }
        )

    payload = {
        "summary": {
            "current_status": actions["summary"]["current_status"],
            "handoff_owner": actions["summary"]["handoff_owner"],
            "phase_count": len(phases),
            "alert_count": alert_packet["summary"]["alert_count"],
            "critical_count": alert_packet["summary"]["critical_count"],
        },
        "phases": phases,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "resolution_plan.json").write_text(json.dumps(payload, indent=2))
    (output / "resolution_plan.md").write_text(render_dashboard_snapshot_resolution_plan_markdown(payload))
    return payload


def render_dashboard_snapshot_resolution_plan_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Resolution Plan",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Phases: `{payload['summary']['phase_count']}`",
        f"- Alerts: `{payload['summary']['alert_count']}`",
        f"- Critical alerts: `{payload['summary']['critical_count']}`",
        "",
    ]
    for phase in payload["phases"]:
        lines.extend([f"## {phase['name']}", ""])
        for item in phase["items"]:
            lines.append(f"- [{phase['priority']}] {item}")
        lines.append("")
    return "\n".join(lines).rstrip()
