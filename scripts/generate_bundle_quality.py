from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.bundle_quality import build_bundle_quality


if __name__ == "__main__":
    build_bundle_quality(
        bundle_manifest_path=ROOT / "outputs" / "debug_bundle_manifest" / "debug_bundle_manifest.json",
        bundle_verifier_path=ROOT / "outputs" / "bundle_verifier" / "bundle_verifier.json",
        output_dir=ROOT / "outputs" / "bundle_quality",
    )
