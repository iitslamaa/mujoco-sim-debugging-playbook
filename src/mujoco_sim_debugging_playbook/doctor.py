from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _parse_dependencies(pyproject_path: str | Path) -> list[str]:
    text = Path(pyproject_path).read_text()
    match = re.search(r"dependencies\s*=\s*\[(.*?)\]", text, re.DOTALL)
    if not match:
        return []
    entries = []
    for item in match.group(1).split(","):
        item = item.strip().strip('"').strip("'")
        if item:
            entries.append(item)
    return entries


def _check_tool_installed(tool_output: str | None) -> tuple[str, str]:
    if tool_output:
        return "pass", tool_output.splitlines()[0]
    return "warn", "not detected"


def build_environment_doctor_report(
    *,
    environment_report_path: str | Path,
    pyproject_path: str | Path,
    docker_compose_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    environment = _read_json(environment_report_path)
    dependencies = _parse_dependencies(pyproject_path)
    docker_compose_exists = Path(docker_compose_path).exists()

    checks: list[dict[str, str]] = []

    python_version = environment["platform"]["python_version"]
    checks.append(
        {
            "name": "python_version",
            "status": "pass" if python_version.startswith("3.10") or python_version.startswith("3.11") else "warn",
            "detail": f"Detected Python {python_version}",
        }
    )

    mujoco_version = environment["runtime"]["mujoco_version"]
    checks.append(
        {
            "name": "mujoco_runtime",
            "status": "pass" if mujoco_version else "fail",
            "detail": f"Detected MuJoCo {mujoco_version}",
        }
    )

    docker_status, docker_detail = _check_tool_installed(environment["tooling"].get("docker_version"))
    checks.append({"name": "docker_cli", "status": docker_status, "detail": docker_detail})

    gh_status, gh_detail = _check_tool_installed(environment["tooling"].get("gh_version"))
    checks.append({"name": "gh_cli", "status": gh_status, "detail": gh_detail})

    checks.append(
        {
            "name": "docker_compose_file",
            "status": "pass" if docker_compose_exists else "warn",
            "detail": "docker-compose.yml present" if docker_compose_exists else "docker-compose.yml missing",
        }
    )

    checks.append(
        {
            "name": "dependencies_declared",
            "status": "pass" if len(dependencies) >= 4 else "warn",
            "detail": f"{len(dependencies)} runtime dependencies declared",
        }
    )

    recommendations: list[str] = []
    if docker_status != "pass":
        recommendations.append("Install Docker Desktop or a compatible Docker engine to run the container workflow.")
    if gh_status != "pass":
        recommendations.append("Install GitHub CLI to reproduce issue and CI workflows locally.")
    if not docker_compose_exists:
        recommendations.append("Add a docker-compose.yml file to keep container entrypoints reproducible.")
    if not recommendations:
        recommendations.append("Environment looks healthy for local simulation, debugging, and support workflows.")

    status = "pass"
    if any(check["status"] == "fail" for check in checks):
        status = "fail"
    elif any(check["status"] == "warn" for check in checks):
        status = "warn"

    payload = {
        "summary": {
            "status": status,
            "check_count": len(checks),
            "warning_count": sum(1 for check in checks if check["status"] == "warn"),
            "failure_count": sum(1 for check in checks if check["status"] == "fail"),
            "repo_root": environment["workspace"]["repo_root"],
            "python_version": python_version,
            "mujoco_version": mujoco_version,
        },
        "checks": checks,
        "dependencies": dependencies,
        "recommendations": recommendations,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "doctor.json").write_text(json.dumps(payload, indent=2))
    (output / "doctor.md").write_text(render_environment_doctor_markdown(payload))
    return payload


def render_environment_doctor_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Environment Doctor",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Checks: `{payload['summary']['check_count']}`",
        f"- Warnings: `{payload['summary']['warning_count']}`",
        f"- Failures: `{payload['summary']['failure_count']}`",
        f"- Python: `{payload['summary']['python_version']}`",
        f"- MuJoCo: `{payload['summary']['mujoco_version']}`",
        "",
        "## Checks",
        "",
    ]
    for check in payload["checks"]:
        lines.append(f"- `{check['name']}`: `{check['status']}` | {check['detail']}")
    lines.extend(["", "## Recommendations", ""])
    for recommendation in payload["recommendations"]:
        lines.append(f"- {recommendation}")
    return "\n".join(lines)
