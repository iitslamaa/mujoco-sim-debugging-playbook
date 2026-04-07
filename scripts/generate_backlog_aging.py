from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.backlog_aging import build_backlog_aging


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Backlog Aging",
        "",
        f"- Items tracked: `{payload['summary']['item_count']}`",
        f"- Stale items: `{payload['summary']['stale_count']}`",
        f"- Oldest target: `{payload['summary']['oldest_target']}`",
        "",
        "| target | bucket | due_in_days | aging_score | status |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['target']} | {row['bucket']} | {row['due_in_days']} | {row['aging_score']:.1f} | {row['status']} |"
        )
    return "\n".join(lines)


def main() -> None:
    payload = build_backlog_aging(
        workstream_plan_path=ROOT / "outputs" / "workstreams" / "workstream_plan.json",
        sla_report_path=ROOT / "outputs" / "sla" / "sla_report.json",
    )
    output_dir = ROOT / "outputs" / "backlog_aging"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "backlog_aging.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "backlog_aging.md").write_text(_render_markdown(payload))
    print(f"Backlog aging written to {output_dir}")


if __name__ == "__main__":
    main()
