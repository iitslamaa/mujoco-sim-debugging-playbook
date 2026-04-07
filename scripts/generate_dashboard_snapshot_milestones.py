from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_milestones import (
    build_dashboard_snapshot_milestones,
)


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_milestones(
        dashboard_snapshot_recovery_forecast_path=output_dir / "recovery_forecast.json",
        dashboard_snapshot_scorecard_path=output_dir / "scorecard.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot milestones with "
        f"{payload['summary']['milestone_count']} milestones to {output_dir}"
    )


if __name__ == "__main__":
    main()
