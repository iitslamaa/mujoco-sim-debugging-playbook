from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_actions(
    *,
    dashboard_snapshot_digest_path: str | Path,
    dashboard_snapshot_closeout_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    digest = _read_json(dashboard_snapshot_digest_path)
    closeout = _read_json(dashboard_snapshot_closeout_path)

    actions: list[dict[str, Any]] = []

    for index, item in enumerate(closeout.get("remaining_items", [])):
        priority = "P0" if index == 0 else "P1"
        actions.append(
            {
                "priority": priority,
                "title": item,
                "owner": digest["summary"]["handoff_owner"],
            }
        )

    payload = {
        "summary": {
            "action_count": len(actions),
            "current_status": digest["summary"]["current_status"],
            "closeout_status": digest["summary"]["closeout_status"],
            "handoff_owner": digest["summary"]["handoff_owner"],
        },
        "actions": actions,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "actions.json").write_text(json.dumps(payload, indent=2))
    (output / "actions.md").write_text(render_dashboard_snapshot_actions_markdown(payload))
    return payload


def render_dashboard_snapshot_actions_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Actions",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Closeout status: `{payload['summary']['closeout_status']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Actions: `{payload['summary']['action_count']}`",
        "",
    ]
    for action in payload["actions"]:
        lines.append(
            f"- [{action['priority']}] {action['title']} "
            f"(owner: `{action['owner']}`)"
        )
    return "\n".join(lines)
