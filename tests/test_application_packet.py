from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.application_packet import build_application_packet


def test_application_packet_creates_forwardable_summary(tmp_path: Path) -> None:
    payload = build_application_packet(
        repo_root=ROOT,
        output_dir=tmp_path / "application",
    )

    assert "earthmoving" in payload["headline"].lower()
    assert payload["proof_points"]
    assert payload["message"].startswith("Hi [Name]")
    assert (tmp_path / "application" / "application_packet.md").exists()
