from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "mujoco_sim_debugging_playbook_mpl"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mujoco_sim_debugging_playbook.environment import capture_environment_report


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _mean_by_controller(rows: list[dict[str, Any]], metric: str) -> dict[str, float]:
    grouped: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(row["controller"], []).append(float(row[metric]))
    return {controller: float(np.mean(values)) for controller, values in grouped.items()}


def create_regression_snapshot(repo_root: str | Path, name: str) -> Path:
    root = Path(repo_root)
    snapshot_dir = root / "outputs" / "regression" / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    baseline = _read_json(root / "outputs" / "baseline" / "summary.json")["summary"]
    imitation = _read_json(root / "outputs" / "learning" / "evaluation" / "summary.json")["summary"]
    rl_eval = _read_json(root / "outputs" / "rl" / "evaluation" / "summary.json")["summary"]
    benchmark = _read_json(root / "outputs" / "controller_benchmark" / "benchmark_summary.json")["benchmark_rows"]
    randomization = _read_json(root / "outputs" / "domain_randomization" / "evaluation_rows.json")["rows"]

    payload = {
        "name": name,
        "environment": capture_environment_report(root),
        "metrics": {
            "baseline_success_rate": baseline["success_rate"],
            "baseline_final_error_mean": baseline["final_error_mean"],
            "imitation_success_rate": imitation["success_rate"],
            "imitation_final_error_mean": imitation["final_error_mean"],
            "rl_success_rate": rl_eval["success_rate"],
            "rl_final_error_mean": rl_eval["final_error_mean"],
            "benchmark_success_rate_by_controller": _mean_by_controller(benchmark, "success_rate"),
            "randomization_success_rate_by_controller": _mean_by_controller(randomization, "success"),
            "randomization_final_error_by_controller": _mean_by_controller(randomization, "final_error"),
        },
    }
    path = snapshot_dir / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


def compare_snapshots(left_path: str | Path, right_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    left = _read_json(left_path)
    right = _read_json(right_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    scalar_keys = [
        "baseline_success_rate",
        "baseline_final_error_mean",
        "imitation_success_rate",
        "imitation_final_error_mean",
        "rl_success_rate",
        "rl_final_error_mean",
    ]
    scalar_deltas = {
        key: float(right["metrics"][key] - left["metrics"][key])
        for key in scalar_keys
    }

    controller_delta = {}
    for metric_key in ["benchmark_success_rate_by_controller", "randomization_success_rate_by_controller", "randomization_final_error_by_controller"]:
        all_controllers = sorted(set(left["metrics"][metric_key]) | set(right["metrics"][metric_key]))
        controller_delta[metric_key] = {
            controller: float(right["metrics"][metric_key].get(controller, 0.0) - left["metrics"][metric_key].get(controller, 0.0))
            for controller in all_controllers
        }

    payload = {
        "left": left["name"],
        "right": right["name"],
        "scalar_deltas": scalar_deltas,
        "controller_deltas": controller_delta,
    }
    (output / "regression_diff.json").write_text(json.dumps(payload, indent=2))
    _write_markdown(payload, output / "regression_diff.md")
    _plot_regression(payload, output / "regression_diff.png")
    return payload


def _write_markdown(payload: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Regression Diff",
        "",
        f"Comparing `{payload['left']}` -> `{payload['right']}`.",
        "",
        "## Scalar deltas",
        "",
        "| metric | delta |",
        "| --- | ---: |",
    ]
    for key, value in payload["scalar_deltas"].items():
        lines.append(f"| {key} | {value:.4f} |")

    lines.extend(["", "## Controller deltas", ""])
    for metric_key, deltas in payload["controller_deltas"].items():
        lines.extend(
            [
                f"### {metric_key}",
                "",
                "| controller | delta |",
                "| --- | ---: |",
            ]
        )
        for controller, value in deltas.items():
            lines.append(f"| {controller} | {value:.4f} |")
        lines.append("")

    Path(path).write_text("\n".join(lines))


def _plot_regression(payload: dict[str, Any], path: str | Path) -> None:
    labels = list(payload["scalar_deltas"].keys())
    values = [payload["scalar_deltas"][key] for key in labels]

    fig, axis = plt.subplots(figsize=(10, 4.8))
    colors = ["#0F9D58" if value >= 0 else "#C85C2C" for value in values]
    axis.bar(labels, values, color=colors)
    axis.axhline(0.0, color="black", linewidth=1)
    axis.set_title("Regression delta summary")
    axis.set_ylabel("Delta")
    axis.tick_params(axis="x", rotation=25)
    axis.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)
