from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_handoff(
    *,
    dashboard_snapshot_review_path: str | Path,
    dashboard_snapshot_monitor_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    review = _read_json(dashboard_snapshot_review_path)
    monitor = _read_json(dashboard_snapshot_monitor_path)

    owner = "dashboard-ops"
    if review["summary"]["critical_count"] > 0:
        owner = "dashboard-stabilization"
    elif review["summary"]["current_status"] == "pass":
        owner = "dashboard-maintenance"

    top_items: list[str] = []
    if review.get("top_alert"):
        title = review["top_alert"]["title"]
        if title not in top_items:
            top_items.append(title)
    if review["summary"].get("next_focus"):
        focus = review["summary"]["next_focus"]
        if focus not in top_items:
            top_items.append(focus)
    for blocker in review.get("blockers", [])[:2]:
        if blocker not in top_items:
            top_items.append(blocker)

    payload = {
        "summary": {
            "handoff_owner": owner,
            "current_status": review["summary"]["current_status"],
            "projected_terminal_status": review["summary"]["projected_terminal_status"],
            "blocker_count": review["summary"]["blocker_count"],
            "top_item_count": len(top_items),
            "dominant_transition": monitor["summary"]["dominant_transition"],
        },
        "top_items": top_items,
        "headlines": monitor.get("headlines", []),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "handoff.json").write_text(json.dumps(payload, indent=2))
    (output / "handoff.md").write_text(render_dashboard_snapshot_handoff_markdown(payload))
    return payload


def render_dashboard_snapshot_handoff_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Handoff",
        "",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Blockers: `{payload['summary']['blocker_count']}`",
        f"- Top items: `{payload['summary']['top_item_count']}`",
        f"- Dominant transition: `{payload['summary']['dominant_transition']}`",
        "",
        "## Top Items",
        "",
    ]
    for item in payload["top_items"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Headlines", ""])
    for headline in payload["headlines"]:
        lines.append(f"- {headline}")
    return "\n".join(lines)
