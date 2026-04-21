from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_role_brief import build_earthmoving_role_brief


if __name__ == "__main__":
    payload = build_earthmoving_role_brief(
        review_packet_path=ROOT / "outputs" / "earthmoving_review_packet" / "review_packet.json",
        dataset_summary_path=ROOT / "outputs" / "earthmoving_dataset" / "dataset_summary.json",
        failure_modes_path=ROOT / "outputs" / "earthmoving_failure_modes" / "failure_modes.json",
        output_dir=ROOT / "outputs" / "earthmoving_role_brief",
    )
    print(f"Wrote earthmoving role brief: {payload['headline']}")
