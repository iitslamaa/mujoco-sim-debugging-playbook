from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.release_handoff_note import build_release_handoff_note


if __name__ == "__main__":
    build_release_handoff_note(
        release_evidence_packet_path=ROOT / "outputs" / "release_evidence_packet" / "release_evidence_packet.json",
        release_dry_run_path=ROOT / "outputs" / "release_dry_run" / "release_dry_run.json",
        output_dir=ROOT / "outputs" / "release_handoff_note",
    )
