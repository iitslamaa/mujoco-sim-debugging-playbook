from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.benchmark import run_controller_benchmark


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark expert, learned, and hybrid controllers across scenarios.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "controller_benchmark.json"))
    parser.add_argument("--checkpoint", default=str(ROOT / "outputs" / "learning" / "training" / "policy.pt"))
    args = parser.parse_args()

    result = run_controller_benchmark(args.config, args.checkpoint)
    print(f"Controller benchmark written to {result['output_dir']}")


if __name__ == "__main__":
    main()

