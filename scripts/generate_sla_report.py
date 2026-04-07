from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.sla import build_sla_report


def main() -> None:
    payload = build_sla_report(
        workstream_plan_path=ROOT / "outputs" / "workstreams" / "workstream_plan.json",
        support_ops_path=ROOT / "outputs" / "support_ops" / "support_ops.json",
        output_dir=ROOT / "outputs" / "sla",
    )
    print(f"SLA report written to {ROOT / 'outputs' / 'sla'}")
    print("At-risk items:", payload["summary"]["at_risk_count"])


if __name__ == "__main__":
    main()
