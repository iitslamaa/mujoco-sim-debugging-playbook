from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_packet(
    *,
    artifact_scorecard_path: str | Path,
    artifact_digest_path: str | Path,
    artifact_handoff_path: str | Path,
    artifact_closeout_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    scorecard = _read_json(artifact_scorecard_path)
    digest = _read_json(artifact_digest_path)
    handoff = _read_json(artifact_handoff_path)
    closeout = _read_json(artifact_closeout_path)

    payload = {
        "summary": {
            "current_status": scorecard["summary"]["current_status"],
            "closeout_status": scorecard["summary"]["closeout_status"],
            "projected_terminal_status": scorecard["summary"]["projected_terminal_status"],
            "headline_count": digest["summary"]["headline_count"],
            "handoff_owner": handoff["summary"]["handoff_owner"],
            "remaining_action_count": closeout["summary"]["remaining_action_count"],
        },
        "scorecard": scorecard,
        "digest": {
            "headlines": digest["headlines"],
            "alerts": digest["alerts"],
            "actions": digest["actions"],
        },
        "handoff": {
            "owner_context": handoff["owner_context"],
            "actions": handoff["actions"],
        },
        "closeout": {
            "checks": closeout["closeout_checks"],
            "remaining_actions": closeout["remaining_actions"],
        },
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_packet.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_packet.md").write_text(render_artifact_packet_markdown(payload))
    return payload


def render_artifact_packet_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Packet",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Closeout status: `{payload['summary']['closeout_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Headlines: `{payload['summary']['headline_count']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Remaining actions: `{payload['summary']['remaining_action_count']}`",
        "",
        "## Headlines",
        "",
    ]
    for headline in payload["digest"]["headlines"]:
        lines.append(f"- {headline}")
    lines.extend(["", "## Top Alerts", ""])
    for alert in payload["digest"]["alerts"]:
        lines.append(f"- [{alert['severity']}] {alert['title']}: {alert['message']}")
    lines.extend(["", "## Handoff Owner", ""])
    lines.append(f"- Owner: `{payload['handoff']['owner_context']['owner']}`")
    lines.append(f"- Status: `{payload['handoff']['owner_context']['status']}`")
    lines.append(f"- Command count: `{payload['handoff']['owner_context']['command_count']}`")
    lines.extend(["", "## Closeout Checks", ""])
    for check in payload["closeout"]["checks"]:
        lines.append(f"- {check['name']}: {check['status']} | {check['message']}")
    return "\n".join(lines)
