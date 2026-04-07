from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_digest import build_artifact_digest


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_digest"
    payload = build_artifact_digest(
        artifact_alerts_path=ROOT / "outputs" / "artifact_alerts" / "artifact_alerts.json",
        artifact_actions_path=ROOT / "outputs" / "artifact_actions" / "artifact_actions.json",
        artifact_history_path=ROOT / "outputs" / "artifact_history" / "artifact_history.json",
        artifact_exec_summary_path=ROOT / "outputs" / "artifact_exec_summary" / "artifact_exec_summary.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact digest with {payload['summary']['headline_count']} headlines to {output_dir}")


if __name__ == "__main__":
    main()
