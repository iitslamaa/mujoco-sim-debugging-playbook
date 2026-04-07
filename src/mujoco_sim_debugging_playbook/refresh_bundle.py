from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_refresh_bundle(
    *,
    regeneration_plan_path: str | Path,
    impact_analysis_path: str | Path,
) -> dict[str, Any]:
    regeneration = _read_json(regeneration_plan_path)
    impact = _read_json(impact_analysis_path)
    impact_lookup = {row["dependency"]: row for row in impact["rows"]}

    bundles = []
    for action in regeneration["actions"]:
        dependency = action["artifact"]
        impact_row = impact_lookup.get(dependency, {"impact_count": 0, "impacted_artifacts": []})
        bundle_name = "dashboard_refresh" if action["artifact"] == "dashboard/data.json" else "support_report_refresh"
        bundles.append(
            {
                "bundle": bundle_name,
                "artifact": action["artifact"],
                "priority": action["priority"],
                "command": action["command"],
                "impact_count": impact_row["impact_count"],
                "impacted_artifacts": impact_row["impacted_artifacts"],
            }
        )

    bundle_summary: dict[str, dict[str, Any]] = {}
    for item in bundles:
        summary = bundle_summary.setdefault(
            item["bundle"],
            {"bundle": item["bundle"], "action_count": 0, "high_priority_count": 0, "max_impact_count": 0},
        )
        summary["action_count"] += 1
        if item["priority"] == "high":
            summary["high_priority_count"] += 1
        summary["max_impact_count"] = max(summary["max_impact_count"], item["impact_count"])

    return {
        "summary": {
            "bundle_count": len(bundle_summary),
            "action_count": len(bundles),
        },
        "bundles": sorted(bundle_summary.values(), key=lambda row: (-row["high_priority_count"], -row["action_count"], row["bundle"])),
        "actions": bundles,
    }


def render_refresh_bundle_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Refresh Bundles",
        "",
        f"- Bundles: `{payload['summary']['bundle_count']}`",
        f"- Actions: `{payload['summary']['action_count']}`",
        "",
        "| bundle | action_count | high_priority_count | max_impact_count |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in payload["bundles"]:
        lines.append(
            f"| {row['bundle']} | {row['action_count']} | {row['high_priority_count']} | {row['max_impact_count']} |"
        )
    lines.extend(["", "## Bundle Actions", ""])
    for row in payload["actions"]:
        lines.append(f"- `{row['bundle']}`: {row['artifact']} via `{row['command']}`")
    return "\n".join(lines)


def write_refresh_bundle(
    *,
    regeneration_plan_path: str | Path,
    impact_analysis_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    payload = build_refresh_bundle(
        regeneration_plan_path=regeneration_plan_path,
        impact_analysis_path=impact_analysis_path,
    )
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "refresh_bundle.json").write_text(json.dumps(payload, indent=2))
    (output / "refresh_bundle.md").write_text(render_refresh_bundle_markdown(payload))
    return payload
