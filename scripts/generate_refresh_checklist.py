from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.refresh_checklist import write_refresh_checklist


def main() -> None:
    payload = write_refresh_checklist(
        refresh_bundle_path=ROOT / "outputs" / "refresh_bundle" / "refresh_bundle.json",
        output_dir=ROOT / "outputs" / "refresh_checklist",
    )
    print(f"Refresh checklist written to {ROOT / 'outputs' / 'refresh_checklist'}")
    print("Steps:", payload["summary"]["total_steps"])


if __name__ == "__main__":
    main()
