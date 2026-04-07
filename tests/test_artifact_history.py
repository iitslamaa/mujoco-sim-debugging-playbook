import json

from mujoco_sim_debugging_playbook.artifact_history import build_artifact_history


def test_artifact_history_projects_improvement(tmp_path):
    exec_summary = tmp_path / "artifact_exec_summary.json"
    exec_summary.write_text(
        json.dumps({"summary": {"top_risk_score": 1.5}})
    )
    readiness = tmp_path / "artifact_readiness.json"
    readiness.write_text(
        json.dumps({"summary": {"status": "fail", "failure_count": 4}})
    )
    delivery = tmp_path / "artifact_delivery.json"
    delivery.write_text(
        json.dumps({"summary": {"breach_count": 1}})
    )
    capacity = tmp_path / "artifact_capacity.json"
    capacity.write_text(
        json.dumps({"summary": {"overloaded_owner_count": 1}})
    )
    scenarios = tmp_path / "artifact_scenarios.json"
    scenarios.write_text(
        json.dumps(
            {
                "scenarios": [
                    {"name": "Support report sprint", "status": "fail", "failure_count": 1},
                    {"name": "Full artifact refresh", "status": "pass", "failure_count": 0},
                ]
            }
        )
    )

    payload = build_artifact_history(
        artifact_exec_summary_path=exec_summary,
        artifact_readiness_path=readiness,
        artifact_delivery_path=delivery,
        artifact_capacity_path=capacity,
        artifact_scenarios_path=scenarios,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["projected_terminal_status"] == "pass"
    assert payload["summary"]["failure_direction"] == "improving"
