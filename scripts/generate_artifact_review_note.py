from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_review_note import build_artifact_review_note


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_review_note"
    payload = build_artifact_review_note(
        artifact_handoff_path=ROOT / "outputs" / "artifact_handoff" / "artifact_handoff.json",
        artifact_digest_path=ROOT / "outputs" / "artifact_digest" / "artifact_digest.json",
        artifact_history_path=ROOT / "outputs" / "artifact_history" / "artifact_history.json",
        artifact_actions_path=ROOT / "outputs" / "artifact_actions" / "artifact_actions.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact review note with {payload['summary']['approval_count']} approvals to {output_dir}")


if __name__ == "__main__":
    main()
