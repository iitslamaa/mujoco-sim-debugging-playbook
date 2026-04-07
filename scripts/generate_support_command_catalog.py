from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_command_catalog import build_support_command_catalog


if __name__ == "__main__":
    build_support_command_catalog(
        setup_cheatsheet_path=ROOT / "docs" / "setup-command-cheatsheet.md",
        output_dir=ROOT / "outputs" / "support_command_catalog",
    )
