import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_status_brief import (
    build_dashboard_snapshot_status_brief,
)


def test_dashboard_snapshot_status_brief_combines_priority_and_monitor(tmp_path):
    priorities = tmp_path / "priorities.json"
    monitor = tmp_path / "monitor.json"

    priorities.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "next_status": "warn",
                    "handoff_owner": "dashboard-stabilization",
                },
                "priorities": [{"objective": "Status transition to pass"}],
                "blockers": ["Closeout has not reached ready_to_close."],
            }
        )
    )
    monitor.write_text(
        json.dumps(
            {
                "summary": {
                    "projected_terminal_status": "pass",
                    "critical_count": 1,
                },
                "headlines": ["Current dashboard status is fail."],
            }
        )
    )

    payload = build_dashboard_snapshot_status_brief(
        dashboard_snapshot_priorities_path=priorities,
        dashboard_snapshot_monitor_path=monitor,
        output_dir=tmp_path,
    )

    assert payload["summary"]["top_priority"] == "Status transition to pass"
    assert payload["summary"]["critical_alerts"] == 1
