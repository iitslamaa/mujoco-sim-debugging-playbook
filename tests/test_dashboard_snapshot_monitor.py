import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_monitor import build_dashboard_snapshot_monitor


def test_dashboard_snapshot_monitor_summarizes_timeline_state(tmp_path):
    history = tmp_path / "history.json"
    drift = tmp_path / "drift.json"
    alerts = tmp_path / "alerts.json"

    history.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "projected_terminal_status": "pass",
                }
            }
        )
    )
    drift.write_text(
        json.dumps(
            {
                "summary": {
                    "largest_failure_drop_transition": "current -> projected",
                    "first_pass_snapshot": "projected",
                }
            }
        )
    )
    alerts.write_text(
        json.dumps(
            {
                "summary": {
                    "alert_count": 2,
                    "critical_count": 1,
                },
                "alerts": [
                    {
                        "severity": "critical",
                        "title": "Status transition to pass",
                        "message": "projected reaches pass",
                    }
                ],
            }
        )
    )

    payload = build_dashboard_snapshot_monitor(
        dashboard_snapshot_history_path=history,
        dashboard_snapshot_drift_path=drift,
        dashboard_snapshot_alerts_path=alerts,
        output_dir=tmp_path,
    )

    assert payload["summary"]["headline_count"] == 4
    assert payload["summary"]["dominant_transition"] == "current -> projected"
    assert payload["highest_priority_alert"]["severity"] == "critical"
