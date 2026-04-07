from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_ops import build_support_ops_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate support operations summary metrics.")
    parser.add_argument("--triage", default=str(ROOT / "outputs" / "triage" / "triage_queue.json"))
    parser.add_argument("--incidents", default=str(ROOT / "outputs" / "incidents" / "index.json"))
    parser.add_argument("--knowledge-base", default=str(ROOT / "outputs" / "knowledge_base" / "index.json"))
    parser.add_argument("--escalation", default=str(ROOT / "outputs" / "escalation" / "escalation_matrix.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "support_ops"))
    args = parser.parse_args()

    payload = build_support_ops_report(
        triage_queue_path=args.triage,
        incidents_index_path=args.incidents,
        knowledge_base_index_path=args.knowledge_base,
        escalation_matrix_path=args.escalation,
        output_dir=args.output_dir,
    )
    print(f"Support ops report written to {args.output_dir}")
    print(f"Queue count: {payload['summary']['queue_count']}")


if __name__ == "__main__":
    main()
