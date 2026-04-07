import json

from mujoco_sim_debugging_playbook.artifact_review_note import build_artifact_review_note


def test_artifact_review_note_collects_blockers_and_approvals(tmp_path):
    handoff = tmp_path / "artifact_handoff.json"
    handoff.write_text(
        json.dumps(
            {
                "summary": {"status": "fail"},
                "alerts": [
                    {"severity": "critical", "message": "blocker a"},
                    {"severity": "warning", "message": "blocker b"},
                ],
            }
        )
    )
    digest = tmp_path / "artifact_digest.json"
    digest.write_text(json.dumps({"headlines": ["a", "b", "c"]}))
    history = tmp_path / "artifact_history.json"
    history.write_text(json.dumps({"summary": {"projected_terminal_status": "pass"}}))
    actions = tmp_path / "artifact_actions.json"
    actions.write_text(json.dumps({"actions": [{"priority": "P0", "target": "x", "owner": "y"}]}))

    payload = build_artifact_review_note(
        artifact_handoff_path=handoff,
        artifact_digest_path=digest,
        artifact_history_path=history,
        artifact_actions_path=actions,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["blocker_count"] == 2
    assert payload["summary"]["approval_count"] == 1
