from mujoco_sim_debugging_playbook.support_command_catalog import build_support_command_catalog


def test_support_command_catalog_extracts_commands(tmp_path):
    cheatsheet = tmp_path / "setup.md"
    cheatsheet.write_text(
        "# Setup\n\n```bash\nbash scripts/bootstrap_env.sh\npython scripts/run_environment_doctor.py\n```\n"
    )
    payload = build_support_command_catalog(setup_cheatsheet_path=cheatsheet, output_dir=tmp_path)
    assert payload["summary"]["command_count"] == 2
