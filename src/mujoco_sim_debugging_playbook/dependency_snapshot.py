from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dependency_snapshot(
    *,
    environment_report_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    environment = _read_json(environment_report_path)
    packages = environment["workspace"].get("pip_freeze", [])

    payload = {
        "summary": {
            "package_count": len(packages),
            "python_version": environment["platform"]["python_version"],
        },
        "packages": packages,
    }

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "dependency_snapshot.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "dependency_snapshot.md").write_text(render_dependency_snapshot_markdown(payload))
    return payload


def render_dependency_snapshot_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dependency Snapshot",
        "",
        f"- Python: `{payload['summary']['python_version']}`",
        f"- Packages: `{payload['summary']['package_count']}`",
        "",
    ]
    for package in payload["packages"][:25]:
        lines.append(f"- {package}")
    return "\n".join(lines)
