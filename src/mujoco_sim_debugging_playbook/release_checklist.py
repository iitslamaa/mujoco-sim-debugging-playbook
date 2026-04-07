from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_release_checklist(*, doctor_path: str | Path, compatibility_path: str | Path, output_dir: str | Path) -> dict:
    doctor = _read_json(doctor_path)
    compatibility = _read_json(compatibility_path)
    items = [
        {"name": "environment_doctor", "status": doctor["summary"]["status"]},
        {"name": "compatibility", "status": compatibility["summary"]["status"]},
        {"name": "warnings_reviewed", "status": "pass" if doctor["summary"]["warning_count"] <= 1 else "warn"},
    ]
    payload = {
        "summary": {
            "item_count": len(items),
            "pass_count": sum(1 for i in items if i["status"] == "pass"),
            "warn_count": sum(1 for i in items if i["status"] == "warn"),
        },
        "items": items,
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "release_checklist.json").write_text(json.dumps(payload, indent=2))
    (out / "release_checklist.md").write_text(
        "# Release Checklist\n\n" + "\n".join(f"- `{i['name']}`: `{i['status']}`" for i in items)
    )
    return payload
