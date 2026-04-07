from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.dependency_snapshot import build_dependency_snapshot


def main() -> None:
    payload = build_dependency_snapshot(
        environment_report_path=ROOT / "outputs" / "diagnostics" / "environment.json",
        output_dir=ROOT / "outputs" / "dependency_snapshot",
    )
    print(
        "Wrote dependency snapshot with "
        f"{payload['summary']['package_count']} packages to {ROOT / 'outputs' / 'dependency_snapshot'}"
    )


if __name__ == "__main__":
    main()
