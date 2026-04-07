from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dashboard_snapshot_actions import build_dashboard_snapshot_actions


def main() -> None:
    output_dir = ROOT / "outputs" / "dashboard_snapshots"
    payload = build_dashboard_snapshot_actions(
        dashboard_snapshot_digest_path=output_dir / "digest.json",
        dashboard_snapshot_closeout_path=output_dir / "closeout.json",
        output_dir=output_dir,
    )
    print(
        "Wrote dashboard snapshot actions with "
        f"{payload['summary']['action_count']} actions to {output_dir}"
    )


if __name__ == "__main__":
    main()
