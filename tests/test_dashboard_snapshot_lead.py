import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_lead import (
    build_dashboard_snapshot_lead,
)


def test_dashboard_snapshot_lead_builds_concise_statement(tmp_path):
    status_brief = tmp_path / "status_brief.json"
    review = tmp_path / "review.json"

    status_brief.write_text(
        json.dumps(
            {
                "summary": {
                    "handoff_owner": "dashboard-stabilization",
                    "current_status": "fail",
                    "next_status": "warn",
                    "projected_terminal_status": "pass",
                    "top_priority": "Status transition to pass",
                    "critical_alerts": 1,
                },
                "headlines": ["Current dashboard status is fail."],
            }
        )
    )
    review.write_text(
        json.dumps(
            {
                "summary": {"next_focus": "Status transition to pass"},
                "blockers": ["Critical snapshot alerts are still active."],
            }
        )
    )

    payload = build_dashboard_snapshot_lead(
        dashboard_snapshot_status_brief_path=status_brief,
        dashboard_snapshot_review_path=review,
        output_dir=tmp_path,
    )

    assert payload["summary"]["next_focus"] == "Status transition to pass"
    assert "dashboard-stabilization" in payload["lead_statement"]
