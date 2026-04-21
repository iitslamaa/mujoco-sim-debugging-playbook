from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.application_packet import build_application_packet


if __name__ == "__main__":
    payload = build_application_packet(
        repo_root=ROOT,
        output_dir=ROOT / "outputs" / "application_packet",
    )
    print(f"Wrote application packet: {payload['headline']}")
