import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_review import build_dashboard_snapshot_review


def test_dashboard_snapshot_review_builds_blockers_and_focus(tmp_path):
    monitor = tmp_path / "monitor.json"
    alerts = tmp_path / "alerts.json"

    monitor.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "projected_terminal_status": "pass",
                    "headline_count": 4,
                },
                "headlines": ["Current status is fail."],
                "highest_priority_alert": {
                    "severity": "critical",
                    "title": "Status transition to pass",
                    "message": "Projected state reaches pass.",
                },
            }
        )
    )
    alerts.write_text(
        json.dumps(
            {
                "summary": {
                    "critical_count": 1,
                }
            }
        )
    )

    payload = build_dashboard_snapshot_review(
        dashboard_snapshot_monitor_path=monitor,
        dashboard_snapshot_alerts_path=alerts,
        output_dir=tmp_path,
    )

    assert payload["summary"]["blocker_count"] == 2
    assert payload["summary"]["next_focus"] == "Status transition to pass"
    assert payload["top_alert"]["severity"] == "critical"
