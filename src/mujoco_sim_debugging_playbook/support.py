from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SupportCase:
    slug: str
    title: str
    summary: str
    user_report: str
    reproduction_command: str
    parameter_of_interest: str
    recommended_checks: list[str]
    recommended_response_points: list[str]


def _load_support_case(path: Path) -> SupportCase:
    payload = json.loads(path.read_text())
    return SupportCase(**payload)


def _load_combined_summary(repo_root: Path) -> list[dict[str, Any]]:
    summary_path = repo_root / "outputs" / "interesting_sweeps" / "combined_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(
            f"Missing {summary_path}. Run scripts/run_sweep.py --config configs/interesting_sweeps.json first."
        )
    return json.loads(summary_path.read_text())


def _parameter_rows(rows: list[dict[str, Any]], parameter: str) -> list[dict[str, Any]]:
    return sorted([row for row in rows if row["parameter"] == parameter], key=lambda item: item["value"])


def _render_markdown(case: SupportCase, parameter_rows: list[dict[str, Any]]) -> str:
    best_success = max(parameter_rows, key=lambda item: item["success_rate"])
    worst_success = min(parameter_rows, key=lambda item: item["success_rate"])
    highest_overshoot = max(parameter_rows, key=lambda item: item["max_overshoot_mean"])

    lines = [
        f"# Support Case: {case.title}",
        "",
        "## User report",
        "",
        case.user_report,
        "",
        "## Reproduction",
        "",
        f"```bash\n{case.reproduction_command}\n```",
        "",
        "## Investigation checklist",
        "",
    ]
    lines.extend([f"- {item}" for item in case.recommended_checks])
    lines.extend(
        [
            "",
            "## Observed sweep summary",
            "",
            f"- Parameter: `{case.parameter_of_interest}`",
            f"- Best success rate: `{best_success['value']}` -> `{best_success['success_rate']:.3f}`",
            f"- Worst success rate: `{worst_success['value']}` -> `{worst_success['success_rate']:.3f}`",
            f"- Highest overshoot: `{highest_overshoot['value']}` -> `{highest_overshoot['max_overshoot_mean']:.4f}`",
            "",
            "| value | success_rate | final_error_mean | overshoot_mean | oscillation_mean |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in parameter_rows:
        lines.append(
            f"| {row['value']} | {row['success_rate']:.3f} | {row['final_error_mean']:.4f} | "
            f"{row['max_overshoot_mean']:.4f} | {row['oscillation_index_mean']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Suggested support response",
            "",
            "Thanks for the detailed report. I was able to reproduce the behavior with the documented sweep outputs.",
            "",
        ]
    )
    lines.extend([f"- {item}" for item in case.recommended_response_points])
    lines.extend(
        [
            "",
            "## Next actions",
            "",
            "- Re-run the baseline and the relevant sweep while keeping the same seed.",
            "- Compare the generated plot and `combined_summary.json` for this parameter.",
            "- If the behavior still looks surprising, inspect one per-episode trace and tune one variable at a time.",
            "",
        ]
    )
    return "\n".join(lines)


def run_support_case(case_slug: str, repo_root: str | Path) -> Path:
    root = Path(repo_root)
    case_path = root / "cases" / "issue_cases" / f"{case_slug}.json"
    if not case_path.exists():
        available = ", ".join(sorted(path.stem for path in (root / "cases" / "issue_cases").glob("*.json")))
        raise FileNotFoundError(f"Unknown case '{case_slug}'. Available cases: {available}")

    case = _load_support_case(case_path)
    rows = _load_combined_summary(root)
    parameter_rows = _parameter_rows(rows, case.parameter_of_interest)
    markdown = _render_markdown(case, parameter_rows)

    output_path = root / "outputs" / "support_cases" / f"{case.slug}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)
    return output_path

