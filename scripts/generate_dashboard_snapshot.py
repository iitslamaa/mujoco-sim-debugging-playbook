from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshots import build_dashboard_snapshot


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot(
        dashboard_data_path=ROOT / "dashboard" / "data.json",
        artifact_packet_path=ROOT / "outputs" / "artifact_packet" / "artifact_packet.json",
        output_dir=output_dir,
        snapshot_name="latest",
    )
    print(f"Wrote dashboard snapshot {payload['name']} to {output_dir}")


if __name__ == "__main__":
    main()
