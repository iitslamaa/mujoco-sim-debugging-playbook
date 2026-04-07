from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_execution_board(
    *,
    dashboard_snapshot_resolution_plan_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    resolution_plan = _read_json(dashboard_snapshot_resolution_plan_path)

    lanes = []
    for phase in resolution_plan.get("phases", []):
        status = "active" if phase["priority"] == "P0" else "planned"
        lanes.append(
            {
                "lane": phase["name"],
                "status": status,
                "priority": phase["priority"],
                "item_count": len(phase.get("items", [])),
                "items": list(phase.get("items", [])),
            }
        )

    payload = {
        "summary": {
            "current_status": resolution_plan["summary"]["current_status"],
            "handoff_owner": resolution_plan["summary"]["handoff_owner"],
            "lane_count": len(lanes),
            "active_lane_count": sum(1 for lane in lanes if lane["status"] == "active"),
            "planned_lane_count": sum(1 for lane in lanes if lane["status"] == "planned"),
        },
        "lanes": lanes,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "execution_board.json").write_text(json.dumps(payload, indent=2))
    (output / "execution_board.md").write_text(render_dashboard_snapshot_execution_board_markdown(payload))
    return payload


def render_dashboard_snapshot_execution_board_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Execution Board",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Lanes: `{payload['summary']['lane_count']}`",
        f"- Active lanes: `{payload['summary']['active_lane_count']}`",
        f"- Planned lanes: `{payload['summary']['planned_lane_count']}`",
        "",
    ]
    for lane in payload["lanes"]:
        lines.extend(
            [
                f"## {lane['lane']}",
                "",
                f"- Status: `{lane['status']}`",
                f"- Priority: `{lane['priority']}`",
                f"- Items: `{lane['item_count']}`",
                "",
            ]
        )
        for item in lane["items"]:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).rstrip()
