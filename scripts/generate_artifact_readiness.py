from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_readiness import write_artifact_readiness


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_readiness"
    payload = write_artifact_readiness(
        artifact_freshness_path=ROOT / "outputs" / "artifact_freshness" / "artifact_freshness.json",
        maintenance_risk_path=ROOT / "outputs" / "maintenance_risk" / "maintenance_risk.json",
        refresh_checklist_path=ROOT / "outputs" / "refresh_checklist" / "refresh_checklist.json",
        regeneration_plan_path=ROOT / "outputs" / "regeneration_plan" / "regeneration_plan.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact readiness with status {payload['summary']['status']} to {output_dir}")


if __name__ == "__main__":
    main()
