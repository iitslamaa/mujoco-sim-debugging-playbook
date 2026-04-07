from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_action_register(
    *,
    ops_review_path: str | Path,
    capacity_plan_path: str | Path,
) -> dict[str, Any]:
    ops_review = _read_json(ops_review_path)
    capacity = _read_json(capacity_plan_path)
    rebalance_lookup = {item["target"]: item for item in capacity["rebalance_items"]}
    actions = []
    for item in ops_review["next_actions"]:
        rebalance = rebalance_lookup.get(item["target"], {})
        actions.append(
            {
                "target": item["target"],
                "owner": item["owner"],
                "action": item["action"],
                "reason": item["reason"],
                "priority": "high" if rebalance.get("status") == "breach" else "medium",
            }
        )
    return {
        "summary": {"count": len(actions)},
        "actions": actions,
    }
