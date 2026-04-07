import json

from mujoco_sim_debugging_playbook.release_checklist import build_release_checklist


def test_release_checklist_counts_statuses(tmp_path):
    doctor = tmp_path / "doctor.json"
    compatibility = tmp_path / "compatibility.json"
    doctor.write_text(json.dumps({"summary": {"status": "warn", "warning_count": 1}}))
    compatibility.write_text(json.dumps({"summary": {"status": "pass"}}))
    payload = build_release_checklist(doctor_path=doctor, compatibility_path=compatibility, output_dir=tmp_path)
    assert payload["summary"]["item_count"] == 3
