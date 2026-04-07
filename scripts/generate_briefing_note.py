from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.briefing_note import build_briefing_note


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Briefing Note",
        "",
        payload["summary"]["headline"],
        "",
        f"Best recovery scenario: `{payload['summary']['best_scenario']}`",
        "",
        "## KPI Snapshot",
        "",
    ]
    for card in payload["cards"]:
        lines.append(f"- {card['label']}: {card['value']}")
    lines.extend(["", "## Wins", ""])
    for item in payload["wins"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Risks", ""])
    for item in payload["risks"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def main() -> None:
    payload = build_briefing_note(
        scorecard_path=ROOT / "outputs" / "scorecard" / "scorecard.json",
        ops_review_path=ROOT / "outputs" / "ops_review" / "ops_review.json",
        scenario_plan_path=ROOT / "outputs" / "scenario_plan" / "scenario_plan.json",
    )
    output_dir = ROOT / "outputs" / "briefing_note"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "briefing_note.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "briefing_note.md").write_text(_render_markdown(payload))
    print(f"Briefing note written to {output_dir}")


if __name__ == "__main__":
    main()
