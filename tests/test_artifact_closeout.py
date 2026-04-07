import json

from mujoco_sim_debugging_playbook.artifact_closeout import build_artifact_closeout


def test_artifact_closeout_marks_not_ready_when_blockers_remain(tmp_path):
    review_note = tmp_path / "artifact_review_note.json"
    review_note.write_text(json.dumps({"summary": {"status": "fail", "blocker_count": 2}}))
    history = tmp_path / "artifact_history.json"
    history.write_text(json.dumps({"summary": {"projected_terminal_status": "pass"}}))
    handoff = tmp_path / "artifact_handoff.json"
    handoff.write_text(json.dumps({"summary": {"handoff_owner": "owner-a", "action_count": 2}}))
    actions = tmp_path / "artifact_actions.json"
    actions.write_text(json.dumps({"actions": [{"priority": "P0", "target": "x", "owner": "y", "expected_impact": "z"}]}))

    payload = build_artifact_closeout(
        artifact_review_note_path=review_note,
        artifact_history_path=history,
        artifact_handoff_path=handoff,
        artifact_actions_path=actions,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["status"] == "not_ready_to_close"
    assert payload["summary"]["remaining_action_count"] == 1
