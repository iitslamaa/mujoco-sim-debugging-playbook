import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_owner_load import (
    build_dashboard_snapshot_owner_load,
)


def test_dashboard_snapshot_owner_load_summarizes_items_and_alerts(tmp_path):
    execution_board = tmp_path / "execution_board.json"
    alert_packet = tmp_path / "alert_packet.json"

    execution_board.write_text(
        json.dumps(
            {
                "summary": {
                    "handoff_owner": "dashboard-stabilization",
                    "current_status": "fail",
                    "active_lane_count": 1,
                    "planned_lane_count": 1,
                },
                "lanes": [
                    {"status": "active", "item_count": 1},
                    {"status": "planned", "item_count": 2},
                ],
            }
        )
    )
    alert_packet.write_text(
        json.dumps(
            {
                "summary": {
                    "critical_count": 1,
                    "warning_count": 2,
                }
            }
        )
    )

    payload = build_dashboard_snapshot_owner_load(
        dashboard_snapshot_execution_board_path=execution_board,
        dashboard_snapshot_alert_packet_path=alert_packet,
        output_dir=tmp_path,
    )

    assert payload["summary"]["active_item_count"] == 1
    assert payload["summary"]["planned_item_count"] == 2
    assert payload["summary"]["critical_alert_count"] == 1
