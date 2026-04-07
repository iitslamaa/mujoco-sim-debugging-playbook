from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.repro_inventory import build_repro_inventory


def main() -> None:
    payload = build_repro_inventory(
        support_cases_dir=ROOT / "outputs" / "support_cases",
        output_dir=ROOT / "outputs" / "repro_inventory",
    )
    print(
        "Wrote repro inventory with "
        f"{payload['summary']['case_count']} cases to {ROOT / 'outputs' / 'repro_inventory'}"
    )


if __name__ == "__main__":
    main()
