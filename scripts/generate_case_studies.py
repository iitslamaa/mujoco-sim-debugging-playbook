from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.case_studies import generate_case_studies


def main() -> None:
    outputs = generate_case_studies(ROOT)
    print(f"Case study markdown: {outputs['markdown']}")
    print(f"Case study image: {outputs['image']}")


if __name__ == "__main__":
    main()

