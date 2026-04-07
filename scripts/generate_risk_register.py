from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.risk_register import build_risk_register


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Risk Register",
        "",
        f"- Risks tracked: `{payload['summary']['count']}`",
        f"- Top risk: `{payload['summary']['top_risk']}`",
        "",
        "| name | category | severity | message |",
        "| --- | --- | ---: | --- |",
    ]
    for risk in payload["risks"]:
        lines.append(f"| {risk['name']} | {risk['category']} | {risk['severity']:.2f} | {risk['message']} |")
    return "\n".join(lines)


def main() -> None:
    payload = build_risk_register(
        anomaly_report_path=ROOT / "outputs" / "anomalies" / "anomaly_report.json",
        support_readiness_path=ROOT / "outputs" / "support_readiness" / "support_readiness.json",
        capacity_plan_path=ROOT / "outputs" / "capacity" / "capacity_plan.json",
    )
    output_dir = ROOT / "outputs" / "risk_register"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "risk_register.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "risk_register.md").write_text(_render_markdown(payload))
    print(f"Risk register written to {output_dir}")


if __name__ == "__main__":
    main()
