from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_owner_load(
    *,
    dashboard_snapshot_execution_board_path: str | Path,
    dashboard_snapshot_alert_packet_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    execution_board = _read_json(dashboard_snapshot_execution_board_path)
    alert_packet = _read_json(dashboard_snapshot_alert_packet_path)

    owner = execution_board["summary"]["handoff_owner"]
    active_items = sum(
        lane["item_count"] for lane in execution_board.get("lanes", []) if lane["status"] == "active"
    )
    planned_items = sum(
        lane["item_count"] for lane in execution_board.get("lanes", []) if lane["status"] == "planned"
    )

    payload = {
        "summary": {
            "owner": owner,
            "current_status": execution_board["summary"]["current_status"],
            "active_lane_count": execution_board["summary"]["active_lane_count"],
            "planned_lane_count": execution_board["summary"]["planned_lane_count"],
            "active_item_count": active_items,
            "planned_item_count": planned_items,
            "critical_alert_count": alert_packet["summary"]["critical_count"],
            "warning_alert_count": alert_packet["summary"]["warning_count"],
        }
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "owner_load.json").write_text(json.dumps(payload, indent=2))
    (output / "owner_load.md").write_text(render_dashboard_snapshot_owner_load_markdown(payload))
    return payload


def render_dashboard_snapshot_owner_load_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Dashboard Snapshot Owner Load",
        "",
        f"- Owner: `{summary['owner']}`",
        f"- Current status: `{summary['current_status']}`",
        f"- Active lanes: `{summary['active_lane_count']}`",
        f"- Planned lanes: `{summary['planned_lane_count']}`",
        f"- Active items: `{summary['active_item_count']}`",
        f"- Planned items: `{summary['planned_item_count']}`",
        f"- Critical alerts: `{summary['critical_alert_count']}`",
        f"- Warning alerts: `{summary['warning_alert_count']}`",
    ]
    return "\n".join(lines)
