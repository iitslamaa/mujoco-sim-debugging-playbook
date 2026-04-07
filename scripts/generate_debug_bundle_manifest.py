from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.debug_bundle_manifest import build_debug_bundle_manifest


def main() -> None:
    build_debug_bundle_manifest(
        bundle_root=ROOT / "outputs" / "debug_bundle",
        output_dir=ROOT / "outputs" / "debug_bundle_manifest",
    )


if __name__ == "__main__":
    main()
