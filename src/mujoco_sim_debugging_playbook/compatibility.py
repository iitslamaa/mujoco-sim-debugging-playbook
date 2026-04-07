from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_compatibility_report(
    *,
    environment_report_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    environment = _read_json(environment_report_path)

    python_version = environment["platform"]["python_version"]
    docker_present = bool(environment["tooling"].get("docker_version"))
    gh_present = bool(environment["tooling"].get("gh_version"))

    checks = [
        {
            "name": "python_supported",
            "status": "pass" if python_version.startswith("3.10") or python_version.startswith("3.11") else "warn",
            "detail": f"Detected Python {python_version}",
        },
        {
            "name": "mujoco_detected",
            "status": "pass" if environment["runtime"]["mujoco_version"] else "fail",
            "detail": f"Detected MuJoCo {environment['runtime']['mujoco_version']}",
        },
        {
            "name": "docker_available",
            "status": "pass" if docker_present else "warn",
            "detail": environment["tooling"].get("docker_version") or "Docker not detected",
        },
        {
            "name": "gh_available",
            "status": "pass" if gh_present else "warn",
            "detail": environment["tooling"].get("gh_version") or "GitHub CLI not detected",
        },
    ]

    payload = {
        "summary": {
            "status": "pass" if all(item["status"] == "pass" for item in checks) else "warn",
            "check_count": len(checks),
            "pass_count": sum(1 for item in checks if item["status"] == "pass"),
            "warn_count": sum(1 for item in checks if item["status"] == "warn"),
        },
        "checks": checks,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "compatibility.json").write_text(json.dumps(payload, indent=2))
    (output / "compatibility.md").write_text(render_compatibility_markdown(payload))
    return payload


def render_compatibility_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Compatibility Report",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Checks: `{payload['summary']['check_count']}`",
        f"- Passes: `{payload['summary']['pass_count']}`",
        f"- Warnings: `{payload['summary']['warn_count']}`",
        "",
    ]
    for item in payload["checks"]:
        lines.append(f"- `{item['name']}`: `{item['status']}` | {item['detail']}")
    return "\n".join(lines)
