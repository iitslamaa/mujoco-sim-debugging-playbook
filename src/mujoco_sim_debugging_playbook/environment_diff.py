from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_environment_diff(*, doctor_path: str | Path, compatibility_path: str | Path, output_dir: str | Path) -> dict:
    doctor = _read_json(doctor_path)
    compatibility = _read_json(compatibility_path)
    payload = {
        "summary": {
            "doctor_status": doctor["summary"]["status"],
            "compatibility_status": compatibility["summary"]["status"],
            "warning_delta": doctor["summary"]["warning_count"] - compatibility["summary"]["warn_count"],
        }
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "environment_diff.json").write_text(json.dumps(payload, indent=2))
    (out / "environment_diff.md").write_text(
        "# Environment Diff\n\n"
        f"- Doctor status: `{payload['summary']['doctor_status']}`\n"
        f"- Compatibility status: `{payload['summary']['compatibility_status']}`\n"
        f"- Warning delta: `{payload['summary']['warning_delta']}`\n"
    )
    return payload
