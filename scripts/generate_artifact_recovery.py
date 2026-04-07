from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_recovery import write_artifact_recovery


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_recovery"
    payload = write_artifact_recovery(
        artifact_readiness_path=ROOT / "outputs" / "artifact_readiness" / "artifact_readiness.json",
        artifact_scenarios_path=ROOT / "outputs" / "artifact_scenarios" / "artifact_scenarios.json",
        maintenance_risk_path=ROOT / "outputs" / "maintenance_risk" / "maintenance_risk.json",
        refresh_checklist_path=ROOT / "outputs" / "refresh_checklist" / "refresh_checklist.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact recovery roadmap with {len(payload['phases'])} phases to {output_dir}")


if __name__ == "__main__":
    main()
