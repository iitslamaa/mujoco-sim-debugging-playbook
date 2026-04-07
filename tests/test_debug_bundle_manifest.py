from pathlib import Path

from mujoco_sim_debugging_playbook.debug_bundle_manifest import build_debug_bundle_manifest


def test_debug_bundle_manifest_uses_latest_bundle(tmp_path):
    older = tmp_path / "a"
    newer = tmp_path / "b"
    older.mkdir()
    newer.mkdir()
    (newer / "file.txt").write_text("x")
    payload = build_debug_bundle_manifest(bundle_root=tmp_path, output_dir=tmp_path / "out")
    assert payload["summary"]["bundle"] == "b"
