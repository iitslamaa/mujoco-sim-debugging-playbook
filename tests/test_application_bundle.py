from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.application_bundle import build_application_bundle


def test_application_bundle_indexes_sendable_artifacts(tmp_path: Path) -> None:
    payload = build_application_bundle(
        repo_root=ROOT,
        output_dir=tmp_path / "bundle",
    )

    assert payload["summary"]["item_count"] >= 5
    assert payload["summary"]["missing_count"] == 0
    assert payload["send_order"]
    assert (tmp_path / "bundle" / "application_bundle.md").exists()
