import json

from mujoco_sim_debugging_playbook.setup_faq import build_setup_faq


def test_setup_faq_builds_entries(tmp_path):
    doctor = tmp_path / "doctor.json"
    compatibility = tmp_path / "compatibility.json"
    doctor.write_text(json.dumps({"summary": {"status": "warn", "warning_count": 1}, "recommendations": ["Install Docker"]}))
    compatibility.write_text(json.dumps({"checks": [{"detail": "ok"}, {"detail": "warn"}]}))
    payload = build_setup_faq(doctor_path=doctor, compatibility_path=compatibility, output_dir=tmp_path)
    assert payload["summary"]["entry_count"] == 3
