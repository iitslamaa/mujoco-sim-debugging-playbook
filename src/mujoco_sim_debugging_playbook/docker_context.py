from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_docker_context_report(
    *,
    environment_report_path: str | Path,
    dockerfile_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    environment = _read_json(environment_report_path)
    dockerfile_lines = Path(dockerfile_path).read_text().splitlines()

    payload = {
        "summary": {
            "docker_detected": bool(environment["tooling"].get("docker_version")),
            "dockerfile_line_count": len(dockerfile_lines),
            "base_image": dockerfile_lines[0].replace("FROM ", "") if dockerfile_lines else "unknown",
        },
        "docker_version": environment["tooling"].get("docker_version"),
        "dockerfile_preview": dockerfile_lines[:12],
    }

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "docker_context.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "docker_context.md").write_text(render_docker_context_markdown(payload))
    return payload


def render_docker_context_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Docker Context",
        "",
        f"- Docker detected: `{payload['summary']['docker_detected']}`",
        f"- Dockerfile lines: `{payload['summary']['dockerfile_line_count']}`",
        f"- Base image: `{payload['summary']['base_image']}`",
    ]
    if payload["docker_version"]:
        lines.append(f"- Docker version: `{payload['docker_version']}`")
    lines.extend(["", "## Dockerfile Preview", ""])
    for line in payload["dockerfile_preview"]:
        lines.append(f"- {line}")
    return "\n".join(lines)
