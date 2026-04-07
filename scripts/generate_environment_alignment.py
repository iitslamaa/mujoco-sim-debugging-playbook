from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.environment_alignment import build_environment_alignment


if __name__ == "__main__":
    build_environment_alignment(
        environment_diff_path=ROOT / "outputs" / "environment_diff" / "environment_diff.json",
        toolchain_inventory_path=ROOT / "outputs" / "toolchain_inventory" / "toolchain_inventory.json",
        dependency_snapshot_path=ROOT / "outputs" / "dependency_snapshot" / "dependency_snapshot.json",
        output_dir=ROOT / "outputs" / "environment_alignment",
    )
