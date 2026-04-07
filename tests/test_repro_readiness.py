import json

from mujoco_sim_debugging_playbook.repro_readiness import build_repro_readiness


def test_repro_readiness_marks_ready_when_cases_and_intake_exist(tmp_path):
    repro = tmp_path / "repro.json"
    intake = tmp_path / "intake.json"
    repro.write_text(json.dumps({"summary": {"entry_count": 1}, "entries": [{"case_id": "delay"}]}))
    intake.write_text(json.dumps({"items": [{"status": "pass"}, {"status": "pass"}]}))
    payload = build_repro_readiness(
        repro_bundle_index_path=repro,
        support_intake_checklist_path=intake,
        output_dir=tmp_path,
    )
    assert payload["summary"]["status"] == "ready"
