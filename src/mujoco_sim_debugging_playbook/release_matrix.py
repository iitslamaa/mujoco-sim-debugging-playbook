from __future__ import annotations
import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_release_matrix(*, release_checklist_path: str | Path, compatibility_path: str | Path, output_dir: str | Path) -> dict:
    checklist = _read_json(release_checklist_path)
    compat = _read_json(compatibility_path)
    rows = [
        {"dimension": "release_checklist", "status": "pass" if checklist["summary"]["warn_count"] == 0 else "warn"},
        {"dimension": "compatibility", "status": compat["summary"]["status"]},
    ]
    payload = {"summary": {"row_count": len(rows)}, "rows": rows}
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "release_matrix.json").write_text(json.dumps(payload, indent=2))
    (out / "release_matrix.md").write_text("# Release Matrix\n\n" + "\n".join(f"- {r['dimension']}: `{r['status']}`" for r in rows))
    return payload
