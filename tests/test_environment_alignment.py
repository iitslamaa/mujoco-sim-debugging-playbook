import json

from mujoco_sim_debugging_playbook.environment_alignment import build_environment_alignment


def test_environment_alignment_flags_missing_tools(tmp_path):
    diff = tmp_path / "diff.json"
    tools = tmp_path / "tools.json"
    deps = tmp_path / "deps.json"
    diff.write_text(json.dumps({"summary": {"warning_delta": 0}}))
    tools.write_text(json.dumps({"entries": [{"name": "docker", "value": "not detected"}]}))
    deps.write_text(json.dumps({"summary": {"package_count": 10}}))
    payload = build_environment_alignment(
        environment_diff_path=diff,
        toolchain_inventory_path=tools,
        dependency_snapshot_path=deps,
        output_dir=tmp_path,
    )
    assert payload["summary"]["missing_tool_count"] == 1
