from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.regeneration_plan import build_regeneration_plan


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Regeneration Plan",
        "",
        f"- Actions: `{payload['summary']['count']}`",
        f"- High priority: `{payload['summary']['high_priority_count']}`",
        "",
        "| priority | artifact | command |",
        "| --- | --- | --- |",
    ]
    for action in payload["actions"]:
        lines.append(f"| {action['priority']} | {action['artifact']} | {action['command']} |")
    return "\n".join(lines)


def main() -> None:
    payload = build_regeneration_plan(
        artifact_freshness_path=ROOT / "outputs" / "artifact_freshness" / "artifact_freshness.json",
    )
    output_dir = ROOT / "outputs" / "regeneration_plan"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "regeneration_plan.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "regeneration_plan.md").write_text(_render_markdown(payload))
    print(f"Regeneration plan written to {output_dir}")


if __name__ == "__main__":
    main()
