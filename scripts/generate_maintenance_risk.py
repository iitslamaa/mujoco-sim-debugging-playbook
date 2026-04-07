from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.maintenance_risk import write_maintenance_risk


def main() -> None:
    output_dir = ROOT / "outputs" / "maintenance_risk"
    payload = write_maintenance_risk(
        artifact_freshness_path=ROOT / "outputs" / "artifact_freshness" / "artifact_freshness.json",
        regeneration_plan_path=ROOT / "outputs" / "regeneration_plan" / "regeneration_plan.json",
        impact_analysis_path=ROOT / "outputs" / "impact_analysis" / "impact_analysis.json",
        refresh_bundle_path=ROOT / "outputs" / "refresh_bundle" / "refresh_bundle.json",
        output_dir=output_dir,
    )
    print(f"Wrote maintenance risk for {payload['summary']['artifact_count']} artifacts to {output_dir}")


if __name__ == "__main__":
    main()
