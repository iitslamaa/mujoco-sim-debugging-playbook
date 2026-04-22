from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.application_bundle import build_application_bundle


if __name__ == "__main__":
    payload = build_application_bundle(
        repo_root=ROOT,
        output_dir=ROOT / "outputs" / "application_bundle",
    )
    print(f"Wrote application bundle with {payload['summary']['item_count']} items")
