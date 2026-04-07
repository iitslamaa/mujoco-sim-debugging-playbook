from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mujoco_sim_debugging_playbook.config import load_experiment_config
from mujoco_sim_debugging_playbook.learning import collect_imitation_dataset, train_imitation_policy


def plot_training_history(summary_path: Path, output_path: Path) -> None:
    import json

    payload = json.loads(summary_path.read_text())
    history = payload["history"]
    epochs = [row["epoch"] for row in history]
    train_losses = [row["train_loss"] for row in history]
    val_losses = [row["val_loss"] for row in history]

    fig, axis = plt.subplots(figsize=(8, 4))
    axis.plot(epochs, train_losses, label="train_loss", linewidth=2)
    axis.plot(epochs, val_losses, label="val_loss", linewidth=2)
    axis.set_xlabel("Epoch")
    axis.set_ylabel("Loss")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a PyTorch imitation policy from MuJoCo expert rollouts.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "baseline.json"))
    parser.add_argument("--dataset-episodes", type=int, default=20)
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "learning"))
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    output_dir = Path(args.output_dir)
    dataset_dir = output_dir / "dataset"
    training_dir = output_dir / "training"
    dataset_summary = collect_imitation_dataset(config, episodes=args.dataset_episodes, output_dir=dataset_dir)
    training_summary = train_imitation_policy(
        dataset_path=dataset_dir / "imitation_dataset.npz",
        output_dir=training_dir,
        epochs=args.epochs,
        seed=config.seed,
    )
    plot_training_history(training_dir / "training_summary.json", training_dir / "training_curve.png")
    print("Dataset samples:", dataset_summary["num_samples"])
    print("Best val loss:", training_summary["best_val_loss"])


if __name__ == "__main__":
    main()

