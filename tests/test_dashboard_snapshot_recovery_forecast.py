import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_recovery_forecast import (
    build_dashboard_snapshot_recovery_forecast,
)


def test_dashboard_snapshot_recovery_forecast_projects_warn_from_fail(tmp_path):
    readiness_gate = tmp_path / "readiness_gate.json"
    resolution_plan = tmp_path / "resolution_plan.json"

    readiness_gate.write_text(
        json.dumps(
            {
                "summary": {
                    "status": "fail",
                }
            }
        )
    )
    resolution_plan.write_text(
        json.dumps(
            {
                "summary": {
                    "critical_count": 1,
                    "phase_count": 2,
                }
            }
        )
    )

    payload = build_dashboard_snapshot_recovery_forecast(
        dashboard_snapshot_readiness_gate_path=readiness_gate,
        dashboard_snapshot_resolution_plan_path=resolution_plan,
        output_dir=tmp_path,
    )

    assert payload["summary"]["projected_next_status"] == "warn"
