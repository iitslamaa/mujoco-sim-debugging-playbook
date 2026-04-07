from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_toolchain_inventory(*, environment_report_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    environment = _read_json(environment_report_path)
    entries = [
        ("python", environment["platform"]["python_version"]),
        ("mujoco", environment["runtime"]["mujoco_version"]),
        ("numpy", environment["runtime"]["numpy_version"]),
        ("docker", environment["tooling"].get("docker_version") or "not detected"),
        ("gh", environment["tooling"].get("gh_version") or "not detected"),
    ]
    payload = {"summary": {"tool_count": len(entries)}, "entries": [{"name": k, "value": v} for k, v in entries]}
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "toolchain_inventory.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "toolchain_inventory.md").write_text(
        "# Toolchain Inventory\n\n" + "\n".join(f"- `{e['name']}`: {e['value']}" for e in payload["entries"])
    )
    return payload
