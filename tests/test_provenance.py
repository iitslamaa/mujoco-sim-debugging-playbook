from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.provenance import build_provenance_index, write_manifest


def test_write_manifest_and_index(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    output_dir = repo_root / "outputs" / "baseline"
    output_dir.mkdir(parents=True)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps({"ok": True}))

    manifest_path = write_manifest(
        repo_root=repo_root,
        output_dir=output_dir,
        run_type="experiment",
        config={"name": "baseline"},
        outputs=[summary_path],
        metadata={"tag": "test"},
    )
    assert manifest_path.exists()

    index_payload = build_provenance_index(
        repo_root=repo_root,
        manifest_paths=[manifest_path],
        output_dir=repo_root / "outputs" / "provenance",
    )
    assert index_payload["summary"]["manifest_count"] == 1
    assert index_payload["manifests"][0]["run_type"] == "experiment"
    assert (repo_root / "outputs" / "provenance" / "index.md").exists()
