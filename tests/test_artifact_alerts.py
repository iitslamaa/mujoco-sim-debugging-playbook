import json

from mujoco_sim_debugging_playbook.artifact_alerts import build_artifact_alerts


def test_artifact_alerts_include_critical_and_info(tmp_path):
    actions = tmp_path / "artifact_actions.json"
    actions.write_text(
        json.dumps(
            {
                "actions": [
                    {"priority": "P0", "owner": "owner-a", "target": "a", "phase": "Phase A"},
                    {"priority": "P1", "owner": "owner-b", "target": "b", "phase": "Phase B"},
                ]
            }
        )
    )
    exec_summary = tmp_path / "artifact_exec_summary.json"
    exec_summary.write_text(json.dumps({"summary": {"status": "fail", "failure_count": 2}}))
    delivery = tmp_path / "artifact_delivery.json"
    delivery.write_text(json.dumps({"phases": [{"status": "breach", "name": "Phase A", "due_date": "2026-04-10"}]}))
    capacity = tmp_path / "artifact_capacity.json"
    capacity.write_text(json.dumps({"owners": [{"owner": "owner-a", "status": "overloaded", "command_count": 4}]}))

    payload = build_artifact_alerts(
        artifact_actions_path=actions,
        artifact_exec_summary_path=exec_summary,
        artifact_delivery_path=delivery,
        artifact_capacity_path=capacity,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["critical_count"] >= 1
    assert payload["summary"]["info_count"] >= 1
