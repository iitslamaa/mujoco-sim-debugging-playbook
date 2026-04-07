from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STATUS_WEIGHT = {
    "fresh": 0.0,
    "stale": 1.0,
    "missing": 1.4,
}

PRIORITY_WEIGHT = {
    "high": 1.35,
    "medium": 1.0,
    "low": 0.75,
}


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _normalize_age(age_delta_seconds: float | None) -> float:
    if age_delta_seconds is None:
        return 1.0
    return min(max(age_delta_seconds, 0.0) / 3600.0, 12.0) / 12.0


def build_maintenance_risk(
    *,
    artifact_freshness_path: str | Path,
    regeneration_plan_path: str | Path,
    impact_analysis_path: str | Path,
    refresh_bundle_path: str | Path,
) -> dict[str, Any]:
    freshness = _read_json(artifact_freshness_path)
    regeneration = _read_json(regeneration_plan_path)
    impact = _read_json(impact_analysis_path)
    refresh_bundle = _read_json(refresh_bundle_path)

    freshness_lookup = {row["artifact"]: row for row in freshness["rows"]}
    regen_lookup = {row["artifact"]: row for row in regeneration["actions"]}
    impact_lookup = {row["dependency"]: row for row in impact["rows"]}

    bundle_lookup: dict[str, list[dict[str, Any]]] = {}
    for row in refresh_bundle["actions"]:
        bundle_lookup.setdefault(row["artifact"], []).append(row)

    rows = []
    for artifact, fresh_row in sorted(freshness_lookup.items()):
        action = regen_lookup.get(
            artifact,
            {
                "priority": "low",
                "command": "no regeneration action recorded",
                "age_delta_seconds": fresh_row.get("age_delta_seconds"),
            },
        )
        impact_row = impact_lookup.get(artifact, {"impact_count": 0, "impacted_artifacts": []})
        bundles = bundle_lookup.get(artifact, [])
        bundle_names = sorted({row["bundle"] for row in bundles})

        status_weight = STATUS_WEIGHT.get(fresh_row["status"], 0.5)
        priority_weight = PRIORITY_WEIGHT.get(action["priority"], 1.0)
        impact_factor = 1.0 + min(impact_row["impact_count"], 6) * 0.18
        age_factor = 1.0 + _normalize_age(action.get("age_delta_seconds")) * 0.35
        bundle_factor = 1.0 + max(len(bundle_names) - 1, 0) * 0.15
        risk_score = round(status_weight * priority_weight * impact_factor * age_factor * bundle_factor, 3)

        rows.append(
            {
                "artifact": artifact,
                "status": fresh_row["status"],
                "priority": action["priority"],
                "risk_score": risk_score,
                "impact_count": impact_row["impact_count"],
                "bundle_count": len(bundle_names),
                "bundles": bundle_names,
                "command": action["command"],
                "age_delta_seconds": action.get("age_delta_seconds"),
            }
        )

    rows.sort(key=lambda row: (-row["risk_score"], -row["impact_count"], row["artifact"]))
    high_risk = [row for row in rows if row["risk_score"] >= 1.5]
    medium_risk = [row for row in rows if 0.75 <= row["risk_score"] < 1.5]

    return {
        "summary": {
            "artifact_count": len(rows),
            "high_risk_count": len(high_risk),
            "medium_risk_count": len(medium_risk),
            "top_risk_artifact": rows[0]["artifact"] if rows else None,
            "top_risk_score": rows[0]["risk_score"] if rows else 0.0,
        },
        "rows": rows,
    }


def render_maintenance_risk_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Maintenance Risk",
        "",
        f"- Artifacts scored: `{payload['summary']['artifact_count']}`",
        f"- High risk: `{payload['summary']['high_risk_count']}`",
        f"- Medium risk: `{payload['summary']['medium_risk_count']}`",
        f"- Top risk artifact: `{payload['summary']['top_risk_artifact']}`",
        f"- Top risk score: `{payload['summary']['top_risk_score']:.3f}`",
        "",
        "| artifact | status | priority | risk_score | impact_count | bundle_count |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['artifact']} | {row['status']} | {row['priority']} | "
            f"{row['risk_score']:.3f} | {row['impact_count']} | {row['bundle_count']} |"
        )
    lines.extend(["", "## Top Risks", ""])
    for row in payload["rows"][:8]:
        bundles = ", ".join(row["bundles"]) if row["bundles"] else "none"
        lines.append(
            f"- `{row['artifact']}`: score `{row['risk_score']:.3f}`, "
            f"status `{row['status']}`, priority `{row['priority']}`, bundles `{bundles}`"
        )
    return "\n".join(lines)


def write_maintenance_risk(
    *,
    artifact_freshness_path: str | Path,
    regeneration_plan_path: str | Path,
    impact_analysis_path: str | Path,
    refresh_bundle_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    payload = build_maintenance_risk(
        artifact_freshness_path=artifact_freshness_path,
        regeneration_plan_path=regeneration_plan_path,
        impact_analysis_path=impact_analysis_path,
        refresh_bundle_path=refresh_bundle_path,
    )
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "maintenance_risk.json").write_text(json.dumps(payload, indent=2))
    (output / "maintenance_risk.md").write_text(render_maintenance_risk_markdown(payload))
    return payload
