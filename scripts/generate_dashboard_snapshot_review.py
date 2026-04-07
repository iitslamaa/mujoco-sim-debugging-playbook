from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_review import build_dashboard_snapshot_review


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_review(
        dashboard_snapshot_monitor_path=output_dir / "monitor.json",
        dashboard_snapshot_alerts_path=output_dir / "alerts.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot review with "
        f"{payload['summary']['blocker_count']} blockers to {output_dir}"
    )


if __name__ == "__main__":
    main()
