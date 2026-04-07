from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_evidence_inventory(*, root: str | Path) -> dict[str, Any]:
    root = Path(root)
    outputs = root / "outputs"
    rows = []
    for path in sorted(outputs.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        rows.append(
            {
                "path": str(rel),
                "suffix": path.suffix or "<none>",
                "area": rel.parts[1] if len(rel.parts) > 1 else "unknown",
            }
        )
    return {
        "summary": {
            "file_count": len(rows),
            "area_count": len({row["area"] for row in rows}),
        },
        "rows": rows,
    }
