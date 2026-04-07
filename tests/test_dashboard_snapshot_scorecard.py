import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_scorecard import build_dashboard_snapshot_scorecard


def test_dashboard_snapshot_scorecard_collects_kpis(tmp_path):
    monitor = tmp_path / "monitor.json"
    handoff = tmp_path / "handoff.json"
    closeout = tmp_path / "closeout.json"

    monitor.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "projected_terminal_status": "pass",
                    "headline_count": 4,
                    "alert_count": 4,
                    "critical_count": 1,
                    "dominant_transition": "current -> recovery",
                }
            }
        )
    )
    handoff.write_text(
        json.dumps(
            {
                "summary": {
                    "handoff_owner": "dashboard-stabilization",
                }
            }
        )
    )
    closeout.write_text(
        json.dumps(
            {
                "summary": {
                    "closeout_status": "not_ready_to_close",
                    "blocker_count": 2,
                    "remaining_item_count": 3,
                }
            }
        )
    )

    payload = build_dashboard_snapshot_scorecard(
        dashboard_snapshot_monitor_path=monitor,
        dashboard_snapshot_handoff_path=handoff,
        dashboard_snapshot_closeout_path=closeout,
        output_dir=tmp_path,
    )

    assert payload["summary"]["critical_count"] == 1
    assert payload["summary"]["handoff_owner"] == "dashboard-stabilization"
    assert payload["summary"]["remaining_item_count"] == 3
