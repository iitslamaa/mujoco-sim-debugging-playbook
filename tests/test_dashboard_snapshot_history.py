import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_history import build_dashboard_snapshot_history


def test_dashboard_snapshot_history_builds_rows(tmp_path):
    snapshot = tmp_path / "latest.json"
    snapshot.write_text(
        json.dumps(
            {
                "artifact_summary": {"current_status": "fail"},
                "baseline_success_rate": 0.1,
            }
        )
    )
    artifact_history = tmp_path / "artifact_history.json"
    artifact_history.write_text(
        json.dumps(
            {
                "summary": {
                    "status_direction": "improving",
                    "projected_terminal_status": "pass",
                },
                "snapshots": [
                    {"name": "a", "date": "2026-04-01", "status": "fail", "failure_count": 2, "top_risk_score": 1.2},
                    {"name": "b", "date": "2026-04-02", "status": "pass", "failure_count": 0, "top_risk_score": 0.0},
                ],
            }
        )
    )

    payload = build_dashboard_snapshot_history(
        dashboard_snapshot_path=snapshot,
        artifact_history_path=artifact_history,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["snapshot_count"] == 2
    assert payload["snapshots"][0]["baseline_success_rate"] == 0.1
