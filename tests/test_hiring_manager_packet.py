from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.hiring_manager_packet import build_hiring_manager_packet


def test_hiring_manager_packet_creates_reviewable_summary(tmp_path: Path) -> None:
    payload = build_hiring_manager_packet(
        repo_root=ROOT,
        output_dir=tmp_path / "packet",
    )

    assert "autonomous earthmoving" in payload["headline"].lower()
    assert payload["manager_summary"]
    assert payload["evidence"]
    assert "Short Note To Send" in (tmp_path / "packet" / "hiring_manager_packet.md").read_text()
    assert (tmp_path / "packet" / "hiring_manager_packet.json").exists()
