from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_gaps import build_support_gap_report


def main() -> None:
    payload = build_support_gap_report(
        triage_queue_path=ROOT / "outputs" / "triage" / "triage_queue.json",
        incidents_index_path=ROOT / "outputs" / "incidents" / "index.json",
        knowledge_base_index_path=ROOT / "outputs" / "knowledge_base" / "index.json",
        escalation_matrix_path=ROOT / "outputs" / "escalation" / "escalation_matrix.json",
        recommendations_path=ROOT / "outputs" / "recommendations" / "recommendations.json",
        output_dir=ROOT / "outputs" / "support_gaps",
    )
    print(f"Support gap report written to {ROOT / 'outputs' / 'support_gaps'}")
    print("Open items needing follow-up:", payload["summary"]["needs_follow_up_count"])


if __name__ == "__main__":
    main()
