from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.responder_load import build_responder_load


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Responder Load",
        "",
        f"- Owners tracked: `{payload['summary']['owner_count']}`",
        f"- Highest-pressure owner: `{payload['summary']['top_owner']}`",
        "",
        "| owner | status | effort_points | breaches | at_risk | on_track | pressure_index |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['owner']} | {row['status']} | {row['effort_points']} | {row['breach_count']} | "
            f"{row['at_risk_count']} | {row['on_track_count']} | {row['pressure_index']:.1f} |"
        )
    return "\n".join(lines)


def main() -> None:
    payload = build_responder_load(
        capacity_plan_path=ROOT / "outputs" / "capacity" / "capacity_plan.json",
        sla_report_path=ROOT / "outputs" / "sla" / "sla_report.json",
    )
    output_dir = ROOT / "outputs" / "responder_load"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "responder_load.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "responder_load.md").write_text(_render_markdown(payload))
    print(f"Responder load written to {output_dir}")


if __name__ == "__main__":
    main()
