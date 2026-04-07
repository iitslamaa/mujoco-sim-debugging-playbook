import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_execution_board import (
    build_dashboard_snapshot_execution_board,
)


def test_dashboard_snapshot_execution_board_builds_lane_view(tmp_path):
    resolution_plan = tmp_path / "resolution_plan.json"
    resolution_plan.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "handoff_owner": "dashboard-stabilization",
                },
                "phases": [
                    {"name": "Immediate stabilization", "priority": "P0", "items": ["Fix pass transition"]},
                    {"name": "Follow-up cleanup", "priority": "P1", "items": ["Clear warnings"]},
                ],
            }
        )
    )

    payload = build_dashboard_snapshot_execution_board(
        dashboard_snapshot_resolution_plan_path=resolution_plan,
        output_dir=tmp_path,
    )

    assert payload["summary"]["lane_count"] == 2
    assert payload["summary"]["active_lane_count"] == 1
    assert payload["lanes"][0]["status"] == "active"
