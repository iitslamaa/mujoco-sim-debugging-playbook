from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_monitor import build_dashboard_snapshot_monitor


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_monitor(
        dashboard_snapshot_history_path=output_dir / "history.json",
        dashboard_snapshot_drift_path=output_dir / "drift.json",
        dashboard_snapshot_alerts_path=output_dir / "alerts.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot monitor with "
        f"{payload['summary']['headline_count']} headlines to {output_dir}"
    )


if __name__ == "__main__":
    main()
