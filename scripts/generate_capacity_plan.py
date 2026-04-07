from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.capacity import build_capacity_plan


def main() -> None:
    payload = build_capacity_plan(
        sla_report_path=ROOT / "outputs" / "sla" / "sla_report.json",
        workstream_plan_path=ROOT / "outputs" / "workstreams" / "workstream_plan.json",
        support_ops_path=ROOT / "outputs" / "support_ops" / "support_ops.json",
        output_dir=ROOT / "outputs" / "capacity",
    )
    print(f"Capacity plan written to {ROOT / 'outputs' / 'capacity'}")
    print("Rebalance candidates:", payload["summary"]["rebalance_item_count"])


if __name__ == "__main__":
    main()
