from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_closeout(
    *,
    dashboard_snapshot_handoff_path: str | Path,
    dashboard_snapshot_review_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    handoff = _read_json(dashboard_snapshot_handoff_path)
    review = _read_json(dashboard_snapshot_review_path)

    ready_to_close = (
        review["summary"]["current_status"] == "pass"
        and review["summary"]["critical_count"] == 0
        and review["summary"]["blocker_count"] == 0
    )

    remaining_items = list(handoff.get("top_items", []))
    if ready_to_close:
        remaining_items = []

    payload = {
        "summary": {
            "closeout_status": "ready_to_close" if ready_to_close else "not_ready_to_close",
            "handoff_owner": handoff["summary"]["handoff_owner"],
            "current_status": review["summary"]["current_status"],
            "projected_terminal_status": review["summary"]["projected_terminal_status"],
            "remaining_item_count": len(remaining_items),
            "blocker_count": review["summary"]["blocker_count"],
        },
        "remaining_items": remaining_items,
        "blockers": review.get("blockers", []),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "closeout.json").write_text(json.dumps(payload, indent=2))
    (output / "closeout.md").write_text(render_dashboard_snapshot_closeout_markdown(payload))
    return payload


def render_dashboard_snapshot_closeout_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Closeout",
        "",
        f"- Closeout status: `{payload['summary']['closeout_status']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Remaining items: `{payload['summary']['remaining_item_count']}`",
        f"- Blockers: `{payload['summary']['blocker_count']}`",
        "",
        "## Remaining Items",
        "",
    ]
    if payload["remaining_items"]:
        for item in payload["remaining_items"]:
            lines.append(f"- {item}")
    else:
        lines.append("- None")
    lines.extend(["", "## Blockers", ""])
    if payload["blockers"]:
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    else:
        lines.append("- None")
    return "\n".join(lines)
