from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_handoff(
    *,
    artifact_digest_path: str | Path,
    artifact_actions_path: str | Path,
    artifact_alerts_path: str | Path,
    artifact_capacity_path: str | Path,
    artifact_exec_summary_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    digest = _read_json(artifact_digest_path)
    actions = _read_json(artifact_actions_path)
    alerts = _read_json(artifact_alerts_path)
    capacity = _read_json(artifact_capacity_path)
    exec_summary = _read_json(artifact_exec_summary_path)

    overloaded_owner = exec_summary["summary"]["overloaded_owner"]
    owner_row = next((row for row in capacity["owners"] if row["owner"] == overloaded_owner), None)

    payload = {
        "summary": {
            "status": exec_summary["summary"]["status"],
            "top_risk_artifact": exec_summary["summary"]["top_risk_artifact"],
            "breach_phase": exec_summary["summary"]["breach_phase"],
            "handoff_owner": overloaded_owner,
            "critical_alert_count": alerts["summary"]["critical_count"],
            "action_count": min(3, len(actions["actions"])),
        },
        "headlines": digest["headlines"][:3],
        "alerts": alerts["alerts"][:3],
        "actions": actions["actions"][:3],
        "owner_context": {
            "owner": overloaded_owner,
            "command_count": owner_row["command_count"] if owner_row else None,
            "phase_count": owner_row["phase_count"] if owner_row else None,
            "status": owner_row["status"] if owner_row else None,
        },
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_handoff.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_handoff.md").write_text(render_artifact_handoff_markdown(payload))
    return payload


def render_artifact_handoff_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Handoff",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Top risk artifact: `{payload['summary']['top_risk_artifact']}`",
        f"- Breach phase: `{payload['summary']['breach_phase']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Critical alerts: `{payload['summary']['critical_alert_count']}`",
        f"- Actions included: `{payload['summary']['action_count']}`",
        "",
        "## Headlines",
        "",
    ]
    for headline in payload["headlines"]:
        lines.append(f"- {headline}")
    lines.extend(["", "## Alerts", ""])
    for alert in payload["alerts"]:
        lines.append(f"- [{alert['severity']}] {alert['title']}: {alert['message']}")
    lines.extend(["", "## Actions", ""])
    for action in payload["actions"]:
        lines.append(f"- {action['priority']} {action['target']} -> {action['owner']}: {action['expected_impact']}")
    lines.extend(["", "## Owner Context", ""])
    lines.append(f"- Owner: `{payload['owner_context']['owner']}`")
    lines.append(f"- Status: `{payload['owner_context']['status']}`")
    lines.append(f"- Command count: `{payload['owner_context']['command_count']}`")
    lines.append(f"- Phase count: `{payload['owner_context']['phase_count']}`")
    return "\n".join(lines)
