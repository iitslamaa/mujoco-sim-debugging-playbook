from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.release_blockers import build_release_blockers


if __name__ == "__main__":
    build_release_blockers(
        release_checklist_path=ROOT / "outputs" / "release_checklist" / "release_checklist.json",
        release_matrix_path=ROOT / "outputs" / "release_matrix" / "release_matrix.json",
        output_dir=ROOT / "outputs" / "release_blockers",
    )
