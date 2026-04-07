from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.scenario_planner import build_scenario_plan


def main() -> None:
    payload = build_scenario_plan(
        support_ops_path=ROOT / "outputs" / "support_ops" / "support_ops.json",
        support_gaps_path=ROOT / "outputs" / "support_gaps" / "support_gaps.json",
        sla_report_path=ROOT / "outputs" / "sla" / "sla_report.json",
        capacity_plan_path=ROOT / "outputs" / "capacity" / "capacity_plan.json",
        release_notes_path=ROOT / "outputs" / "releases" / "latest" / "release_notes.json",
        output_dir=ROOT / "outputs" / "scenario_plan",
    )
    print(f"Scenario plan written to {ROOT / 'outputs' / 'scenario_plan'}")
    print("Scenarios:", len(payload["scenarios"]))


if __name__ == "__main__":
    main()
