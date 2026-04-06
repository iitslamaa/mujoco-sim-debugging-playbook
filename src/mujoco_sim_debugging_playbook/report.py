from __future__ import annotations

from collections import defaultdict
from pathlib import Path


def _trend_sentence(rows: list[dict]) -> str:
    sorted_rows = sorted(rows, key=lambda item: item["value"])
    best_success = max(sorted_rows, key=lambda item: item["success_rate"])
    worst_success = min(sorted_rows, key=lambda item: item["success_rate"])
    highest_overshoot = max(sorted_rows, key=lambda item: item["max_overshoot_mean"])
    return (
        f"Best success rate appears at `{best_success['value']}` ({best_success['success_rate']:.2f}), "
        f"worst success rate appears at `{worst_success['value']}` ({worst_success['success_rate']:.2f}), "
        f"and the largest overshoot appears at `{highest_overshoot['value']}` "
        f"({highest_overshoot['max_overshoot_mean']:.4f})."
    )


def write_markdown_report(rows: list[dict], path: str | Path, title: str) -> None:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["parameter"]].append(row)

    lines = [
        f"# {title}",
        "",
        "Automatically generated sweep summary for the MuJoCo reaching experiments.",
        "",
    ]

    for parameter, parameter_rows in sorted(grouped.items()):
        lines.extend(
            [
                f"## {parameter}",
                "",
                _trend_sentence(parameter_rows),
                "",
                "| value | success_rate | final_error_mean | overshoot_mean | oscillation_mean | control_energy_mean |",
                "| --- | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in sorted(parameter_rows, key=lambda item: item["value"]):
            lines.append(
                "| "
                f"{row['value']} | "
                f"{row['success_rate']:.3f} | "
                f"{row['final_error_mean']:.4f} | "
                f"{row['max_overshoot_mean']:.4f} | "
                f"{row['oscillation_index_mean']:.4f} | "
                f"{row['control_energy_mean']:.4f} |"
            )
        lines.append("")

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines))

