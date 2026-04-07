from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_packet import build_artifact_packet


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_packet"
    payload = build_artifact_packet(
        artifact_scorecard_path=ROOT / "outputs" / "artifact_scorecard" / "artifact_scorecard.json",
        artifact_digest_path=ROOT / "outputs" / "artifact_digest" / "artifact_digest.json",
        artifact_handoff_path=ROOT / "outputs" / "artifact_handoff" / "artifact_handoff.json",
        artifact_closeout_path=ROOT / "outputs" / "artifact_closeout" / "artifact_closeout.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact packet for owner {payload['summary']['handoff_owner']} to {output_dir}")


if __name__ == "__main__":
    main()
