from __future__ import annotations

import json
from pathlib import Path


def build_support_case_catalog(*, support_cases_dir: str | Path, output_dir: str | Path) -> dict:
    cases = []
    for path in sorted(Path(support_cases_dir).glob("*.md")):
        lines = path.read_text().splitlines()
        title = lines[0].lstrip("# ").strip() if lines else path.stem
        cases.append({"case_id": path.stem, "title": title, "path": str(path)})
    payload = {"summary": {"case_count": len(cases)}, "cases": cases}
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "support_case_catalog.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "support_case_catalog.md").write_text(
        "# Support Case Catalog\n\n" + "\n".join(f"- `{c['case_id']}` | {c['title']}" for c in cases)
    )
    return payload
