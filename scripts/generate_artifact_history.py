from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_history import build_artifact_history


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_history"
    payload = build_artifact_history(
        artifact_exec_summary_path=ROOT / "outputs" / "artifact_exec_summary" / "artifact_exec_summary.json",
        artifact_readiness_path=ROOT / "outputs" / "artifact_readiness" / "artifact_readiness.json",
        artifact_delivery_path=ROOT / "outputs" / "artifact_delivery" / "artifact_delivery.json",
        artifact_capacity_path=ROOT / "outputs" / "artifact_capacity" / "artifact_capacity.json",
        artifact_scenarios_path=ROOT / "outputs" / "artifact_scenarios" / "artifact_scenarios.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact history with {len(payload['snapshots'])} snapshots to {output_dir}")


if __name__ == "__main__":
    main()
