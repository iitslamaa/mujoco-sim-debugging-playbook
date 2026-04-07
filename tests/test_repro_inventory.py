from pathlib import Path

from mujoco_sim_debugging_playbook.repro_inventory import build_repro_inventory


def test_repro_inventory_lists_support_cases(tmp_path):
    support_dir = tmp_path / "support_cases"
    support_dir.mkdir()
    (support_dir / "case_a.md").write_text("# case a")
    (support_dir / "case_b.md").write_text("# case b")

    payload = build_repro_inventory(
        support_cases_dir=support_dir,
        output_dir=tmp_path,
    )

    assert payload["summary"]["case_count"] == 2
    assert payload["cases"][0]["case_id"] == "case_a"
