import json

from mujoco_sim_debugging_playbook.toolchain_inventory import build_toolchain_inventory


def test_toolchain_inventory_builds_entries(tmp_path):
    p = tmp_path / "env.json"
    p.write_text(json.dumps({"platform": {"python_version": "3.10"}, "runtime": {"mujoco_version": "3.2", "numpy_version": "1.0"}, "tooling": {}}))
    payload = build_toolchain_inventory(environment_report_path=p, output_dir=tmp_path)
    assert payload["summary"]["tool_count"] == 5
