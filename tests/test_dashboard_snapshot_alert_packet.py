import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_alert_packet import build_dashboard_snapshot_alert_packet


def test_dashboard_snapshot_alert_packet_maps_actions_to_alerts(tmp_path):
    actions = tmp_path / "actions.json"
    actions.write_text(
        json.dumps(
            {
                "summary": {
                    "handoff_owner": "dashboard-stabilization",
                    "current_status": "fail",
                },
                "actions": [
                    {
                        "priority": "P0",
                        "title": "Status transition to pass",
                        "owner": "dashboard-stabilization",
                    },
                    {
                        "priority": "P1",
                        "title": "Critical snapshot alerts are still active.",
                        "owner": "dashboard-stabilization",
                    },
                ],
            }
        )
    )

    payload = build_dashboard_snapshot_alert_packet(
        dashboard_snapshot_actions_path=actions,
        output_dir=tmp_path,
    )

    assert payload["summary"]["alert_count"] == 2
    assert payload["summary"]["critical_count"] == 1
    assert payload["summary"]["warning_count"] == 1
