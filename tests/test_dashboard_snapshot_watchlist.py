import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_watchlist import (
    build_dashboard_snapshot_watchlist,
)


def test_dashboard_snapshot_watchlist_prioritizes_alerts_and_actions(tmp_path):
    alert_packet = tmp_path / "alert_packet.json"
    actions = tmp_path / "actions.json"
    owner_load = tmp_path / "owner_load.json"

    alert_packet.write_text(
        json.dumps(
            {
                "summary": {"critical_alerts": 1, "handoff_owner": "dashboard-stabilization"},
                "alerts": [
                    {"title": "Status transition to pass", "severity": "critical"},
                    {"title": "Closeout blockers remain", "severity": "warning"},
                ],
            }
        )
    )
    actions.write_text(
        json.dumps(
            {
                "summary": {"handoff_owner": "dashboard-stabilization"},
                "actions": [
                    {"label": "Clear critical blocker", "priority": "P0"},
                    {"label": "Reduce warning backlog", "priority": "P1"},
                ],
            }
        )
    )
    owner_load.write_text(
        json.dumps(
            {
                "summary": {
                    "owner": "dashboard-stabilization",
                    "active_items": 1,
                    "planned_items": 2,
                }
            }
        )
    )

    payload = build_dashboard_snapshot_watchlist(
        dashboard_snapshot_alert_packet_path=alert_packet,
        dashboard_snapshot_actions_path=actions,
        dashboard_snapshot_owner_load_path=owner_load,
        output_dir=tmp_path,
    )

    assert payload["summary"]["watch_item_count"] == 4
    assert payload["watch_items"][0]["kind"] == "alert"
    assert payload["watch_items"][2]["severity"] == "p0"
