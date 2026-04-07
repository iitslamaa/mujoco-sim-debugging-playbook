import json

from mujoco_sim_debugging_playbook.artifact_digest import build_artifact_digest


def test_artifact_digest_collects_headlines_and_actions(tmp_path):
    alerts = tmp_path / "artifact_alerts.json"
    alerts.write_text(json.dumps({"summary": {"critical_count": 1}, "alerts": [{"severity": "critical", "title": "A", "message": "B"}]}))
    actions = tmp_path / "artifact_actions.json"
    actions.write_text(json.dumps({"summary": {"action_count": 2}, "actions": [{"priority": "P0", "target": "x", "owner": "y", "expected_impact": "z"}]}))
    history = tmp_path / "artifact_history.json"
    history.write_text(json.dumps({"summary": {"status_direction": "improving", "projected_terminal_status": "pass"}}))
    exec_summary = tmp_path / "artifact_exec_summary.json"
    exec_summary.write_text(json.dumps({"summary": {"status": "fail", "failure_count": 2, "top_risk_artifact": "a", "top_risk_score": 1.2}}))

    payload = build_artifact_digest(
        artifact_alerts_path=alerts,
        artifact_actions_path=actions,
        artifact_history_path=history,
        artifact_exec_summary_path=exec_summary,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["headline_count"] == 3
    assert payload["summary"]["projected_terminal_status"] == "pass"
