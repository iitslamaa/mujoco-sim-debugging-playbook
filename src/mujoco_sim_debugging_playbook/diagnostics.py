from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DiagnosticSummary:
    label: str
    success_rate: float
    final_error_mean: float
    max_overshoot_mean: float
    oscillation_index_mean: float
    worst_episode: int | None
    worst_final_error: float | None
    most_oscillatory_episode: int | None
    most_oscillatory_value: float | None


def load_summary(summary_path: str | Path) -> dict[str, Any]:
    return json.loads(Path(summary_path).read_text())


def summarize_experiment(summary_payload: dict[str, Any], label: str) -> DiagnosticSummary:
    episodes = summary_payload.get("episodes", [])
    worst_episode = max(episodes, key=lambda row: row["final_error"]) if episodes else None
    most_oscillatory = max(episodes, key=lambda row: row["oscillation_index"]) if episodes else None
    summary = summary_payload["summary"]
    return DiagnosticSummary(
        label=label,
        success_rate=summary["success_rate"],
        final_error_mean=summary["final_error_mean"],
        max_overshoot_mean=summary["max_overshoot_mean"],
        oscillation_index_mean=summary["oscillation_index_mean"],
        worst_episode=worst_episode["episode"] if worst_episode else None,
        worst_final_error=worst_episode["final_error"] if worst_episode else None,
        most_oscillatory_episode=most_oscillatory["episode"] if most_oscillatory else None,
        most_oscillatory_value=most_oscillatory["oscillation_index"] if most_oscillatory else None,
    )


def compare_summaries(left: DiagnosticSummary, right: DiagnosticSummary) -> dict[str, float]:
    return {
        "success_rate_delta": right.success_rate - left.success_rate,
        "final_error_mean_delta": right.final_error_mean - left.final_error_mean,
        "max_overshoot_mean_delta": right.max_overshoot_mean - left.max_overshoot_mean,
        "oscillation_index_mean_delta": right.oscillation_index_mean - left.oscillation_index_mean,
    }


def render_diagnostic_markdown(
    environment: dict[str, Any],
    summaries: list[DiagnosticSummary],
    comparison_rows: list[dict[str, float]],
) -> str:
    lines = [
        "# Diagnostics Bundle",
        "",
        "Automatically generated environment and experiment diagnostics.",
        "",
        "## Environment",
        "",
        f"- Platform: `{environment['platform']['system']} {environment['platform']['release']}`",
        f"- Machine: `{environment['platform']['machine']}`",
        f"- Python: `{environment['platform']['python_version']}`",
        f"- MuJoCo: `{environment['runtime']['mujoco_version']}`",
        f"- NumPy: `{environment['runtime']['numpy_version']}`",
        f"- Git HEAD: `{environment['tooling']['git_head']}`",
        "",
        "## Experiment summaries",
        "",
        "| label | success_rate | final_error_mean | overshoot_mean | oscillation_mean | worst_episode |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in summaries:
        lines.append(
            f"| {item.label} | {item.success_rate:.3f} | {item.final_error_mean:.4f} | "
            f"{item.max_overshoot_mean:.4f} | {item.oscillation_index_mean:.4f} | "
            f"{item.worst_episode if item.worst_episode is not None else 'n/a'} |"
        )

    if comparison_rows:
        lines.extend(
            [
                "",
                "## Comparisons",
                "",
                "| baseline | candidate | success_delta | final_error_delta | overshoot_delta | oscillation_delta |",
                "| --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in comparison_rows:
            lines.append(
                f"| {row['left']} | {row['right']} | {row['success_rate_delta']:.3f} | "
                f"{row['final_error_mean_delta']:.4f} | {row['max_overshoot_mean_delta']:.4f} | "
                f"{row['oscillation_index_mean_delta']:.4f} |"
            )
    lines.append("")
    return "\n".join(lines)

