from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_focus(
    *,
    dashboard_snapshot_watchlist_path: str | Path,
    dashboard_snapshot_readiness_gate_path: str | Path,
    dashboard_snapshot_milestones_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    watchlist = _read_json(dashboard_snapshot_watchlist_path)
    readiness_gate = _read_json(dashboard_snapshot_readiness_gate_path)
    milestones = _read_json(dashboard_snapshot_milestones_path)

    focus_items = []
    for item in watchlist.get("watch_items", [])[:3]:
        focus_items.append(
            {
                "label": item["label"],
                "kind": item["kind"],
                "severity": item["severity"],
            }
        )

    payload = {
        "summary": {
            "current_status": readiness_gate["summary"]["current_status"],
            "readiness_status": readiness_gate["summary"]["status"],
            "next_status": milestones["summary"]["projected_next_status"],
            "terminal_status": milestones["summary"]["terminal_status"],
            "focus_item_count": len(focus_items),
            "handoff_owner": watchlist["summary"]["handoff_owner"],
        },
        "focus_items": focus_items,
        "blocking_reasons": readiness_gate.get("failures", [])[:2],
        "next_objective": focus_items[0]["label"] if focus_items else "Maintain dashboard stability",
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "focus.json").write_text(json.dumps(payload, indent=2))
    (output / "focus.md").write_text(render_dashboard_snapshot_focus_markdown(payload))
    return payload


def render_dashboard_snapshot_focus_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Focus",
        "",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Readiness status: `{payload['summary']['readiness_status']}`",
        f"- Next status: `{payload['summary']['next_status']}`",
        f"- Terminal status: `{payload['summary']['terminal_status']}`",
        f"- Focus items: `{payload['summary']['focus_item_count']}`",
        f"- Next objective: `{payload['next_objective']}`",
        "",
    ]
    for reason in payload["blocking_reasons"]:
        lines.append(f"- Blocker: {reason}")
    for item in payload["focus_items"]:
        lines.append(f"- [{item['kind']}] {item['label']} | severity `{item['severity']}`")
    return "\n".join(lines)
