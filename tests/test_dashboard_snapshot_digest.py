import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_digest import build_dashboard_snapshot_digest


def test_dashboard_snapshot_digest_collects_attention_points(tmp_path):
    scorecard = tmp_path / "scorecard.json"
    closeout = tmp_path / "closeout.json"

    scorecard.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "projected_terminal_status": "pass",
                    "closeout_status": "not_ready_to_close",
                    "handoff_owner": "dashboard-stabilization",
                    "critical_count": 1,
                    "blocker_count": 2,
                    "remaining_item_count": 3,
                }
            }
        )
    )
    closeout.write_text(
        json.dumps(
            {
                "remaining_items": ["Status transition to pass"],
            }
        )
    )

    payload = build_dashboard_snapshot_digest(
        dashboard_snapshot_scorecard_path=scorecard,
        dashboard_snapshot_closeout_path=closeout,
        output_dir=tmp_path,
    )

    assert payload["summary"]["attention_count"] == 3
    assert payload["summary"]["handoff_owner"] == "dashboard-stabilization"
