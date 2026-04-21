from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_dashboard import build_earthmoving_dashboard


if __name__ == "__main__":
    result = build_earthmoving_dashboard(
        review_packet_path=ROOT / "outputs" / "earthmoving_review_packet" / "review_packet.json",
        output_dir=ROOT / "outputs" / "earthmoving_dashboard",
    )
    print(f"Wrote earthmoving dashboard to {result['index_path']}")
