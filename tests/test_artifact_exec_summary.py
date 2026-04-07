import json

from mujoco_sim_debugging_playbook.artifact_exec_summary import build_artifact_exec_summary


def test_artifact_exec_summary_surfaces_top_risk_and_owner(tmp_path):
    readiness = tmp_path / "artifact_readiness.json"
    readiness.write_text(json.dumps({"summary": {"status": "fail", "failure_count": 3, "warning_count": 0}}))
    maintenance = tmp_path / "maintenance_risk.json"
    maintenance.write_text(
        json.dumps(
            {
                "rows": [
                    {"artifact": "a", "risk_score": 1.7},
                ]
            }
        )
    )
    delivery = tmp_path / "artifact_delivery.json"
    delivery.write_text(
        json.dumps({"phases": [{"name": "Phase A", "status": "breach", "due_date": "2026-04-10"}]})
    )
    capacity = tmp_path / "artifact_capacity.json"
    capacity.write_text(
        json.dumps(
            {
                "owners": [{"owner": "artifact-reporting", "status": "overloaded", "command_count": 5}],
                "summary": {"highest_pressure_phase": "Phase A"},
                "rebalance_items": [{"artifact": "a", "phase": "Phase A", "recommended_owner": "artifact-integrity", "reason": "move it"}],
            }
        )
    )

    payload = build_artifact_exec_summary(
        artifact_readiness_path=readiness,
        maintenance_risk_path=maintenance,
        artifact_delivery_path=delivery,
        artifact_capacity_path=capacity,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["top_risk_artifact"] == "a"
    assert payload["summary"]["overloaded_owner"] == "artifact-reporting"
