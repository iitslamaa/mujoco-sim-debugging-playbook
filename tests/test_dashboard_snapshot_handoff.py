import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_handoff import build_dashboard_snapshot_handoff


def test_dashboard_snapshot_handoff_assigns_owner_and_items(tmp_path):
    review = tmp_path / "review.json"
    monitor = tmp_path / "monitor.json"

    review.write_text(
        json.dumps(
            {
                "summary": {
                    "critical_count": 1,
                    "current_status": "fail",
                    "projected_terminal_status": "pass",
                    "blocker_count": 2,
                    "next_focus": "Status transition to pass",
                },
                "top_alert": {
                    "title": "Status transition to pass",
                },
                "blockers": ["Current dashboard status is not yet pass."],
            }
        )
    )
    monitor.write_text(
        json.dumps(
            {
                "summary": {
                    "dominant_transition": "current -> recovery",
                },
                "headlines": ["Largest recovery step is current -> recovery."],
            }
        )
    )

    payload = build_dashboard_snapshot_handoff(
        dashboard_snapshot_review_path=review,
        dashboard_snapshot_monitor_path=monitor,
        output_dir=tmp_path,
    )

    assert payload["summary"]["handoff_owner"] == "dashboard-stabilization"
    assert payload["summary"]["top_item_count"] >= 2
    assert payload["summary"]["dominant_transition"] == "current -> recovery"
