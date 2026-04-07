import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_alerts import build_dashboard_snapshot_alerts


def test_dashboard_snapshot_alerts_surface_major_transitions(tmp_path):
    drift = tmp_path / "drift.json"
    drift.write_text(
        json.dumps(
            {
                "summary": {"first_pass_snapshot": "recovered"},
                "transitions": [
                    {
                        "from": "baseline",
                        "to": "stabilized",
                        "from_status": "fail",
                        "to_status": "fail",
                        "failure_delta": -4,
                        "risk_delta": -0.5,
                        "status_changed": False,
                    },
                    {
                        "from": "stabilized",
                        "to": "recovered",
                        "from_status": "fail",
                        "to_status": "pass",
                        "failure_delta": -1,
                        "risk_delta": -1.2,
                        "status_changed": True,
                    },
                ],
            }
        )
    )

    payload = build_dashboard_snapshot_alerts(
        dashboard_snapshot_drift_path=drift,
        output_dir=tmp_path,
    )

    assert payload["summary"]["alert_count"] == 4
    assert payload["summary"]["critical_count"] == 1
    assert payload["summary"]["warning_count"] == 2
    assert payload["summary"]["info_count"] == 1
