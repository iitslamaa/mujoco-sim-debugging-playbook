from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_environment_alignment(
    *,
    environment_diff_path: str | Path,
    toolchain_inventory_path: str | Path,
    dependency_snapshot_path: str | Path,
    output_dir: str | Path,
) -> dict:
    diff = _read_json(environment_diff_path)
    tools = _read_json(toolchain_inventory_path)
    deps = _read_json(dependency_snapshot_path)
    missing_tools = [entry["name"] for entry in tools["entries"] if entry["value"] == "not detected"]
    payload = {
        "summary": {
            "status": "pass" if diff["summary"]["warning_delta"] == 0 and not missing_tools else "warn",
            "warning_delta": diff["summary"]["warning_delta"],
            "missing_tool_count": len(missing_tools),
            "dependency_count": deps["summary"]["package_count"],
        },
        "missing_tools": missing_tools,
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "environment_alignment.json").write_text(json.dumps(payload, indent=2))
    (out / "environment_alignment.md").write_text(
        "# Environment Alignment\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Warning delta: `{payload['summary']['warning_delta']}`\n"
        f"- Missing tools: `{payload['summary']['missing_tool_count']}`\n"
        f"- Dependency count: `{payload['summary']['dependency_count']}`\n"
    )
    return payload
