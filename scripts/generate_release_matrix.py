from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.release_matrix import build_release_matrix


if __name__ == "__main__":
    build_release_matrix(release_checklist_path=ROOT / "outputs" / "release_checklist" / "release_checklist.json", compatibility_path=ROOT / "outputs" / "compatibility" / "compatibility.json", output_dir=ROOT / "outputs" / "release_matrix")
