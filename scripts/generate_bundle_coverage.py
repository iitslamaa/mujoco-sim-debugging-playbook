from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.bundle_coverage import build_bundle_coverage


if __name__ == "__main__":
    build_bundle_coverage(
        bundle_quality_path=ROOT / "outputs" / "bundle_quality" / "bundle_quality.json",
        repro_bundle_index_path=ROOT / "outputs" / "repro_bundle_index" / "repro_bundle_index.json",
        output_dir=ROOT / "outputs" / "bundle_coverage",
    )
