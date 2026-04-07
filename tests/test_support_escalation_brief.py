import json

from mujoco_sim_debugging_playbook.support_escalation_brief import build_support_escalation_brief


def test_support_escalation_brief_escalates_when_blockers_exist(tmp_path):
    triage = tmp_path / "triage.json"
    session = tmp_path / "session.json"
    blockers = tmp_path / "blockers.json"
    triage.write_text(json.dumps({"summary": {"status": "ready"}}))
    session.write_text(json.dumps({"summary": {"status": "pass"}, "next_step": "Attach logs."}))
    blockers.write_text(json.dumps({"summary": {"blocker_count": 2}}))
    payload = build_support_escalation_brief(
        support_triage_reply_path=triage,
        support_session_note_path=session,
        release_blockers_path=blockers,
        output_dir=tmp_path,
    )
    assert payload["summary"]["status"] == "escalate"
