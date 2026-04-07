from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_risk_register(
    *,
    anomaly_report_path: str | Path,
    support_readiness_path: str | Path,
    capacity_plan_path: str | Path,
) -> dict[str, Any]:
    anomalies = _read_json(anomaly_report_path)
    readiness = _read_json(support_readiness_path)
    capacity = _read_json(capacity_plan_path)

    risks = []
    for case in anomalies["benchmark_anomalies"]["top_cases"][:3]:
        risks.append(
            {
                "name": f"{case['scenario']} / {case['controller']}",
                "category": "simulation",
                "severity": float(case["risk_score"]),
                "message": f"Benchmark fragility remains elevated for {case['controller']} in {case['scenario']}.",
            }
        )
    for check in readiness["checks"]:
        if check["status"] in {"fail", "warn"}:
            risks.append(
                {
                    "name": check["name"],
                    "category": "readiness",
                    "severity": 1.0 if check["status"] == "fail" else 0.5,
                    "message": check["message"],
                }
            )
    for owner in capacity["owners"]:
        if owner["status"] == "overloaded":
            risks.append(
                {
                    "name": owner["owner"],
                    "category": "capacity",
                    "severity": float(owner["effort_points"]) / 10.0,
                    "message": f"{owner['owner']} is overloaded with {owner['effort_points']} effort points.",
                }
            )

    ordered = sorted(risks, key=lambda item: (-item["severity"], item["name"]))
    return {
        "summary": {"count": len(ordered), "top_risk": ordered[0]["name"] if ordered else None},
        "risks": ordered,
    }
