from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.artifact_delivery import build_artifact_delivery


def main() -> None:
    output_dir = ROOT / "outputs" / "artifact_delivery"
    payload = build_artifact_delivery(
        artifact_recovery_path=ROOT / "outputs" / "artifact_recovery" / "artifact_recovery.json",
        maintenance_risk_path=ROOT / "outputs" / "maintenance_risk" / "maintenance_risk.json",
        refresh_checklist_path=ROOT / "outputs" / "refresh_checklist" / "refresh_checklist.json",
        output_dir=output_dir,
    )
    print(f"Wrote artifact delivery forecast with {len(payload['phases'])} phases to {output_dir}")


if __name__ == "__main__":
    main()
