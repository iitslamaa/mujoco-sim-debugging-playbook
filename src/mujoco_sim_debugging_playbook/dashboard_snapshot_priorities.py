from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_priorities(
    *,
    dashboard_snapshot_focus_path: str | Path,
    dashboard_snapshot_resolution_plan_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    focus = _read_json(dashboard_snapshot_focus_path)
    resolution_plan = _read_json(dashboard_snapshot_resolution_plan_path)

    priorities = []
    for phase in resolution_plan.get("phases", [])[:2]:
        first_item = phase.get("items", ["Maintain dashboard stability"])[0]
        priorities.append(
            {
                "priority": phase["priority"],
                "phase": phase["name"],
                "objective": first_item,
            }
        )

    payload = {
        "summary": {
            "current_status": focus["summary"]["current_status"],
            "next_status": focus["summary"]["next_status"],
            "priority_count": len(priorities),
            "handoff_owner": focus["summary"]["handoff_owner"],
            "next_objective": focus["next_objective"],
        },
        "priorities": priorities,
        "blockers": focus.get("blocking_reasons", [])[:2],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "priorities.json").write_text(json.dumps(payload, indent=2))
    (output / "priorities.md").write_text(render_dashboard_snapshot_priorities_markdown(payload))
    return payload


def render_dashboard_snapshot_priorities_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Priorities",
        "",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Next status: `{payload['summary']['next_status']}`",
        f"- Priorities: `{payload['summary']['priority_count']}`",
        f"- Next objective: `{payload['summary']['next_objective']}`",
        "",
    ]
    for blocker in payload["blockers"]:
        lines.append(f"- Blocker: {blocker}")
    for item in payload["priorities"]:
        lines.append(
            f"- {item['priority']} | {item['phase']} | objective `{item['objective']}`"
        )
    return "\n".join(lines)
