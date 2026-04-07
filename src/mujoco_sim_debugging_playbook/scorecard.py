from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_scorecard(
    *,
    support_ops_path: str | Path,
    support_readiness_path: str | Path,
    scenario_plan_path: str | Path,
) -> dict[str, Any]:
    support_ops = _read_json(support_ops_path)
    support_readiness = _read_json(support_readiness_path)
    scenario_plan = _read_json(scenario_plan_path)
    return {
        "cards": [
            {"label": "Queue", "value": support_ops["summary"]["queue_count"]},
            {"label": "KB coverage", "value": round(100 * support_ops["summary"]["knowledge_base_coverage"], 1)},
            {"label": "Status", "value": support_readiness["summary"]["status"]},
            {"label": "Best scenario", "value": next((scenario["name"] for scenario in scenario_plan["scenarios"] if scenario["status"] == "pass"), "none")},
        ]
    }
