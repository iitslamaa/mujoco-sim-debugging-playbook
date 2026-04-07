import json

from mujoco_sim_debugging_playbook.artifact_actions import build_artifact_actions


def test_artifact_actions_prioritize_rebalance_items(tmp_path):
    exec_summary = tmp_path / "artifact_exec_summary.json"
    exec_summary.write_text(json.dumps({"summary": {"status": "fail", "top_risk_artifact": "a"}}))
    delivery = tmp_path / "artifact_delivery.json"
    delivery.write_text(json.dumps({"summary": {"next_due_phase": "Phase A"}}))
    capacity = tmp_path / "artifact_capacity.json"
    capacity.write_text(
        json.dumps(
            {
                "rebalance_items": [
                    {"artifact": "a", "recommended_owner": "owner-a", "phase": "Phase A", "reason": "move it"},
                ]
            }
        )
    )
    history = tmp_path / "artifact_history.json"
    history.write_text(json.dumps({"summary": {"projected_terminal_status": "pass"}}))

    payload = build_artifact_actions(
        artifact_exec_summary_path=exec_summary,
        artifact_delivery_path=delivery,
        artifact_capacity_path=capacity,
        artifact_history_path=history,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["action_count"] >= 3
    assert payload["actions"][0]["priority"] == "P0"
