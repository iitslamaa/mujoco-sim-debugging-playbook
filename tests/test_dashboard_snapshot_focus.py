import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_focus import (
    build_dashboard_snapshot_focus,
)


def test_dashboard_snapshot_focus_summarizes_blockers_and_objective(tmp_path):
    watchlist = tmp_path / "watchlist.json"
    readiness_gate = tmp_path / "readiness_gate.json"
    milestones = tmp_path / "milestones.json"

    watchlist.write_text(
        json.dumps(
            {
                "summary": {"handoff_owner": "dashboard-stabilization"},
                "watch_items": [
                    {"label": "Status transition to pass", "kind": "alert", "severity": "critical"},
                    {"label": "Closeout blockers remain", "kind": "alert", "severity": "warning"},
                ],
            }
        )
    )
    readiness_gate.write_text(
        json.dumps(
            {
                "summary": {"current_status": "fail", "status": "fail"},
                "failures": ["Closeout has not reached ready_to_close."],
            }
        )
    )
    milestones.write_text(
        json.dumps(
            {
                "summary": {"projected_next_status": "warn", "terminal_status": "pass"},
            }
        )
    )

    payload = build_dashboard_snapshot_focus(
        dashboard_snapshot_watchlist_path=watchlist,
        dashboard_snapshot_readiness_gate_path=readiness_gate,
        dashboard_snapshot_milestones_path=milestones,
        output_dir=tmp_path,
    )

    assert payload["summary"]["focus_item_count"] == 2
    assert payload["next_objective"] == "Status transition to pass"
