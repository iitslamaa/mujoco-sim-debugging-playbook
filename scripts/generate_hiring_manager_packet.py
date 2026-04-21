from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.hiring_manager_packet import build_hiring_manager_packet


if __name__ == "__main__":
    payload = build_hiring_manager_packet(
        repo_root=ROOT,
        output_dir=ROOT / "outputs" / "hiring_manager_packet",
    )
    print(f"Wrote hiring manager packet: {payload['headline']}")
