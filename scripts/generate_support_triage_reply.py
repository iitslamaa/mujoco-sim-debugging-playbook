from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_triage_reply import build_support_triage_reply


if __name__ == "__main__":
    build_support_triage_reply(
        support_response_template_path=ROOT / "outputs" / "support_response_template" / "support_response_template.json",
        support_session_note_path=ROOT / "outputs" / "support_session_note" / "support_session_note.json",
        support_intake_checklist_path=ROOT / "outputs" / "support_intake_checklist" / "support_intake_checklist.json",
        output_dir=ROOT / "outputs" / "support_triage_reply",
    )
