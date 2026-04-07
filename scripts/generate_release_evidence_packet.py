from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.release_evidence_packet import build_release_evidence_packet


if __name__ == "__main__":
    build_release_evidence_packet(
        release_dry_run_path=ROOT / "outputs" / "release_dry_run" / "release_dry_run.json",
        release_blockers_path=ROOT / "outputs" / "release_blockers" / "release_blockers.json",
        release_matrix_path=ROOT / "outputs" / "release_matrix" / "release_matrix.json",
        output_dir=ROOT / "outputs" / "release_evidence_packet",
    )
