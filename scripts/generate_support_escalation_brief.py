from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_escalation_brief import build_support_escalation_brief


if __name__ == "__main__":
    build_support_escalation_brief(
        support_triage_reply_path=ROOT / "outputs" / "support_triage_reply" / "support_triage_reply.json",
        support_session_note_path=ROOT / "outputs" / "support_session_note" / "support_session_note.json",
        release_blockers_path=ROOT / "outputs" / "release_blockers" / "release_blockers.json",
        output_dir=ROOT / "outputs" / "support_escalation_brief",
    )
