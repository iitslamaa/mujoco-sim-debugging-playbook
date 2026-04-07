from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_responder_load(
    *,
    capacity_plan_path: str | Path,
    sla_report_path: str | Path,
) -> dict[str, Any]:
    capacity = _read_json(capacity_plan_path)
    sla = _read_json(sla_report_path)

    owner_records: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "owner": "",
            "effort_points": 0,
            "breach_count": 0,
            "at_risk_count": 0,
            "on_track_count": 0,
            "targets": [],
        }
    )

    for item in sla["items"]:
        record = owner_records[item["owner"]]
        record["owner"] = item["owner"]
        record["effort_points"] += item["effort_points"]
        record["targets"].append(item["target"])
        if item["status"] == "breach":
            record["breach_count"] += 1
        elif item["status"] == "at_risk":
            record["at_risk_count"] += 1
        else:
            record["on_track_count"] += 1

    overload_lookup = {item["owner"]: item for item in capacity["owners"]}
    rows = []
    for owner, record in owner_records.items():
        overload = overload_lookup.get(owner, {})
        rows.append(
            {
                **record,
                "status": overload.get("status", "healthy"),
                "pressure_index": float(record["effort_points"] + 3 * record["breach_count"] + record["at_risk_count"]),
            }
        )

    ordered = sorted(rows, key=lambda row: (-row["pressure_index"], row["owner"]))
    return {
        "summary": {
            "owner_count": len(ordered),
            "top_owner": ordered[0]["owner"] if ordered else None,
        },
        "rows": ordered,
    }
