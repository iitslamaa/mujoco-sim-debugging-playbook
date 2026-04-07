from pathlib import Path

from mujoco_sim_debugging_playbook.evidence_inventory import build_evidence_inventory


def test_evidence_inventory_indexes_output_files(tmp_path):
    root = tmp_path
    output = root / "outputs" / "demo"
    output.mkdir(parents=True)
    (output / "a.json").write_text("{}")
    (output / "b.md").write_text("# hi")
    payload = build_evidence_inventory(root=root)
    assert payload["summary"]["file_count"] == 2
    assert payload["summary"]["area_count"] == 1
