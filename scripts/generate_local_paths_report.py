from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.local_paths_report import build_local_paths_report


def main() -> None:
    build_local_paths_report(repo_root=ROOT, output_dir=ROOT / "outputs" / "local_paths")


if __name__ == "__main__":
    main()
