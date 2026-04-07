import json

from mujoco_sim_debugging_playbook.support_session_note import build_support_session_note


def test_support_session_note_uses_repro_and_rubric(tmp_path):
    intake = tmp_path / "intake.json"
    repro = tmp_path / "repro.json"
    rubric = tmp_path / "rubric.json"
    intake.write_text(json.dumps({"items": [{"status": "pass"}, {"status": "pass"}, {"status": "pass"}]}))
    repro.write_text(json.dumps({"summary": {"case_count": 2}}))
    rubric.write_text(json.dumps({"criteria": [{"status": "required"}, {"status": "recommended"}]}))
    payload = build_support_session_note(
        intake_path=intake,
        repro_inventory_path=repro,
        response_rubric_path=rubric,
        output_dir=tmp_path,
    )
    assert payload["summary"]["status"] == "pass"
