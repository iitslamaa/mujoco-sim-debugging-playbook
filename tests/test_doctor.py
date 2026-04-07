import json

from mujoco_sim_debugging_playbook.doctor import build_environment_doctor_report


def test_environment_doctor_flags_missing_tools_and_declared_dependencies(tmp_path):
    environment_path = tmp_path / "environment.json"
    pyproject_path = tmp_path / "pyproject.toml"
    docker_compose_path = tmp_path / "docker-compose.yml"

    environment_path.write_text(
        json.dumps(
            {
                "platform": {"python_version": "3.10.14"},
                "runtime": {"mujoco_version": "3.2.7"},
                "tooling": {"docker_version": None, "gh_version": "gh version 2.80.0"},
                "workspace": {"repo_root": "/tmp/example"},
            }
        )
    )
    pyproject_path.write_text(
        """
[project]
dependencies = ["mujoco>=3.2.0", "numpy>=1.26.0", "matplotlib>=3.8.0", "torch>=2.11.0"]
""".strip()
    )

    payload = build_environment_doctor_report(
        environment_report_path=environment_path,
        pyproject_path=pyproject_path,
        docker_compose_path=docker_compose_path,
        output_dir=tmp_path,
    )

    assert payload["summary"]["status"] == "warn"
    assert payload["summary"]["warning_count"] >= 1
    assert "Docker" in payload["recommendations"][0]
