from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.application_readiness import build_application_readiness


def test_application_readiness_checks_bundle_artifacts(tmp_path: Path) -> None:
    payload = build_application_readiness(
        repo_root=ROOT,
        bundle_path=ROOT / "outputs" / "application_bundle" / "application_bundle.json",
        output_dir=tmp_path / "readiness",
    )

    assert payload["summary"]["status"] == "pass"
    assert payload["summary"]["failed_count"] == 0
    assert payload["checks"]
    assert (tmp_path / "readiness" / "application_readiness.md").exists()
