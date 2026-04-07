from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.diagnostics import (
    compare_summaries,
    load_summary,
    render_diagnostic_markdown,
    summarize_experiment,
)
from mujoco_sim_debugging_playbook.environment import capture_environment_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a diagnostics bundle from one or more experiment summaries.")
    parser.add_argument("--summary", action="append", required=True, help="Path to a summary.json file.")
    parser.add_argument("--label", action="append", required=True, help="Human-readable label matching each summary.")
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "diagnostics"), help="Output directory.")
    args = parser.parse_args()

    if len(args.summary) != len(args.label):
        raise SystemExit("Pass the same number of --summary and --label arguments.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summaries = [
        summarize_experiment(load_summary(summary_path), label)
        for summary_path, label in zip(args.summary, args.label)
    ]
    comparison_rows = []
    if len(summaries) >= 2:
        baseline = summaries[0]
        for candidate in summaries[1:]:
            row = compare_summaries(baseline, candidate)
            row["left"] = baseline.label
            row["right"] = candidate.label
            comparison_rows.append(row)

    environment = capture_environment_report(ROOT)
    markdown = render_diagnostic_markdown(environment, summaries, comparison_rows)
    (output_dir / "diagnostics.md").write_text(markdown)
    (output_dir / "environment.json").write_text(json.dumps(environment, indent=2))
    print(f"Diagnostics bundle written to {output_dir}")


if __name__ == "__main__":
    main()

