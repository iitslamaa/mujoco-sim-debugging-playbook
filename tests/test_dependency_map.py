from pathlib import Path

from mujoco_sim_debugging_playbook.dependency_map import build_dependency_map


def test_dependency_map_counts_existing_dependencies(tmp_path: Path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "generate_dashboard.py").write_text("print('x')")
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "support_readiness").mkdir()
    (tmp_path / "outputs" / "support_readiness" / "support_readiness.json").write_text("{}")
    payload = build_dependency_map(root=tmp_path, artifacts=["dashboard/data.json"])
    assert payload["summary"]["artifact_count"] == 1
    assert payload["rows"][0]["dependency_count"] >= 1
    assert payload["rows"][0]["existing_dependency_count"] >= 1
