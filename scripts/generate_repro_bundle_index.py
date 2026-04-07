from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.repro_bundle_index import build_repro_bundle_index


if __name__ == "__main__":
    build_repro_bundle_index(
        repro_inventory_path=ROOT / "outputs" / "repro_inventory" / "repro_inventory.json",
        debug_bundle_manifest_path=ROOT / "outputs" / "debug_bundle_manifest" / "debug_bundle_manifest.json",
        output_dir=ROOT / "outputs" / "repro_bundle_index",
    )
