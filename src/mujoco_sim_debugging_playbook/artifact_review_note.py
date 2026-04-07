from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_review_note(
    *,
    artifact_handoff_path: str | Path,
    artifact_digest_path: str | Path,
    artifact_history_path: str | Path,
    artifact_actions_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    handoff = _read_json(artifact_handoff_path)
    digest = _read_json(artifact_digest_path)
    history = _read_json(artifact_history_path)
    actions = _read_json(artifact_actions_path)

    changed = [
        digest["headlines"][0],
        digest["headlines"][2],
    ]
    blockers = [
        alert["message"]
        for alert in handoff["alerts"]
        if alert["severity"] in {"critical", "warning"}
    ][:3]
    approvals = [
        f"{action['priority']} {action['target']} -> {action['owner']}"
        for action in actions["actions"][:3]
    ]

    payload = {
        "summary": {
            "status": handoff["summary"]["status"],
            "projected_terminal_status": history["summary"]["projected_terminal_status"],
            "changed_count": len(changed),
            "blocker_count": len(blockers),
            "approval_count": len(approvals),
        },
        "changed": changed,
        "blockers": blockers,
        "approvals": approvals,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_review_note.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_review_note.md").write_text(render_artifact_review_note_markdown(payload))
    return payload


def render_artifact_review_note_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Review Note",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Changed items: `{payload['summary']['changed_count']}`",
        f"- Blockers: `{payload['summary']['blocker_count']}`",
        f"- Approval items: `{payload['summary']['approval_count']}`",
        "",
        "## What Changed",
        "",
    ]
    for item in payload["changed"]:
        lines.append(f"- {item}")
    lines.extend(["", "## What Still Blocks", ""])
    for item in payload["blockers"]:
        lines.append(f"- {item}")
    lines.extend(["", "## What To Approve Next", ""])
    for item in payload["approvals"]:
        lines.append(f"- {item}")
    return "\n".join(lines)
