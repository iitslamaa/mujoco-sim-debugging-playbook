from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.response_rubric import build_response_rubric


def main() -> None:
    build_response_rubric(
        support_case_catalog_path=ROOT / "outputs" / "support_case_catalog" / "support_case_catalog.json",
        output_dir=ROOT / "outputs" / "response_rubric",
    )


if __name__ == "__main__":
    main()
