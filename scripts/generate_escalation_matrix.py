from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.escalation import build_escalation_matrix


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate escalation guidance from triage artifacts.")
    parser.add_argument("--triage", default=str(ROOT / "outputs" / "triage" / "triage_queue.json"))
    parser.add_argument("--incidents", default=str(ROOT / "outputs" / "incidents" / "index.json"))
    parser.add_argument("--regression-gate", default=str(ROOT / "outputs" / "regression" / "gate" / "regression_gate.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "escalation"))
    args = parser.parse_args()

    payload = build_escalation_matrix(
        triage_queue_path=args.triage,
        incidents_index_path=args.incidents,
        regression_gate_path=args.regression_gate,
        output_dir=args.output_dir,
    )
    print(f"Escalation matrix written to {args.output_dir}")
    print(f"Critical items: {payload['summary']['critical_count']}")


if __name__ == "__main__":
    main()
