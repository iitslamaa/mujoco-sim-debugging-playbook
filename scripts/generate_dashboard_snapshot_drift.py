from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_drift import build_dashboard_snapshot_drift


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_drift(
        dashboard_snapshot_history_path=ROOT / "outputs" / "dashboard_snapshots" / "history.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot drift with "
        f"{payload['summary']['transition_count']} transitions to {output_dir}"
    )


if __name__ == "__main__":
    main()
