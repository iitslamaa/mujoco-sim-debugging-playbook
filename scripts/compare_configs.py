from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.diagnostics import compare_summaries, load_summary, summarize_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two experiment summary.json files.")
    parser.add_argument("--left", required=True, help="Left summary.json path.")
    parser.add_argument("--right", required=True, help="Right summary.json path.")
    parser.add_argument("--left-label", default="left", help="Label for left summary.")
    parser.add_argument("--right-label", default="right", help="Label for right summary.")
    args = parser.parse_args()

    left = summarize_experiment(load_summary(args.left), args.left_label)
    right = summarize_experiment(load_summary(args.right), args.right_label)
    deltas = compare_summaries(left, right)

    print(f"{left.label} success_rate: {left.success_rate:.3f}")
    print(f"{right.label} success_rate: {right.success_rate:.3f}")
    print(f"success_rate_delta: {deltas['success_rate_delta']:.3f}")
    print(f"final_error_mean_delta: {deltas['final_error_mean_delta']:.4f}")
    print(f"max_overshoot_mean_delta: {deltas['max_overshoot_mean_delta']:.4f}")
    print(f"oscillation_index_mean_delta: {deltas['oscillation_index_mean_delta']:.4f}")


if __name__ == "__main__":
    main()

