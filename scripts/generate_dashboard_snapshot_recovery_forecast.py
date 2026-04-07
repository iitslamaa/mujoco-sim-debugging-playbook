from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_recovery_forecast import (
    build_dashboard_snapshot_recovery_forecast,
)


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_recovery_forecast(
        dashboard_snapshot_readiness_gate_path=output_dir / "readiness_gate.json",
        dashboard_snapshot_resolution_plan_path=output_dir / "resolution_plan.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot recovery forecast with projected status "
        f"{payload['summary']['projected_next_status']} to {output_dir}"
    )


if __name__ == "__main__":
    main()
