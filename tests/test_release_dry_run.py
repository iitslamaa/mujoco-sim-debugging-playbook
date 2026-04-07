import json

from mujoco_sim_debugging_playbook.release_dry_run import build_release_dry_run


def test_release_dry_run_reports_warn_when_inputs_warn(tmp_path):
    blockers = tmp_path / "blockers.json"
    machine = tmp_path / "machine.json"
    alignment = tmp_path / "alignment.json"
    blockers.write_text(json.dumps({"summary": {"status": "warn", "blocker_count": 2}}))
    machine.write_text(json.dumps({"summary": {"status": "warn", "warning_count": 1}}))
    alignment.write_text(json.dumps({"summary": {"status": "warn", "missing_tool_count": 1}}))
    payload = build_release_dry_run(
        release_blockers_path=blockers,
        machine_readiness_path=machine,
        environment_alignment_path=alignment,
        output_dir=tmp_path,
    )
    assert payload["summary"]["status"] == "warn"
