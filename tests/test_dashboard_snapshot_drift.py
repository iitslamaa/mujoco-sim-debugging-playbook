import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_drift import build_dashboard_snapshot_drift


def test_dashboard_snapshot_drift_detects_key_transitions(tmp_path):
    history = tmp_path / "history.json"
    history.write_text(
        json.dumps(
            {
                "snapshots": [
                    {
                        "name": "baseline",
                        "date": "2026-03-30",
                        "status": "fail",
                        "failure_count": 6,
                        "top_risk_score": 1.7,
                        "baseline_success_rate": 0.1,
                    },
                    {
                        "name": "stabilized",
                        "date": "2026-04-06",
                        "status": "fail",
                        "failure_count": 2,
                        "top_risk_score": 1.2,
                        "baseline_success_rate": 0.1,
                    },
                    {
                        "name": "recovered",
                        "date": "2026-04-10",
                        "status": "pass",
                        "failure_count": 0,
                        "top_risk_score": 0.0,
                        "baseline_success_rate": 0.1,
                    },
                ]
            }
        )
    )

    payload = build_dashboard_snapshot_drift(
        dashboard_snapshot_history_path=history,
        output_dir=tmp_path,
    )

    assert payload["summary"]["transition_count"] == 2
    assert payload["summary"]["first_pass_snapshot"] == "recovered"
    assert payload["summary"]["largest_failure_drop_transition"] == "baseline -> stabilized"
    assert payload["summary"]["largest_risk_drop_transition"] == "stabilized -> recovered"
