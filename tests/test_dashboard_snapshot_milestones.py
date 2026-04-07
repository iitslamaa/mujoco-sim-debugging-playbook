import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_milestones import (
    build_dashboard_snapshot_milestones,
)


def test_dashboard_snapshot_milestones_tracks_state_progression(tmp_path):
    recovery_forecast = tmp_path / "recovery_forecast.json"
    scorecard = tmp_path / "scorecard.json"

    recovery_forecast.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "projected_next_status": "warn",
                    "confidence": "medium",
                }
            }
        )
    )
    scorecard.write_text(
        json.dumps(
            {
                "summary": {
                    "projected_terminal_status": "pass",
                }
            }
        )
    )

    payload = build_dashboard_snapshot_milestones(
        dashboard_snapshot_recovery_forecast_path=recovery_forecast,
        dashboard_snapshot_scorecard_path=scorecard,
        output_dir=tmp_path,
    )

    assert payload["summary"]["milestone_count"] == 3
    assert payload["milestones"][1]["status"] == "warn"
