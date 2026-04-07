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


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_anomaly_report(
    *,
    benchmark_summary_path: str | Path,
    randomization_rows_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    benchmark_payload = _read_json(benchmark_summary_path)
    randomization_payload = _read_json(randomization_rows_path)

    benchmark_rows = benchmark_payload["benchmark_rows"]
    randomization_rows = randomization_payload["rows"]

    benchmark_anomalies = _rank_benchmark_anomalies(benchmark_rows)
    randomization_anomalies = _rank_randomization_anomalies(randomization_rows)
    parameter_effects = _estimate_parameter_effects(randomization_rows)

    payload = {
        "benchmark_anomalies": benchmark_anomalies,
        "randomization_anomalies": randomization_anomalies,
        "parameter_effects": parameter_effects,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "anomaly_report.json").write_text(json.dumps(payload, indent=2))
    _write_markdown(payload, output / "anomaly_report.md")
    _plot_benchmark_heatmap(benchmark_anomalies, output / "benchmark_risk_heatmap.png")
    _plot_randomization_difficulty(randomization_anomalies, output / "randomization_difficulty.png")
    _plot_parameter_effects(parameter_effects, output / "parameter_effects.png")
    return payload


def _rank_benchmark_anomalies(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scenarios = sorted({row["scenario"] for row in rows})
    controllers = sorted({row["controller"] for row in rows})
    risk_rows = []
    heatmap = np.zeros((len(controllers), len(scenarios)))

    for scenario_index, scenario in enumerate(scenarios):
        scenario_rows = [row for row in rows if row["scenario"] == scenario]
        best_success = max(row["success_rate"] for row in scenario_rows)
        best_error = min(row["final_error_mean"] for row in scenario_rows)
        lowest_energy = min(row["control_energy_mean"] for row in scenario_rows)
        for row in scenario_rows:
            success_gap = best_success - row["success_rate"]
            error_gap = max(0.0, row["final_error_mean"] - best_error)
            energy_gap = max(0.0, row["control_energy_mean"] - lowest_energy)
            risk_score = float(5.0 * success_gap + 20.0 * error_gap + 0.015 * energy_gap)
            item = {
                "scenario": scenario,
                "controller": row["controller"],
                "risk_score": risk_score,
                "success_gap": float(success_gap),
                "error_gap": float(error_gap),
                "energy_gap": float(energy_gap),
                "success_rate": float(row["success_rate"]),
                "final_error_mean": float(row["final_error_mean"]),
            }
            risk_rows.append(item)
            controller_index = controllers.index(row["controller"])
            heatmap[controller_index, scenario_index] = risk_score

    ordered = sorted(risk_rows, key=lambda item: item["risk_score"], reverse=True)
    return {
        "top_cases": ordered[:8],
        "controllers": controllers,
        "scenarios": scenarios,
        "heatmap": heatmap.tolist(),
    }


def _rank_randomization_anomalies(rows: list[dict[str, Any]]) -> dict[str, Any]:
    episodes = sorted({int(row["episode"]) for row in rows})
    episode_summaries = []
    for episode in episodes:
        episode_rows = [row for row in rows if int(row["episode"]) == episode]
        ordered = sorted(episode_rows, key=lambda row: (-row["success"], row["final_error"], row["control_energy"]))
        hardest = sorted(episode_rows, key=lambda row: (-row["final_error"], row["success"], -row["control_energy"]))[0]
        avg_final_error = float(np.mean([row["final_error"] for row in episode_rows]))
        success_rate = float(np.mean([row["success"] for row in episode_rows]))
        best = ordered[0]
        worst = sorted(episode_rows, key=lambda row: (row["success"], -row["final_error"], row["control_energy"]))[0]
        difficulty_score = float(avg_final_error + (1.0 - success_rate))
        episode_summaries.append(
            {
                "episode": episode,
                "difficulty_score": difficulty_score,
                "avg_final_error": avg_final_error,
                "success_rate": success_rate,
                "best_controller": best["controller"],
                "worst_controller": worst["controller"],
                "worst_final_error": float(hardest["final_error"]),
                "joint_damping": float(hardest["joint_damping"]),
                "actuator_gain": float(hardest["actuator_gain"]),
                "sensor_noise_std": float(hardest["sensor_noise_std"]),
                "control_delay_steps": int(hardest["control_delay_steps"]),
            }
        )
    ordered = sorted(episode_summaries, key=lambda item: item["difficulty_score"], reverse=True)
    return {"episodes": ordered}


def _estimate_parameter_effects(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    effects = []
    target = np.asarray([row["final_error"] + (1 - row["success"]) for row in rows], dtype=float)
    for parameter in ["joint_damping", "friction_loss", "actuator_gain", "sensor_noise_std", "control_delay_steps"]:
        values = np.asarray([row[parameter] for row in rows], dtype=float)
        correlation = float(np.corrcoef(values, target)[0, 1]) if np.std(values) > 0 else 0.0
        effects.append({"parameter": parameter, "correlation_with_difficulty": correlation})
    return sorted(effects, key=lambda item: abs(item["correlation_with_difficulty"]), reverse=True)


def _write_markdown(payload: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Anomaly Report",
        "",
        "Scenario-level anomaly analysis across the controller benchmark and domain randomization suite.",
        "",
        "## Highest-risk benchmark cases",
        "",
        "| scenario | controller | risk_score | success_gap | error_gap | energy_gap |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["benchmark_anomalies"]["top_cases"]:
        lines.append(
            f"| {row['scenario']} | {row['controller']} | {row['risk_score']:.4f} | "
            f"{row['success_gap']:.4f} | {row['error_gap']:.4f} | {row['energy_gap']:.4f} |"
        )

    lines.extend(["", "## Hardest randomized episodes", "", "| episode | difficulty_score | best | worst | avg_final_error | success_rate | delay | noise | gain | damping |", "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"])
    for row in payload["randomization_anomalies"]["episodes"][:8]:
        lines.append(
            f"| {row['episode']} | {row['difficulty_score']:.4f} | {row['best_controller']} | {row['worst_controller']} | "
            f"{row['avg_final_error']:.4f} | {row['success_rate']:.4f} | {row['control_delay_steps']} | "
            f"{row['sensor_noise_std']:.4f} | {row['actuator_gain']:.4f} | {row['joint_damping']:.4f} |"
        )

    lines.extend(["", "## Parameter effects", "", "| parameter | correlation_with_difficulty |", "| --- | ---: |"])
    for row in payload["parameter_effects"]:
        lines.append(f"| {row['parameter']} | {row['correlation_with_difficulty']:.4f} |")

    Path(path).write_text("\n".join(lines))


def _plot_benchmark_heatmap(payload: dict[str, Any], path: str | Path) -> None:
    heatmap = np.asarray(payload["heatmap"], dtype=float)
    fig, axis = plt.subplots(figsize=(9, 4.8))
    im = axis.imshow(heatmap, cmap="magma")
    axis.set_xticks(np.arange(len(payload["scenarios"])), payload["scenarios"], rotation=20)
    axis.set_yticks(np.arange(len(payload["controllers"])), payload["controllers"])
    axis.set_title("Benchmark risk heatmap")
    fig.colorbar(im, ax=axis, shrink=0.85, label="Risk score")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _plot_randomization_difficulty(payload: dict[str, Any], path: str | Path) -> None:
    rows = payload["episodes"][:12]
    labels = [str(row["episode"]) for row in rows]
    values = [row["difficulty_score"] for row in rows]
    fig, axis = plt.subplots(figsize=(10, 4.8))
    axis.bar(labels, values, color="#C85C2C")
    axis.set_title("Hardest randomized episodes")
    axis.set_xlabel("Episode")
    axis.set_ylabel("Difficulty score")
    axis.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _plot_parameter_effects(rows: list[dict[str, Any]], path: str | Path) -> None:
    labels = [row["parameter"] for row in rows]
    values = [row["correlation_with_difficulty"] for row in rows]
    colors = ["#C85C2C" if value >= 0 else "#3367D6" for value in values]
    fig, axis = plt.subplots(figsize=(9, 4.8))
    axis.bar(labels, values, color=colors)
    axis.axhline(0.0, color="black", linewidth=1)
    axis.set_title("Parameter correlation with episode difficulty")
    axis.set_ylabel("Correlation")
    axis.tick_params(axis="x", rotation=20)
    axis.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
