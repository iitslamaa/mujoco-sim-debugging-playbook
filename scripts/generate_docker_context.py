from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.docker_context import build_docker_context_report


def main() -> None:
    payload = build_docker_context_report(
        environment_report_path=ROOT / "outputs" / "diagnostics" / "environment.json",
        dockerfile_path=ROOT / "Dockerfile",
        output_dir=ROOT / "outputs" / "docker_context",
    )
    print(
        "Wrote docker context report for "
        f"{payload['summary']['base_image']} to {ROOT / 'outputs' / 'docker_context'}"
    )


if __name__ == "__main__":
    main()
