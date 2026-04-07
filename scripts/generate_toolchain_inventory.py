from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.toolchain_inventory import build_toolchain_inventory


def main() -> None:
    build_toolchain_inventory(
        environment_report_path=ROOT / "outputs" / "diagnostics" / "environment.json",
        output_dir=ROOT / "outputs" / "toolchain_inventory",
    )


if __name__ == "__main__":
    main()
