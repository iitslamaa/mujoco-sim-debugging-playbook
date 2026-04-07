from __future__ import annotations

from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_trace(trace_path: str | Path, output_path: str | Path, title: str | None = None) -> None:
    trace = json.loads(Path(trace_path).read_text())
    steps = list(range(len(trace["errors"])))
    ee_xy = trace["ee_xy"]
    target_xy = trace["target_xy"]
    torques = trace["torques"]

    fig, axes = plt.subplots(3, 1, figsize=(8, 12))
    if title:
        fig.suptitle(title)

    axes[0].plot(steps, trace["errors"], linewidth=2)
    axes[0].set_ylabel("Tracking error")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot([point[0] for point in ee_xy], [point[1] for point in ee_xy], label="end effector", linewidth=2)
    axes[1].scatter([target_xy[0][0]], [target_xy[0][1]], label="target", color="red", s=60)
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("y")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(steps, [torque[0] for torque in torques], label="shoulder")
    axes[2].plot(steps, [torque[1] for torque in torques], label="elbow")
    axes[2].set_ylabel("Torque")
    axes[2].set_xlabel("Control step")
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(destination, dpi=180)
    plt.close(fig)

