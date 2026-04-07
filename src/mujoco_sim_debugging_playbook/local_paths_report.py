from __future__ import annotations

import json
from pathlib import Path


def build_local_paths_report(*, repo_root: str | Path, output_dir: str | Path) -> dict:
    root = Path(repo_root)
    payload = {
        "summary": {"path_count": 5},
        "paths": [
            {"name": "repo_root", "path": str(root)},
            {"name": "outputs", "path": str(root / "outputs")},
            {"name": "support_cases", "path": str(root / "outputs" / "support_cases")},
            {"name": "dashboard", "path": str(root / "dashboard")},
            {"name": "scripts", "path": str(root / "scripts")},
        ],
    }
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "local_paths_report.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "local_paths_report.md").write_text(
        "# Local Paths Report\n\n" + "\n".join(f"- `{p['name']}`: {p['path']}" for p in payload["paths"])
    )
    return payload
