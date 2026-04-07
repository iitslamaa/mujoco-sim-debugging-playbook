import json

from mujoco_sim_debugging_playbook.support_triage_reply import build_support_triage_reply


def test_support_triage_reply_marks_ready_when_intake_complete(tmp_path):
    template = tmp_path / "template.json"
    session = tmp_path / "session.json"
    intake = tmp_path / "intake.json"
    template.write_text(json.dumps({"sections": [{}, {}]}))
    session.write_text(json.dumps({"summary": {"status": "pass"}, "next_step": "Attach logs."}))
    intake.write_text(json.dumps({"items": [{"status": "pass"}, {"status": "pass"}]}))
    payload = build_support_triage_reply(
        support_response_template_path=template,
        support_session_note_path=session,
        support_intake_checklist_path=intake,
        output_dir=tmp_path,
    )
    assert payload["summary"]["status"] == "ready"
