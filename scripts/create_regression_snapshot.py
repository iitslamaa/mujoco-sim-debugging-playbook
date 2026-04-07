from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.regression import create_regression_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a named regression snapshot from current outputs.")
    parser.add_argument("--name", required=True, help="Snapshot name.")
    args = parser.parse_args()

    path = create_regression_snapshot(ROOT, args.name)
    print(f"Regression snapshot written to {path}")


if __name__ == "__main__":
    main()

