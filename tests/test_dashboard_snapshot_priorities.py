import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_priorities import (
    build_dashboard_snapshot_priorities,
)


def test_dashboard_snapshot_priorities_uses_focus_and_plan(tmp_path):
    focus = tmp_path / "focus.json"
    resolution_plan = tmp_path / "resolution_plan.json"

    focus.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "next_status": "warn",
                    "handoff_owner": "dashboard-stabilization",
                },
                "blocking_reasons": ["Closeout has not reached ready_to_close."],
                "next_objective": "Status transition to pass",
            }
        )
    )
    resolution_plan.write_text(
        json.dumps(
            {
                "phases": [
                    {"name": "Immediate stabilization", "priority": "P0", "items": ["Status transition to pass"]},
                    {"name": "Follow-up cleanup", "priority": "P1", "items": ["Current dashboard status is not yet pass."]},
                ]
            }
        )
    )

    payload = build_dashboard_snapshot_priorities(
        dashboard_snapshot_focus_path=focus,
        dashboard_snapshot_resolution_plan_path=resolution_plan,
        output_dir=tmp_path,
    )

    assert payload["summary"]["priority_count"] == 2
    assert payload["priorities"][0]["priority"] == "P0"
