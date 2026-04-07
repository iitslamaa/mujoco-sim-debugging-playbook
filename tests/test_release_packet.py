import json

from mujoco_sim_debugging_playbook.release_packet import build_release_packet


def test_release_packet_copies_release_and_support_state(tmp_path):
    release_notes = tmp_path / "release_notes.json"
    support_readiness = tmp_path / "support_readiness.json"
    ops_review = tmp_path / "ops_review.json"
    release_notes.write_text(json.dumps({"base_ref": "a", "head_ref": "b", "commit_count": 3}))
    support_readiness.write_text(json.dumps({"summary": {"status": "warn"}}))
    ops_review.write_text(json.dumps({"summary": {"breach_count": 2}, "wins": ["w1"], "risks": ["r1"]}))
    payload = build_release_packet(
        release_notes_path=release_notes,
        support_readiness_path=support_readiness,
        ops_review_path=ops_review,
    )
    assert payload["summary"]["support_status"] == "warn"
    assert payload["summary"]["commit_count"] == 3
