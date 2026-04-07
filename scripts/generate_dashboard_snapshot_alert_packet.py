from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_alert_packet import build_dashboard_snapshot_alert_packet


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_alert_packet(
        dashboard_snapshot_actions_path=output_dir / "actions.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot alert packet with "
        f"{payload['summary']['alert_count']} alerts to {output_dir}"
    )


if __name__ == "__main__":
    main()
