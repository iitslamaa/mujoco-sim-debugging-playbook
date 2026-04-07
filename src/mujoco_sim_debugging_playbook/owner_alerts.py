from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_owner_alerts(
    *,
    capacity_plan_path: str | Path,
    sla_report_path: str | Path,
) -> dict[str, Any]:
    capacity = _read_json(capacity_plan_path)
    sla = _read_json(sla_report_path)
    items_by_owner: dict[str, list[dict[str, Any]]] = {}
    for item in sla["items"]:
        items_by_owner.setdefault(item["owner"], []).append(item)

    alerts = []
    for owner in capacity["owners"]:
        if owner["status"] != "overloaded":
            continue
        items = sorted(items_by_owner.get(owner["owner"], []), key=lambda item: (item["status"] != "breach", -item["effort_points"]))
        alerts.append(
            {
                "owner": owner["owner"],
                "severity": "high" if owner["breach_count"] > 0 else "medium",
                "message": f"{owner['owner']} has {owner['breach_count']} breaches and {owner['at_risk_count']} at-risk items.",
                "targets": [item["target"] for item in items[:3]],
            }
        )

    return {
        "summary": {"count": len(alerts)},
        "alerts": alerts,
    }
