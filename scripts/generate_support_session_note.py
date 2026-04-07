from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_session_note import build_support_session_note


if __name__ == "__main__":
    build_support_session_note(
        intake_path=ROOT / "outputs" / "support_intake_checklist" / "support_intake_checklist.json",
        repro_inventory_path=ROOT / "outputs" / "repro_inventory" / "repro_inventory.json",
        response_rubric_path=ROOT / "outputs" / "response_rubric" / "response_rubric.json",
        output_dir=ROOT / "outputs" / "support_session_note",
    )
