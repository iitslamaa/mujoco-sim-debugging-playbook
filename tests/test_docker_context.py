import json

from mujoco_sim_debugging_playbook.docker_context import build_docker_context_report


def test_docker_context_extracts_base_image(tmp_path):
    environment_path = tmp_path / "environment.json"
    dockerfile_path = tmp_path / "Dockerfile"
    environment_path.write_text(json.dumps({"tooling": {"docker_version": "Docker version 1.0"}}))
    dockerfile_path.write_text("FROM python:3.10-slim\nRUN echo hi\n")

    payload = build_docker_context_report(
        environment_report_path=environment_path,
        dockerfile_path=dockerfile_path,
        output_dir=tmp_path,
    )

    assert payload["summary"]["base_image"] == "python:3.10-slim"
