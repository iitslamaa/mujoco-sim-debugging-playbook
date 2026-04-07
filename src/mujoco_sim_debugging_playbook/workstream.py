from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_workstream_plan(
    *,
    support_gaps_path: str | Path,
    triage_queue_path: str | Path,
    recommendations_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    support_gaps = _read_json(support_gaps_path)
    triage = _read_json(triage_queue_path)
    recommendations = _read_json(recommendations_path)

    triage_lookup = {item["target"]: item for item in triage["items"]}
    recommendation_lookup = {item["target"]: item for item in recommendations["recommendations"]}

    workstreams: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in support_gaps["items"]:
        if not item["missing_artifacts"]:
            continue

        triage_item = triage_lookup.get(item["target"], {})
        recommendation = recommendation_lookup.get(item["target"])
        lane = _lane_for_item(item)
        effort = _effort_for_item(item)
        blocking = item["severity"] in {"critical", "high"} or item["gap_score"] >= 35
        workstreams[lane].append(
            {
                "target": item["target"],
                "kind": item["kind"],
                "severity": item["severity"],
                "owner": item["owner"],
                "priority_score": item["priority_score"],
                "gap_score": item["gap_score"],
                "effort": effort,
                "blocking": blocking,
                "deliverable": _deliverable_for_item(item),
                "rationale": triage_item.get("summary") or recommendation.get("evidence") if recommendation else item["next_best_asset"],
                "recommended_action": recommendation["recommendation"] if recommendation else item["next_best_asset"],
            }
        )

    lanes = []
    for lane, items in sorted(workstreams.items()):
        ordered_items = sorted(items, key=lambda item: (-item["blocking"], -item["gap_score"], -item["priority_score"]))
        lanes.append(
            {
                "lane": lane,
                "item_count": len(ordered_items),
                "blocking_count": sum(1 for item in ordered_items if item["blocking"]),
                "estimated_points": sum(item["effort"]["points"] for item in ordered_items),
                "items": ordered_items,
            }
        )

    payload = {
        "summary": {
            "lane_count": len(lanes),
            "item_count": sum(lane["item_count"] for lane in lanes),
            "blocking_count": sum(lane["blocking_count"] for lane in lanes),
            "estimated_points": sum(lane["estimated_points"] for lane in lanes),
            "top_lane": lanes[0]["lane"] if lanes else None,
        },
        "lanes": lanes,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "workstream_plan.json").write_text(json.dumps(payload, indent=2))
    (output / "workstream_plan.md").write_text(_render_markdown(payload))
    return payload


def _lane_for_item(item: dict[str, Any]) -> str:
    missing = set(item["missing_artifacts"])
    if "incident_bundle" in missing:
        return "incident_backfill"
    if "knowledge_base_entry" in missing:
        return "self_serve_docs"
    if "mitigation_recommendation" in missing:
        return "mitigation_design"
    return "queue_hygiene"


def _effort_for_item(item: dict[str, Any]) -> dict[str, Any]:
    missing_count = len(item["missing_artifacts"])
    points = max(1, missing_count * 2)
    if item["severity"] == "critical":
        points += 1
    elif item["severity"] == "high":
        points += 1
    size = "small" if points <= 2 else "medium" if points <= 4 else "large"
    return {"points": points, "size": size}


def _deliverable_for_item(item: dict[str, Any]) -> str:
    missing = set(item["missing_artifacts"])
    if "incident_bundle" in missing:
        return "Create a reproducible incident bundle and attach trace evidence."
    if "knowledge_base_entry" in missing:
        return "Publish a knowledge-base article once the mitigation is validated."
    if "mitigation_recommendation" in missing:
        return "Add a mitigation recommendation tied to benchmark or sweep evidence."
    return "Audit queue metadata and keep the item aligned with owners and severity."


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Support Workstream Plan",
        "",
        f"- Active lanes: `{payload['summary']['lane_count']}`",
        f"- Planned items: `{payload['summary']['item_count']}`",
        f"- Blocking items: `{payload['summary']['blocking_count']}`",
        f"- Estimated points: `{payload['summary']['estimated_points']}`",
        f"- Top lane: `{payload['summary']['top_lane']}`",
        "",
    ]

    for lane in payload["lanes"]:
        lines.extend(
            [
                f"## {lane['lane']}",
                "",
                f"- Items: `{lane['item_count']}`",
                f"- Blocking: `{lane['blocking_count']}`",
                f"- Estimated points: `{lane['estimated_points']}`",
                "",
                "| severity | target | effort | deliverable | recommended_action |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in lane["items"]:
            effort = f"{item['effort']['size']} ({item['effort']['points']} pts)"
            lines.append(
                f"| {item['severity']} | {item['target']} | {effort} | "
                f"{item['deliverable']} | {item['recommended_action']} |"
            )
        lines.extend(["", "### Rationale", ""])
        for item in lane["items"]:
            lines.append(f"- `{item['target']}`: {item['rationale']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
