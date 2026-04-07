from mujoco_sim_debugging_playbook.local_paths_report import build_local_paths_report


def test_local_paths_report_has_expected_entries(tmp_path):
    payload = build_local_paths_report(repo_root=tmp_path, output_dir=tmp_path / "out")
    assert payload["summary"]["path_count"] == 5
