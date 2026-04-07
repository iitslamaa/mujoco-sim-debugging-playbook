from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.workstream import build_workstream_plan


def main() -> None:
    payload = build_workstream_plan(
        support_gaps_path=ROOT / "outputs" / "support_gaps" / "support_gaps.json",
        triage_queue_path=ROOT / "outputs" / "triage" / "triage_queue.json",
        recommendations_path=ROOT / "outputs" / "recommendations" / "recommendations.json",
        output_dir=ROOT / "outputs" / "workstreams",
    )
    print(f"Workstream plan written to {ROOT / 'outputs' / 'workstreams'}")
    print("Planned items:", payload["summary"]["item_count"])


if __name__ == "__main__":
    main()
