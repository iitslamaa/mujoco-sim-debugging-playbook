import json

from mujoco_sim_debugging_playbook.machine_readiness import build_machine_readiness


def test_machine_readiness_counts_warnings(tmp_path):
    machine = tmp_path / "machine.json"
    doctor = tmp_path / "doctor.json"
    compatibility = tmp_path / "compatibility.json"
    machine.write_text(json.dumps({"summary": {"system": "Darwin", "machine": "arm64"}}))
    doctor.write_text(json.dumps({"checks": [{"name": "docker_cli", "status": "warn"}]}))
    compatibility.write_text(json.dumps({"checks": [{"name": "python_supported", "status": "pass"}]}))
    payload = build_machine_readiness(
        machine_profile_path=machine,
        doctor_path=doctor,
        compatibility_path=compatibility,
        output_dir=tmp_path,
    )
    assert payload["summary"]["warning_count"] == 1
