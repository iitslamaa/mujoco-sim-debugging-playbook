from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_case_catalog import build_support_case_catalog


def main() -> None:
    build_support_case_catalog(
        support_cases_dir=ROOT / "outputs" / "support_cases",
        output_dir=ROOT / "outputs" / "support_case_catalog",
    )


if __name__ == "__main__":
    main()
