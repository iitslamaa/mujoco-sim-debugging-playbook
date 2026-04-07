import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_resolution_plan import (
    build_dashboard_snapshot_resolution_plan,
)


def test_dashboard_snapshot_resolution_plan_groups_actions_by_priority(tmp_path):
    alert_packet = tmp_path / "alert_packet.json"
    actions = tmp_path / "actions.json"
    alert_packet.write_text(
        json.dumps(
            {
                "summary": {
                    "alert_count": 3,
                    "critical_count": 1,
                }
            }
        )
    )
    actions.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "handoff_owner": "dashboard-stabilization",
                },
                "actions": [
                    {"priority": "P0", "title": "Status transition to pass"},
                    {"priority": "P1", "title": "Clear warning backlog"},
                ],
            }
        )
    )

    payload = build_dashboard_snapshot_resolution_plan(
        dashboard_snapshot_alert_packet_path=alert_packet,
        dashboard_snapshot_actions_path=actions,
        output_dir=tmp_path,
    )

    assert payload["summary"]["phase_count"] == 2
    assert payload["phases"][0]["name"] == "Immediate stabilization"
