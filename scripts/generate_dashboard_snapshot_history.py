from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_history import build_dashboard_snapshot_history


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_history(
        dashboard_snapshot_path=ROOT / "outputs" / "dashboard_snapshots" / "latest.json",
        artifact_history_path=ROOT / "outputs" / "artifact_history" / "artifact_history.json",
        output_dir=output_dir,
    )
    print(f"Wrote dashboard snapshot history with {payload['summary']['snapshot_count']} entries to {output_dir}")


if __name__ == "__main__":
    main()
