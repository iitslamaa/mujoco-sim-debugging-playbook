from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_scorecard import build_artifact_scorecard


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_scorecard"
    payload = build_artifact_scorecard(
        artifact_closeout_path=ROOT / "outputs" / "artifact_closeout" / "artifact_closeout.json",
        artifact_exec_summary_path=ROOT / "outputs" / "artifact_exec_summary" / "artifact_exec_summary.json",
        artifact_alerts_path=ROOT / "outputs" / "artifact_alerts" / "artifact_alerts.json",
        artifact_actions_path=ROOT / "outputs" / "artifact_actions" / "artifact_actions.json",
        artifact_history_path=ROOT / "outputs" / "artifact_history" / "artifact_history.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact scorecard with {payload['summary']['metric_count']} metrics to {output_dir}")


if __name__ == "__main__":
    main()
