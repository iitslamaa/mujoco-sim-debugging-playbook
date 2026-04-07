from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_closeout import build_artifact_closeout


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_closeout"
    payload = build_artifact_closeout(
        artifact_review_note_path=ROOT / "outputs" / "artifact_review_note" / "artifact_review_note.json",
        artifact_history_path=ROOT / "outputs" / "artifact_history" / "artifact_history.json",
        artifact_handoff_path=ROOT / "outputs" / "artifact_handoff" / "artifact_handoff.json",
        artifact_actions_path=ROOT / "outputs" / "artifact_actions" / "artifact_actions.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact closeout with status {payload['summary']['status']} to {output_dir}")


if __name__ == "__main__":
    main()
