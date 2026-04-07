from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _benchmark_winners(benchmark_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scenarios = sorted({row["scenario"] for row in benchmark_rows})
    winners = []
    for scenario in scenarios:
        rows = [row for row in benchmark_rows if row["scenario"] == scenario]
        ordered = sorted(rows, key=lambda item: (-item["success_rate"], item["final_error_mean"]))
        winners.append({"scenario": scenario, "winner": ordered[0], "rows": rows})
    return winners


def _randomization_summary(randomization_rows: list[dict[str, Any]]) -> list[dict[str, float | str]]:
    controllers = sorted({row["controller"] for row in randomization_rows})
    summary = []
    for controller in controllers:
        rows = [row for row in randomization_rows if row["controller"] == controller]
        summary.append(
            {
                "controller": controller,
                "success_rate": float(np.mean([row["success"] for row in rows])),
                "final_error_mean": float(np.mean([row["final_error"] for row in rows])),
                "control_energy_mean": float(np.mean([row["control_energy"] for row in rows])),
            }
        )
    return sorted(summary, key=lambda item: (-item["success_rate"], item["final_error_mean"]))


def _write_markdown_case_study(
    benchmark_rows: list[dict[str, Any]],
    randomization_rows: list[dict[str, Any]],
    output_path: str | Path,
) -> None:
    winners = _benchmark_winners(benchmark_rows)
    randomization = _randomization_summary(randomization_rows)

    lines = [
        "# Case Study: Controller Robustness Under Stress and Randomization",
        "",
        "This case study summarizes how different controller strategies behave under curated stress scenarios and randomized simulator conditions.",
        "",
        "## Main observations",
        "",
    ]

    for winner in winners:
        lines.append(
            f"- In `{winner['scenario']}`, the strongest controller was `{winner['winner']['controller']}` "
            f"with `{winner['winner']['success_rate']:.3f}` success rate and "
            f"`{winner['winner']['final_error_mean']:.4f}` mean final error."
        )

    lines.extend(
        [
            "",
            "## Domain-randomization summary",
            "",
            "| controller | success_rate | final_error_mean | control_energy_mean |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in randomization:
        lines.append(
            f"| {row['controller']} | {row['success_rate']:.3f} | "
            f"{row['final_error_mean']:.4f} | {row['control_energy_mean']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The expert controller remains a strong baseline in nominal settings.",
            "- The learned policy can match or exceed the expert in some noisy or aggressive regimes.",
            "- The hybrid controller is useful when robustness matters more than peak nominal efficiency.",
            "- Randomized evaluations reveal stability gaps that are easy to miss in fixed-scenario testing.",
            "",
            "## Suggested next investigations",
            "",
            "- Increase domain randomization during training instead of only at evaluation time.",
            "- Compare deterministic policy evaluation against stochastic rollout sampling.",
            "- Add explicit risk metrics for actuator saturation and recovery latency.",
            "",
        ]
    )
    Path(output_path).write_text("\n".join(lines))


def _plot_summary_card(
    benchmark_rows: list[dict[str, Any]],
    randomization_rows: list[dict[str, Any]],
    output_path: str | Path,
) -> None:
    winners = _benchmark_winners(benchmark_rows)
    randomization = _randomization_summary(randomization_rows)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    scenario_names = [item["scenario"] for item in winners]
    winner_scores = [item["winner"]["success_rate"] for item in winners]
    winner_labels = [item["winner"]["controller"] for item in winners]
    axes[0].bar(scenario_names, winner_scores, color="#2D6CDF")
    axes[0].set_ylim(0, 1.0)
    axes[0].set_ylabel("Success rate")
    axes[0].set_title("Best controller per stress scenario")
    axes[0].tick_params(axis="x", rotation=20)
    for idx, label in enumerate(winner_labels):
        axes[0].text(idx, winner_scores[idx] + 0.02, label, ha="center", va="bottom", fontsize=8)

    controllers = [row["controller"] for row in randomization]
    random_scores = [row["success_rate"] for row in randomization]
    axes[1].bar(controllers, random_scores, color="#C85C2C")
    axes[1].set_ylim(0, 1.0)
    axes[1].set_ylabel("Success rate")
    axes[1].set_title("Domain-randomization robustness")
    axes[1].tick_params(axis="x", rotation=20)

    fig.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def generate_case_studies(repo_root: str | Path) -> dict[str, str]:
    root = Path(repo_root)
    benchmark = _read_json(root / "outputs" / "controller_benchmark" / "benchmark_summary.json")
    randomization = _read_json(root / "outputs" / "domain_randomization" / "evaluation_rows.json")
    output_dir = root / "outputs" / "case_studies"
    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_path = output_dir / "controller_robustness_story.md"
    image_path = output_dir / "controller_robustness_story.png"
    _write_markdown_case_study(benchmark["benchmark_rows"], randomization["rows"], markdown_path)
    _plot_summary_card(benchmark["benchmark_rows"], randomization["rows"], image_path)
    return {
        "markdown": str(markdown_path),
        "image": str(image_path),
    }

