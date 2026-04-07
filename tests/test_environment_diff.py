import json

from mujoco_sim_debugging_playbook.environment_diff import build_environment_diff


def test_environment_diff_tracks_warning_delta(tmp_path):
    doctor = tmp_path / "doctor.json"
    compatibility = tmp_path / "compatibility.json"
    doctor.write_text(json.dumps({"summary": {"status": "warn", "warning_count": 2}}))
    compatibility.write_text(json.dumps({"summary": {"status": "warn", "warn_count": 1}}))
    payload = build_environment_diff(doctor_path=doctor, compatibility_path=compatibility, output_dir=tmp_path)
    assert payload["summary"]["warning_delta"] == 1
