from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.config import load_experiment_config
from mujoco_sim_debugging_playbook.experiment import run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run baseline MuJoCo reaching experiments.")
    parser.add_argument(
        "--config",
        default=str(ROOT / "configs" / "baseline.json"),
        help="Path to experiment config JSON.",
    )
    parser.add_argument("--episodes", type=int, default=None, help="Override episode count.")
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    if args.episodes is not None:
        config = type(config)(
            name=config.name,
            episodes=args.episodes,
            episode_horizon_s=config.episode_horizon_s,
            seed=config.seed,
            output_dir=config.output_dir,
            task=config.task,
            sim=config.sim,
            controller=config.controller,
        )
    result = run_experiment(config)
    print(f"Baseline run complete. Outputs written to {result['output_dir']}")
    print(result["summary"])


if __name__ == "__main__":
    main()
