from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.simulation_packet import build_simulation_packet


def test_simulation_packet_creates_forwardable_entry_point(tmp_path: Path) -> None:
    root_packet = tmp_path / "EARTHMOVING_SIMULATION_PACKET.md"
    payload = build_simulation_packet(
        repo_root=ROOT,
        output_dir=tmp_path / "packet",
        root_packet_path=root_packet,
    )

    assert "Construction-machine simulation" in payload["headline"]
    assert payload["metrics"]["gate_status"] == "pass"
    assert payload["entry_points"]["dashboard"] == "outputs/earthmoving_dashboard/index.html"
    assert root_packet.exists()
    assert (tmp_path / "packet" / "simulation_packet.json").exists()
    assert (tmp_path / "packet" / "simulation_packet.md").exists()
