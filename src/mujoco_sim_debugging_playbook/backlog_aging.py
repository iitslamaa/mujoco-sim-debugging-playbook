from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_backlog_aging(
    *,
    workstream_plan_path: str | Path,
    sla_report_path: str | Path,
) -> dict[str, Any]:
    workstreams = _read_json(workstream_plan_path)
    sla = _read_json(sla_report_path)
    workstream_lookup = {
        (lane["lane"], item["target"]): item
        for lane in workstreams["lanes"]
        for item in lane["items"]
    }

    rows = []
    bucket_counts = {"fresh": 0, "warming": 0, "stale": 0}
    for item in sla["items"]:
        workstream_item = workstream_lookup.get((item["lane"], item["target"]), {})
        effort_points = workstream_item.get("effort", {}).get("points", item["effort_points"])
        aging_score = float(
            item["due_in_days"]
            + effort_points
            + (3 if item["status"] == "breach" else 1 if item["status"] == "at_risk" else 0)
        )
        bucket = "fresh" if aging_score < 8 else "warming" if aging_score < 12 else "stale"
        bucket_counts[bucket] += 1
        rows.append(
            {
                "target": item["target"],
                "lane": item["lane"],
                "status": item["status"],
                "aging_score": aging_score,
                "bucket": bucket,
                "due_in_days": item["due_in_days"],
            }
        )

    ordered = sorted(rows, key=lambda row: (-row["aging_score"], row["target"]))
    return {
        "summary": {
            "item_count": len(ordered),
            "stale_count": bucket_counts["stale"],
            "oldest_target": ordered[0]["target"] if ordered else None,
        },
        "bucket_counts": bucket_counts,
        "rows": ordered,
    }
