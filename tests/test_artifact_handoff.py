import json

from mujoco_sim_debugging_playbook.artifact_handoff import build_artifact_handoff


def test_artifact_handoff_includes_owner_context(tmp_path):
    digest = tmp_path / "artifact_digest.json"
    digest.write_text(json.dumps({"headlines": ["a", "b", "c"]}))
    actions = tmp_path / "artifact_actions.json"
    actions.write_text(json.dumps({"actions": [{"priority": "P0", "target": "x", "owner": "y", "expected_impact": "z"}]}))
    alerts = tmp_path / "artifact_alerts.json"
    alerts.write_text(json.dumps({"summary": {"critical_count": 1}, "alerts": [{"severity": "critical", "title": "A", "message": "B"}]}))
    capacity = tmp_path / "artifact_capacity.json"
    capacity.write_text(json.dumps({"owners": [{"owner": "owner-a", "command_count": 4, "phase_count": 1, "status": "overloaded"}]}))
    exec_summary = tmp_path / "artifact_exec_summary.json"
    exec_summary.write_text(json.dumps({"summary": {"status": "fail", "top_risk_artifact": "x", "breach_phase": "phase", "overloaded_owner": "owner-a"}}))

    payload = build_artifact_handoff(
        artifact_digest_path=digest,
        artifact_actions_path=actions,
        artifact_alerts_path=alerts,
        artifact_capacity_path=capacity,
        artifact_exec_summary_path=exec_summary,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["handoff_owner"] == "owner-a"
    assert payload["owner_context"]["status"] == "overloaded"
