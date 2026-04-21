from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_dashboard import build_earthmoving_dashboard


def test_dashboard_writes_static_html(tmp_path: Path) -> None:
    result = build_earthmoving_dashboard(
        review_packet_path=ROOT / "outputs" / "earthmoving_review_packet" / "review_packet.json",
        output_dir=tmp_path / "dashboard",
    )

    index = Path(result["index_path"])
    assert index.exists()
    assert Path(result["data_path"]).exists()
    html = index.read_text()
    assert "Earthmoving Simulation Review" in html
    assert "baseline_push_terrain.png" in html
