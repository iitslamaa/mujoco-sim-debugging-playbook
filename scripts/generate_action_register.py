from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.action_register import build_action_register


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Action Register",
        "",
        f"- Actions: `{payload['summary']['count']}`",
        "",
        "| priority | target | owner | action | reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in payload["actions"]:
        lines.append(
            f"| {item['priority']} | {item['target']} | {item['owner']} | {item['action']} | {item['reason']} |"
        )
    return "\n".join(lines)


def main() -> None:
    payload = build_action_register(
        ops_review_path=ROOT / "outputs" / "ops_review" / "ops_review.json",
        capacity_plan_path=ROOT / "outputs" / "capacity" / "capacity_plan.json",
    )
    output_dir = ROOT / "outputs" / "action_register"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "action_register.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "action_register.md").write_text(_render_markdown(payload))
    print(f"Action register written to {output_dir}")


if __name__ == "__main__":
    main()
