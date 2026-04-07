from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_capacity_plan(
    *,
    sla_report_path: str | Path,
    workstream_plan_path: str | Path,
    support_ops_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    sla = _read_json(sla_report_path)
    workstreams = _read_json(workstream_plan_path)
    support_ops = _read_json(support_ops_path)

    workload_by_owner: Counter[str] = Counter()
    effort_by_lane: Counter[str] = Counter()
    item_lookup = {
        (lane["lane"], item["target"]): item
        for lane in workstreams["lanes"]
        for item in lane["items"]
    }
    owner_items: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for item in sla["items"]:
        workload_by_owner[item["owner"]] += item["effort_points"]
        effort_by_lane[item["lane"]] += item["effort_points"]
        owner_items[item["owner"]].append(item)

    overloaded_owners = []
    for owner, effort_points in workload_by_owner.items():
        breach_count = sum(1 for item in owner_items[owner] if item["status"] == "breach")
        at_risk_count = sum(1 for item in owner_items[owner] if item["status"] == "at_risk")
        overloaded = breach_count > 0 or effort_points >= 10
        overloaded_owners.append(
            {
                "owner": owner,
                "effort_points": effort_points,
                "breach_count": breach_count,
                "at_risk_count": at_risk_count,
                "status": "overloaded" if overloaded else "healthy",
            }
        )

    lane_actions = []
    for lane in sla["lanes"]:
        lane_items = [item for item in sla["items"] if item["lane"] == lane["lane"]]
        primary_owner = lane_items[0]["owner"] if lane_items else "unassigned"
        suggested_capacity_shift = max(0, lane["breach_count"] * 2 + lane["at_risk_count"])
        lane_actions.append(
            {
                "lane": lane["lane"],
                "current_effort_points": effort_by_lane[lane["lane"]],
                "breach_count": lane["breach_count"],
                "at_risk_count": lane["at_risk_count"],
                "primary_owner": primary_owner,
                "suggested_capacity_shift": suggested_capacity_shift,
                "action": _lane_action_for_counts(lane["breach_count"], lane["at_risk_count"]),
            }
        )

    rebalance_items = []
    for item in sla["items"]:
        if item["status"] == "on_track":
            continue
        source_owner = item["owner"]
        recommended_owner = _recommended_owner(item)
        workstream_item = item_lookup.get((item["lane"], item["target"]), {})
        rebalance_items.append(
            {
                "target": item["target"],
                "status": item["status"],
                "current_owner": source_owner,
                "recommended_owner": recommended_owner,
                "lane": item["lane"],
                "effort_points": item["effort_points"],
                "handoff_reason": _handoff_reason(item),
                "recommended_action": workstream_item.get("recommended_action") or item["deliverable"],
            }
        )

    payload = {
        "summary": {
            "queue_count": support_ops["summary"]["queue_count"],
            "owner_count": len(overloaded_owners),
            "overloaded_owner_count": sum(1 for owner in overloaded_owners if owner["status"] == "overloaded"),
            "lane_count": len(lane_actions),
            "rebalance_item_count": len(rebalance_items),
            "highest_pressure_lane": max(lane_actions, key=lambda item: item["suggested_capacity_shift"])["lane"] if lane_actions else None,
        },
        "owners": sorted(overloaded_owners, key=lambda item: (- (item["status"] == "overloaded"), -item["effort_points"], item["owner"])),
        "lanes": sorted(lane_actions, key=lambda item: (-item["suggested_capacity_shift"], item["lane"])),
        "rebalance_items": sorted(rebalance_items, key=lambda item: (item["status"] != "breach", -item["effort_points"], item["target"])),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "capacity_plan.json").write_text(json.dumps(payload, indent=2))
    (output / "capacity_plan.md").write_text(_render_markdown(payload))
    return payload


def _lane_action_for_counts(breach_count: int, at_risk_count: int) -> str:
    if breach_count > 0:
        return "Reassign one blocking item immediately and split the lane across additional owners."
    if at_risk_count >= 2:
        return "Pre-stage documentation or incident scaffolding to reduce turnaround time."
    return "Keep the lane under observation and preserve current staffing."


def _recommended_owner(item: dict[str, Any]) -> str:
    if item["lane"] == "incident_backfill":
        return "simulation-debugging"
    if item["lane"] == "self_serve_docs":
        return "maintainer-review"
    return item["owner"]


def _handoff_reason(item: dict[str, Any]) -> str:
    if item["status"] == "breach":
        return "Current owner has a breaching item and should offload work to keep the queue moving."
    return "This item is at risk and benefits from parallel evidence gathering."


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Support Capacity Plan",
        "",
        f"- Queue count: `{payload['summary']['queue_count']}`",
        f"- Owners tracked: `{payload['summary']['owner_count']}`",
        f"- Overloaded owners: `{payload['summary']['overloaded_owner_count']}`",
        f"- Lanes tracked: `{payload['summary']['lane_count']}`",
        f"- Rebalance candidates: `{payload['summary']['rebalance_item_count']}`",
        f"- Highest-pressure lane: `{payload['summary']['highest_pressure_lane']}`",
        "",
        "## Owner Pressure",
        "",
        "| owner | status | effort_points | breaches | at_risk |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for owner in payload["owners"]:
        lines.append(
            f"| {owner['owner']} | {owner['status']} | {owner['effort_points']} | "
            f"{owner['breach_count']} | {owner['at_risk_count']} |"
        )

    lines.extend(["", "## Lane Actions", "", "| lane | pressure_shift | breaches | at_risk | action |", "| --- | ---: | ---: | ---: | --- |"])
    for lane in payload["lanes"]:
        lines.append(
            f"| {lane['lane']} | {lane['suggested_capacity_shift']} | {lane['breach_count']} | "
            f"{lane['at_risk_count']} | {lane['action']} |"
        )

    lines.extend(["", "## Rebalance Candidates", "", "| status | target | current_owner | recommended_owner | effort_points | handoff_reason |", "| --- | --- | --- | --- | ---: | --- |"])
    for item in payload["rebalance_items"]:
        lines.append(
            f"| {item['status']} | {item['target']} | {item['current_owner']} | {item['recommended_owner']} | "
            f"{item['effort_points']} | {item['handoff_reason']} |"
        )
    return "\n".join(lines)
