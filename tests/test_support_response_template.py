import json

from mujoco_sim_debugging_playbook.support_response_template import build_support_response_template


def test_support_response_template_uses_required_criteria(tmp_path):
    session = tmp_path / "session.json"
    rubric = tmp_path / "rubric.json"
    session.write_text(json.dumps({"summary": {"status": "pass"}, "next_step": "Attach logs."}))
    rubric.write_text(
        json.dumps(
            {
                "criteria": [
                    {"criterion": "Reproduction command", "status": "required"},
                    {"criterion": "Evidence", "status": "recommended"},
                ]
            }
        )
    )
    payload = build_support_response_template(
        support_session_note_path=session,
        response_rubric_path=rubric,
        output_dir=tmp_path,
    )
    assert payload["summary"]["required_section_count"] == 1
