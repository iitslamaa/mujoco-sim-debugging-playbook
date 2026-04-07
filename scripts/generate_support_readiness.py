from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.readiness import build_support_readiness_report


def main() -> None:
    payload = build_support_readiness_report(
        support_ops_path=ROOT / "outputs" / "support_ops" / "support_ops.json",
        support_gaps_path=ROOT / "outputs" / "support_gaps" / "support_gaps.json",
        sla_report_path=ROOT / "outputs" / "sla" / "sla_report.json",
        capacity_plan_path=ROOT / "outputs" / "capacity" / "capacity_plan.json",
        release_notes_path=ROOT / "outputs" / "releases" / "latest" / "release_notes.json",
        output_dir=ROOT / "outputs" / "support_readiness",
    )
    print(f"Support readiness report written to {ROOT / 'outputs' / 'support_readiness'}")
    print("Status:", payload["summary"]["status"])


if __name__ == "__main__":
    main()
