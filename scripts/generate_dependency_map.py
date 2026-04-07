from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dependency_map import write_dependency_map


def main() -> None:
    payload = write_dependency_map(
        root=ROOT,
        output_dir=ROOT / "outputs" / "dependency_map",
        artifacts=[
            "dashboard/data.json",
            "outputs/support_readiness/support_readiness.json",
            "outputs/scenario_plan/scenario_plan.json",
            "outputs/ops_review/ops_review.json",
            "outputs/scorecard/scorecard.json",
            "outputs/briefing_note/briefing_note.json",
        ],
    )
    print(f"Dependency map written to {ROOT / 'outputs' / 'dependency_map'}")
    print("Artifacts mapped:", payload["summary"]["artifact_count"])


if __name__ == "__main__":
    main()
