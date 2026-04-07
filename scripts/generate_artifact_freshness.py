from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_freshness import write_artifact_freshness


def main() -> None:
    payload = write_artifact_freshness(
        root=ROOT,
        output_dir=ROOT / "outputs" / "artifact_freshness",
        artifact_paths=[
            "dashboard/data.json",
            "outputs/support_readiness/support_readiness.json",
            "outputs/scenario_plan/scenario_plan.json",
            "outputs/ops_review/ops_review.json",
            "outputs/scorecard/scorecard.json",
            "outputs/briefing_note/briefing_note.json",
        ],
        reference_paths=[
            "README.md",
            "scripts/generate_dashboard.py",
            "scripts/generate_support_readiness.py",
            "scripts/generate_scenario_plan.py",
            "scripts/generate_scorecard.py",
            "scripts/generate_briefing_note.py",
            "src/mujoco_sim_debugging_playbook/readiness.py",
            "src/mujoco_sim_debugging_playbook/scenario_planner.py",
            "src/mujoco_sim_debugging_playbook/scorecard.py",
            "src/mujoco_sim_debugging_playbook/briefing_note.py",
        ],
    )
    print(f"Artifact freshness written to {ROOT / 'outputs' / 'artifact_freshness'}")
    print("Stale artifacts:", payload["summary"]["stale_count"])


if __name__ == "__main__":
    main()
