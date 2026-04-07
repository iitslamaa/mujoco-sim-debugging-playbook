import json
from mujoco_sim_debugging_playbook.machine_profile import build_machine_profile


def test_machine_profile_reads_platform(tmp_path):
    p = tmp_path / "e.json"
    p.write_text(json.dumps({"platform": {"system": "Darwin", "machine": "arm64", "python_version": "3.10"}}))
    payload = build_machine_profile(environment_report_path=p, output_dir=tmp_path)
    assert payload["summary"]["system"] == "Darwin"
