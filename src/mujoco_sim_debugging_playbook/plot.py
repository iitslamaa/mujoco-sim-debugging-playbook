from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


METRICS_TO_PLOT = [
    ("success_rate", "Success rate"),
    ("final_error_mean", "Mean final error"),
    ("max_overshoot_mean", "Mean overshoot"),
    ("oscillation_index_mean", "Oscillation index"),
    ("control_energy_mean", "Control energy"),
]


def plot_sweep_results(rows: list[dict], output_dir: str | Path) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["parameter"]].append(row)

    for parameter, parameter_rows in grouped.items():
        ordered_rows = sorted(parameter_rows, key=lambda item: item["value"])
        fig, axes = plt.subplots(len(METRICS_TO_PLOT), 1, figsize=(8, 16), sharex=True)
        fig.suptitle(f"Parameter sensitivity: {parameter}")

        x_values = [row["value"] for row in ordered_rows]
        for axis, (metric_key, title) in zip(axes, METRICS_TO_PLOT):
            axis.plot(x_values, [row[metric_key] for row in ordered_rows], marker="o", linewidth=2)
            axis.set_ylabel(title)
            axis.grid(True, alpha=0.3)

        axes[-1].set_xlabel(parameter)
        fig.tight_layout()
        fig.savefig(output_path / f"{parameter}.png", dpi=180)
        plt.close(fig)
