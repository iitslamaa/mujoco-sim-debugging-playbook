from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.doctor import build_environment_doctor_report
from mujoco_sim_debugging_playbook.environment import capture_environment_report


def main() -> None:
    diagnostics_dir = ROOT / "outputs" / "diagnostics"
    diagnostics_dir.mkdir(parents=True, exist_ok=True)
    environment_path = diagnostics_dir / "environment.json"
    environment_path.write_text(json.dumps(capture_environment_report(ROOT), indent=2))

    output_dir = ROOT / "outputs" / "environment_doctor"
    payload = build_environment_doctor_report(
        environment_report_path=environment_path,
        pyproject_path=ROOT / "pyproject.toml",
        docker_compose_path=ROOT / "docker-compose.yml",
        output_dir=output_dir,
    )
    print(
        "Wrote environment doctor report with "
        f"{payload['summary']['check_count']} checks to {output_dir}"
    )


if __name__ == "__main__":
    main()
