from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.owner_alerts import build_owner_alerts


def _render_markdown(payload: dict) -> str:
    lines = ["# Owner Alerts", "", f"- Alerts: `{payload['summary']['count']}`", ""]
    for alert in payload["alerts"]:
        lines.append(f"## {alert['owner']}")
        lines.append("")
        lines.append(f"- Severity: `{alert['severity']}`")
        lines.append(f"- {alert['message']}")
        for target in alert["targets"]:
            lines.append(f"- target: {target}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    payload = build_owner_alerts(
        capacity_plan_path=ROOT / "outputs" / "capacity" / "capacity_plan.json",
        sla_report_path=ROOT / "outputs" / "sla" / "sla_report.json",
    )
    output_dir = ROOT / "outputs" / "owner_alerts"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "owner_alerts.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "owner_alerts.md").write_text(_render_markdown(payload))
    print(f"Owner alerts written to {output_dir}")


if __name__ == "__main__":
    main()
