from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support import run_support_case


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a repro and response draft for a support case.")
    parser.add_argument("--case", required=True, help="Support case slug.")
    args = parser.parse_args()

    output_path = run_support_case(args.case, ROOT)
    print(f"Support case report written to {output_path}")


if __name__ == "__main__":
    main()

