from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.regression import compare_snapshots


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two regression snapshots.")
    parser.add_argument("--left", required=True)
    parser.add_argument("--right", required=True)
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "regression" / "latest_diff"))
    args = parser.parse_args()

    result = compare_snapshots(args.left, args.right, args.output_dir)
    print(f"Regression diff written to {args.output_dir}")
    print(result["scalar_deltas"])


if __name__ == "__main__":
    main()

