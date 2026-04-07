from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_watchlist(
    *,
    dashboard_snapshot_alert_packet_path: str | Path,
    dashboard_snapshot_actions_path: str | Path,
    dashboard_snapshot_owner_load_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    alert_packet = _read_json(dashboard_snapshot_alert_packet_path)
    actions = _read_json(dashboard_snapshot_actions_path)
    owner_load = _read_json(dashboard_snapshot_owner_load_path)

    watch_items: list[dict[str, Any]] = []

    for alert in alert_packet.get("alerts", [])[:2]:
        watch_items.append(
            {
                "kind": "alert",
                "label": alert["title"],
                "severity": alert["severity"],
                "owner": alert_packet["summary"]["handoff_owner"],
            }
        )

    for action in actions.get("actions", [])[:2]:
        watch_items.append(
            {
                "kind": "action",
                "label": action.get("label", action.get("title", "unnamed action")),
                "severity": action["priority"].lower(),
                "owner": action.get("owner", actions["summary"]["handoff_owner"]),
            }
        )

    payload = {
        "summary": {
            "watch_item_count": len(watch_items),
            "critical_alerts": alert_packet["summary"].get(
                "critical_alerts",
                alert_packet["summary"].get("critical_count", 0),
            ),
            "active_items": owner_load["summary"].get(
                "active_items",
                owner_load["summary"].get("active_item_count", 0),
            ),
            "planned_items": owner_load["summary"].get(
                "planned_items",
                owner_load["summary"].get("planned_item_count", 0),
            ),
            "handoff_owner": owner_load["summary"]["owner"],
        },
        "watch_items": watch_items,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "watchlist.json").write_text(json.dumps(payload, indent=2))
    (output / "watchlist.md").write_text(render_dashboard_snapshot_watchlist_markdown(payload))
    return payload


def render_dashboard_snapshot_watchlist_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Watchlist",
        "",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Watch items: `{payload['summary']['watch_item_count']}`",
        f"- Critical alerts: `{payload['summary']['critical_alerts']}`",
        f"- Active items: `{payload['summary']['active_items']}`",
        f"- Planned items: `{payload['summary']['planned_items']}`",
        "",
    ]
    for item in payload["watch_items"]:
        lines.append(
            f"- [{item['kind']}] {item['label']} | severity `{item['severity']}` | owner `{item['owner']}`"
        )
    return "\n".join(lines)
