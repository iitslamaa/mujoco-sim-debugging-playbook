from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.experiment import run_sweep_suite


def main() -> None:
    parser = argparse.ArgumentParser(description="Run MuJoCo sweep experiments.")
    parser.add_argument(
        "--config",
        default=str(ROOT / "configs" / "interesting_sweeps.json"),
        help="Path to sweep config JSON.",
    )
    args = parser.parse_args()

    result = run_sweep_suite(args.config)
    print(f"Sweep run complete. Outputs written to {result['output_dir']}")


if __name__ == "__main__":
    main()

