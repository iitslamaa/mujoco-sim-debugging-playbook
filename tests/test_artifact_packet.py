import json

from mujoco_sim_debugging_playbook.artifact_packet import build_artifact_packet


def test_artifact_packet_collects_summary_fields(tmp_path):
    scorecard = tmp_path / "artifact_scorecard.json"
    scorecard.write_text(json.dumps({"summary": {"current_status": "fail", "closeout_status": "not_ready", "projected_terminal_status": "pass"}}))
    digest = tmp_path / "artifact_digest.json"
    digest.write_text(json.dumps({"summary": {"headline_count": 2}, "headlines": ["a"], "alerts": [], "actions": []}))
    handoff = tmp_path / "artifact_handoff.json"
    handoff.write_text(json.dumps({"summary": {"handoff_owner": "owner-a"}, "owner_context": {"owner": "owner-a", "status": "overloaded", "command_count": 4}, "actions": []}))
    closeout = tmp_path / "artifact_closeout.json"
    closeout.write_text(json.dumps({"summary": {"remaining_action_count": 2}, "closeout_checks": [], "remaining_actions": []}))

    payload = build_artifact_packet(
        artifact_scorecard_path=scorecard,
        artifact_digest_path=digest,
        artifact_handoff_path=handoff,
        artifact_closeout_path=closeout,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["handoff_owner"] == "owner-a"
    assert payload["summary"]["remaining_action_count"] == 2
