from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.compatibility import build_compatibility_report


def main() -> None:
    payload = build_compatibility_report(
        environment_report_path=ROOT / "outputs" / "diagnostics" / "environment.json",
        output_dir=ROOT / "outputs" / "compatibility",
    )
    print(
        "Wrote compatibility report with "
        f"{payload['summary']['check_count']} checks to {ROOT / 'outputs' / 'compatibility'}"
    )


if __name__ == "__main__":
    main()
