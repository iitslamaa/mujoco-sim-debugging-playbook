from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_response_template import build_support_response_template


if __name__ == "__main__":
    build_support_response_template(
        support_session_note_path=ROOT / "outputs" / "support_session_note" / "support_session_note.json",
        response_rubric_path=ROOT / "outputs" / "response_rubric" / "response_rubric.json",
        output_dir=ROOT / "outputs" / "support_response_template",
    )
