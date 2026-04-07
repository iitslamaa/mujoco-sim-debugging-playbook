from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_closeout(
    *,
    artifact_review_note_path: str | Path,
    artifact_history_path: str | Path,
    artifact_handoff_path: str | Path,
    artifact_actions_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    review_note = _read_json(artifact_review_note_path)
    history = _read_json(artifact_history_path)
    handoff = _read_json(artifact_handoff_path)
    actions = _read_json(artifact_actions_path)

    ready_to_close = (
        review_note["summary"]["status"] == "pass"
        or (
            review_note["summary"]["blocker_count"] == 0
            and history["summary"]["projected_terminal_status"] == "pass"
        )
    )
    remaining_actions = actions["actions"][:3]

    payload = {
        "summary": {
            "status": "ready_to_close" if ready_to_close else "not_ready_to_close",
            "current_status": review_note["summary"]["status"],
            "projected_terminal_status": history["summary"]["projected_terminal_status"],
            "blocker_count": review_note["summary"]["blocker_count"],
            "remaining_action_count": len(remaining_actions),
            "handoff_owner": handoff["summary"]["handoff_owner"],
        },
        "closeout_checks": [
            {
                "name": "review_blockers",
                "status": "pass" if review_note["summary"]["blocker_count"] == 0 else "fail",
                "message": f"{review_note['summary']['blocker_count']} blockers remain.",
            },
            {
                "name": "projected_terminal_state",
                "status": "pass" if history["summary"]["projected_terminal_status"] == "pass" else "fail",
                "message": f"Projected terminal status is {history['summary']['projected_terminal_status']}.",
            },
            {
                "name": "handoff_alignment",
                "status": "pass" if handoff["summary"]["action_count"] > 0 else "fail",
                "message": f"Handoff includes {handoff['summary']['action_count']} actions.",
            },
        ],
        "remaining_actions": remaining_actions,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_closeout.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_closeout.md").write_text(render_artifact_closeout_markdown(payload))
    return payload


def render_artifact_closeout_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Closeout",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Blockers: `{payload['summary']['blocker_count']}`",
        f"- Remaining actions: `{payload['summary']['remaining_action_count']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        "",
        "## Closeout Checks",
        "",
        "| check | status | message |",
        "| --- | --- | --- |",
    ]
    for check in payload["closeout_checks"]:
        lines.append(f"| {check['name']} | {check['status']} | {check['message']} |")
    lines.extend(["", "## Remaining Actions", ""])
    for action in payload["remaining_actions"]:
        lines.append(f"- {action['priority']} {action['target']} -> {action['owner']}: {action['expected_impact']}")
    return "\n".join(lines)
