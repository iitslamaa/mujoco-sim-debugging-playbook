from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_documentation_audit(
    *,
    support_ops_path: str | Path,
    support_gaps_path: str | Path,
    knowledge_base_path: str | Path,
) -> dict[str, Any]:
    support_ops = _read_json(support_ops_path)
    support_gaps = _read_json(support_gaps_path)
    knowledge_base = _read_json(knowledge_base_path)

    kb_targets = {entry["target"] for entry in knowledge_base["entries"]}
    uncovered = [item["target"] for item in support_gaps["items"] if item["missing_artifacts"]]
    coverage = support_ops["summary"]["knowledge_base_coverage"]

    return {
        "summary": {
            "knowledge_base_coverage": coverage,
            "entry_count": len(knowledge_base["entries"]),
            "uncovered_count": len(uncovered),
        },
        "covered_targets": sorted(kb_targets),
        "uncovered_targets": sorted(uncovered),
    }
