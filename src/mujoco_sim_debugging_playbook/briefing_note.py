from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_briefing_note(
    *,
    scorecard_path: str | Path,
    ops_review_path: str | Path,
    scenario_plan_path: str | Path,
) -> dict[str, Any]:
    scorecard = _read_json(scorecard_path)
    ops_review = _read_json(ops_review_path)
    scenario_plan = _read_json(scenario_plan_path)
    best_scenario = next((scenario["name"] for scenario in scenario_plan["scenarios"] if scenario["status"] == "pass"), "none")
    return {
        "summary": {
            "headline": f"Support state is {ops_review['summary']['breach_count']} breaches away from stable operations.",
            "best_scenario": best_scenario,
        },
        "cards": scorecard["cards"][:3],
        "wins": ops_review["wins"][:2],
        "risks": ops_review["risks"][:2],
    }
