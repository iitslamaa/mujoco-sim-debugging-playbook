from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.bundle_verifier import build_bundle_verifier


if __name__ == "__main__":
    build_bundle_verifier(bundle_manifest_path=ROOT / "outputs" / "debug_bundle_manifest" / "debug_bundle_manifest.json", output_dir=ROOT / "outputs" / "bundle_verifier")
