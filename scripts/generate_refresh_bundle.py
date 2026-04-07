from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.refresh_bundle import write_refresh_bundle


def main() -> None:
    payload = write_refresh_bundle(
        regeneration_plan_path=ROOT / "outputs" / "regeneration_plan" / "regeneration_plan.json",
        impact_analysis_path=ROOT / "outputs" / "impact_analysis" / "impact_analysis.json",
        output_dir=ROOT / "outputs" / "refresh_bundle",
    )
    print(f"Refresh bundle written to {ROOT / 'outputs' / 'refresh_bundle'}")
    print("Bundles:", payload["summary"]["bundle_count"])


if __name__ == "__main__":
    main()
