import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_closeout import build_dashboard_snapshot_closeout


def test_dashboard_snapshot_closeout_marks_not_ready_when_blocked(tmp_path):
    handoff = tmp_path / "handoff.json"
    review = tmp_path / "review.json"

    handoff.write_text(
        json.dumps(
            {
                "summary": {
                    "handoff_owner": "dashboard-stabilization",
                },
                "top_items": ["Status transition to pass", "Critical snapshot alerts are still active."],
            }
        )
    )
    review.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "projected_terminal_status": "pass",
                    "critical_count": 1,
                    "blocker_count": 2,
                },
                "blockers": ["Current dashboard status is not yet pass."],
            }
        )
    )

    payload = build_dashboard_snapshot_closeout(
        dashboard_snapshot_handoff_path=handoff,
        dashboard_snapshot_review_path=review,
        output_dir=tmp_path,
    )

    assert payload["summary"]["closeout_status"] == "not_ready_to_close"
    assert payload["summary"]["remaining_item_count"] == 2
