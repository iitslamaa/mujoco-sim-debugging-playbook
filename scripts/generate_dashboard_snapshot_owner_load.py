from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_owner_load import (
    build_dashboard_snapshot_owner_load,
)


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_owner_load(
        dashboard_snapshot_execution_board_path=output_dir / "execution_board.json",
        dashboard_snapshot_alert_packet_path=output_dir / "alert_packet.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot owner load for "
        f"{payload['summary']['owner']} to {output_dir}"
    )


if __name__ == "__main__":
    main()
