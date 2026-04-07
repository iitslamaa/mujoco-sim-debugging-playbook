from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mujoco_sim_debugging_playbook.config import load_experiment_config
from mujoco_sim_debugging_playbook.rl import train_policy_gradient


def plot_rl_history(summary_path: Path, output_path: Path) -> None:
    payload = json.loads(summary_path.read_text())
    history = payload["history"]
    iterations = [row["iteration"] for row in history]
    returns = [row["mean_episode_return"] for row in history]
    success = [row["success_rate"] for row in history]

    fig, axes = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
    axes[0].plot(iterations, returns, linewidth=2)
    axes[0].set_ylabel("Mean episode return")
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(iterations, success, linewidth=2)
    axes[1].set_ylabel("Success rate")
    axes[1].set_xlabel("Iteration")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune the imitation policy with REINFORCE in MuJoCo.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "baseline.json"))
    parser.add_argument("--imitation-checkpoint", default=str(ROOT / "outputs" / "learning" / "training" / "policy.pt"))
    parser.add_argument("--iterations", type=int, default=12)
    parser.add_argument("--episodes-per-iteration", type=int, default=6)
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "rl" / "training"))
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    summary = train_policy_gradient(
        imitation_checkpoint=args.imitation_checkpoint,
        experiment_config=config,
        iterations=args.iterations,
        episodes_per_iteration=args.episodes_per_iteration,
        output_dir=args.output_dir,
    )
    plot_rl_history(Path(args.output_dir) / "training_summary.json", Path(args.output_dir) / "training_curve.png")
    print("RL training complete.")
    print(summary["history"][-1])


if __name__ == "__main__":
    main()

