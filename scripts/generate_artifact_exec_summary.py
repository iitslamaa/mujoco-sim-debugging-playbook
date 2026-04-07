from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_exec_summary import build_artifact_exec_summary


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_exec_summary"
    payload = build_artifact_exec_summary(
        artifact_readiness_path=ROOT / "outputs" / "artifact_readiness" / "artifact_readiness.json",
        maintenance_risk_path=ROOT / "outputs" / "maintenance_risk" / "maintenance_risk.json",
        artifact_delivery_path=ROOT / "outputs" / "artifact_delivery" / "artifact_delivery.json",
        artifact_capacity_path=ROOT / "outputs" / "artifact_capacity" / "artifact_capacity.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact executive summary with status {payload['summary']['status']} to {output_dir}")


if __name__ == "__main__":
    main()
