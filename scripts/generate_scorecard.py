from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.scorecard import build_scorecard


def _render_markdown(payload: dict) -> str:
    lines = ["# Support Scorecard", "", "| label | value |", "| --- | --- |"]
    for card in payload["cards"]:
        lines.append(f"| {card['label']} | {card['value']} |")
    return "\n".join(lines)


def main() -> None:
    payload = build_scorecard(
        support_ops_path=ROOT / "outputs" / "support_ops" / "support_ops.json",
        support_readiness_path=ROOT / "outputs" / "support_readiness" / "support_readiness.json",
        scenario_plan_path=ROOT / "outputs" / "scenario_plan" / "scenario_plan.json",
    )
    output_dir = ROOT / "outputs" / "scorecard"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "scorecard.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "scorecard.md").write_text(_render_markdown(payload))
    print(f"Scorecard written to {output_dir}")


if __name__ == "__main__":
    main()
