from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_readiness_gate import (
    build_dashboard_snapshot_readiness_gate,
)


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_readiness_gate(
        dashboard_snapshot_owner_load_path=output_dir / "owner_load.json",
        dashboard_snapshot_closeout_path=output_dir / "closeout.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot readiness gate with status "
        f"{payload['summary']['status']} to {output_dir}"
    )


if __name__ == "__main__":
    main()
