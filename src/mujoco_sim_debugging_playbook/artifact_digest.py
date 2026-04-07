from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_digest(
    *,
    artifact_alerts_path: str | Path,
    artifact_actions_path: str | Path,
    artifact_history_path: str | Path,
    artifact_exec_summary_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    alerts = _read_json(artifact_alerts_path)
    actions = _read_json(artifact_actions_path)
    history = _read_json(artifact_history_path)
    exec_summary = _read_json(artifact_exec_summary_path)

    headlines = [
        f"Artifact status is {exec_summary['summary']['status']} with {exec_summary['summary']['failure_count']} failures.",
        f"Top risk remains {exec_summary['summary']['top_risk_artifact']} at {exec_summary['summary']['top_risk_score']:.3f}.",
        f"Trend direction is {history['summary']['status_direction']} toward {history['summary']['projected_terminal_status']}.",
    ]

    payload = {
        "summary": {
            "headline_count": len(headlines),
            "critical_alert_count": alerts["summary"]["critical_count"],
            "action_count": actions["summary"]["action_count"],
            "projected_terminal_status": history["summary"]["projected_terminal_status"],
        },
        "headlines": headlines,
        "alerts": alerts["alerts"][:3],
        "actions": actions["actions"][:3],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_digest.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_digest.md").write_text(render_artifact_digest_markdown(payload))
    return payload


def render_artifact_digest_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Digest",
        "",
        f"- Headlines: `{payload['summary']['headline_count']}`",
        f"- Critical alerts: `{payload['summary']['critical_alert_count']}`",
        f"- Top actions: `{payload['summary']['action_count']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        "",
        "## Headlines",
        "",
    ]
    for line in payload["headlines"]:
        lines.append(f"- {line}")
    lines.extend(["", "## Key Alerts", ""])
    for alert in payload["alerts"]:
        lines.append(f"- [{alert['severity']}] {alert['title']}: {alert['message']}")
    lines.extend(["", "## Top Actions", ""])
    for action in payload["actions"]:
        lines.append(f"- {action['priority']} {action['target']} -> {action['owner']}: {action['expected_impact']}")
    return "\n".join(lines)
