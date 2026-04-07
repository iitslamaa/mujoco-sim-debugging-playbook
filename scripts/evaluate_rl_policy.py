from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.config import load_experiment_config
from mujoco_sim_debugging_playbook.rl import evaluate_reinforce_policy


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the RL fine-tuned policy in MuJoCo.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "baseline.json"))
    parser.add_argument("--checkpoint", default=str(ROOT / "outputs" / "rl" / "training" / "reinforce_policy.pt"))
    parser.add_argument("--episodes", type=int, default=8)
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "rl" / "evaluation"))
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    result = evaluate_reinforce_policy(args.checkpoint, config, args.episodes, args.output_dir)
    print("RL policy evaluation complete.")
    print(result["summary"])


if __name__ == "__main__":
    main()

