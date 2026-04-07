import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_actions import build_dashboard_snapshot_actions


def test_dashboard_snapshot_actions_prioritize_remaining_items(tmp_path):
    digest = tmp_path / "digest.json"
    closeout = tmp_path / "closeout.json"

    digest.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "closeout_status": "not_ready_to_close",
                    "handoff_owner": "dashboard-stabilization",
                }
            }
        )
    )
    closeout.write_text(
        json.dumps(
            {
                "remaining_items": [
                    "Status transition to pass",
                    "Critical snapshot alerts are still active.",
                ]
            }
        )
    )

    payload = build_dashboard_snapshot_actions(
        dashboard_snapshot_digest_path=digest,
        dashboard_snapshot_closeout_path=closeout,
        output_dir=tmp_path,
    )

    assert payload["summary"]["action_count"] == 2
    assert payload["actions"][0]["priority"] == "P0"
    assert payload["actions"][1]["priority"] == "P1"
