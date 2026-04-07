from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_actions import build_artifact_actions


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_actions"
    payload = build_artifact_actions(
        artifact_exec_summary_path=ROOT / "outputs" / "artifact_exec_summary" / "artifact_exec_summary.json",
        artifact_delivery_path=ROOT / "outputs" / "artifact_delivery" / "artifact_delivery.json",
        artifact_capacity_path=ROOT / "outputs" / "artifact_capacity" / "artifact_capacity.json",
        artifact_history_path=ROOT / "outputs" / "artifact_history" / "artifact_history.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact action register with {len(payload['actions'])} actions to {output_dir}")


if __name__ == "__main__":
    main()
