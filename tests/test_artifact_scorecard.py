import json

from mujoco_sim_debugging_playbook.artifact_scorecard import build_artifact_scorecard


def test_artifact_scorecard_collects_key_metrics(tmp_path):
    closeout = tmp_path / "artifact_closeout.json"
    closeout.write_text(json.dumps({"summary": {"current_status": "fail", "status": "not_ready_to_close", "projected_terminal_status": "pass", "remaining_action_count": 2}}))
    exec_summary = tmp_path / "artifact_exec_summary.json"
    exec_summary.write_text(json.dumps({"summary": {"failure_count": 3, "top_risk_score": 1.2}}))
    alerts = tmp_path / "artifact_alerts.json"
    alerts.write_text(json.dumps({"summary": {"critical_count": 2}}))
    actions = tmp_path / "artifact_actions.json"
    actions.write_text(json.dumps({"actions": [{"priority": "P0", "target": "x", "owner": "y"}]}))
    history = tmp_path / "artifact_history.json"
    history.write_text(json.dumps({"summary": {"status_direction": "improving"}}))

    payload = build_artifact_scorecard(
        artifact_closeout_path=closeout,
        artifact_exec_summary_path=exec_summary,
        artifact_alerts_path=alerts,
        artifact_actions_path=actions,
        artifact_history_path=history,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["metric_count"] == 8
    assert payload["summary"]["projected_terminal_status"] == "pass"
