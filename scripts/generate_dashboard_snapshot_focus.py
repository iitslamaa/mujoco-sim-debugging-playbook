from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_focus import (
    build_dashboard_snapshot_focus,
)


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_focus(
        dashboard_snapshot_watchlist_path=output_dir / "watchlist.json",
        dashboard_snapshot_readiness_gate_path=output_dir / "readiness_gate.json",
        dashboard_snapshot_milestones_path=output_dir / "milestones.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot focus with "
        f"{payload['summary']['focus_item_count']} items to {output_dir}"
    )


if __name__ == "__main__":
    main()
