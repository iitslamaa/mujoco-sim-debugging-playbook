from __future__ import annotations

import json
from pathlib import Path
from typing import Any


COMMAND_MAP = {
    "dashboard/data.json": "python scripts/generate_dashboard.py",
    "outputs/support_readiness/support_readiness.json": "python scripts/generate_support_readiness.py",
    "outputs/scenario_plan/scenario_plan.json": "python scripts/generate_scenario_plan.py",
    "outputs/ops_review/ops_review.json": "python scripts/generate_ops_review.py",
    "outputs/scorecard/scorecard.json": "python scripts/generate_scorecard.py",
    "outputs/briefing_note/briefing_note.json": "python scripts/generate_briefing_note.py",
}


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_regeneration_plan(*, artifact_freshness_path: str | Path) -> dict[str, Any]:
    freshness = _read_json(artifact_freshness_path)
    actions = []
    for row in freshness["rows"]:
        if row["status"] == "fresh":
            continue
        priority = "high" if row["artifact"] == "dashboard/data.json" else "medium"
        actions.append(
            {
                "artifact": row["artifact"],
                "status": row["status"],
                "priority": priority,
                "command": COMMAND_MAP.get(row["artifact"], "regenerate artifact manually"),
                "age_delta_seconds": row["age_delta_seconds"],
            }
        )

    actions.sort(key=lambda item: (item["priority"] != "high", -(item["age_delta_seconds"] or 0)))
    return {
        "summary": {
            "count": len(actions),
            "high_priority_count": sum(1 for action in actions if action["priority"] == "high"),
        },
        "actions": actions,
    }
