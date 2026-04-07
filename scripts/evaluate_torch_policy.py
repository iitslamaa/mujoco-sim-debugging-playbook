from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.config import load_experiment_config
from mujoco_sim_debugging_playbook.learning import evaluate_policy


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained PyTorch policy in MuJoCo.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "baseline.json"))
    parser.add_argument("--checkpoint", default=str(ROOT / "outputs" / "learning" / "training" / "policy.pt"))
    parser.add_argument("--episodes", type=int, default=8)
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "learning" / "evaluation"))
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    result = evaluate_policy(args.checkpoint, config, episodes=args.episodes, output_dir=args.output_dir)
    print("Policy evaluation complete.")
    print(result["summary"])


if __name__ == "__main__":
    main()

