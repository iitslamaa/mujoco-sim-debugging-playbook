from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_sla_report(
    *,
    workstream_plan_path: str | Path,
    support_ops_path: str | Path,
    output_dir: str | Path,
    today: date | None = None,
) -> dict[str, Any]:
    workstreams = _read_json(workstream_plan_path)
    support_ops = _read_json(support_ops_path)
    today = today or date.today()

    items: list[dict[str, Any]] = []
    lane_summaries: list[dict[str, Any]] = []
    open_queue = support_ops["summary"]["queue_count"]
    base_capacity = max(3, min(8, open_queue // 2))

    for lane in workstreams["lanes"]:
        lane_capacity = max(2, base_capacity - lane["blocking_count"])
        cumulative_days = 0
        lane_items = []
        for item in lane["items"]:
            estimated_days = max(1, item["effort"]["points"] // 2)
            if item["blocking"]:
                estimated_days += 1
            cumulative_days += estimated_days
            due_date = today + timedelta(days=cumulative_days)
            status = _status_for_item(item, cumulative_days)
            record = {
                "lane": lane["lane"],
                "target": item["target"],
                "severity": item["severity"],
                "blocking": item["blocking"],
                "effort_points": item["effort"]["points"],
                "estimated_days": estimated_days,
                "due_in_days": cumulative_days,
                "due_date": due_date.isoformat(),
                "status": status,
                "owner": item["owner"],
                "deliverable": item["deliverable"],
            }
            lane_items.append(record)
            items.append(record)

        lane_summaries.append(
            {
                "lane": lane["lane"],
                "item_count": len(lane_items),
                "blocking_count": lane["blocking_count"],
                "estimated_days_total": sum(item["estimated_days"] for item in lane_items),
                "lane_capacity_points_per_week": lane_capacity,
                "at_risk_count": sum(1 for item in lane_items if item["status"] == "at_risk"),
                "breach_count": sum(1 for item in lane_items if item["status"] == "breach"),
            }
        )

    ordered_items = sorted(items, key=lambda item: (_status_rank(item["status"]), item["due_in_days"], -item["effort_points"]))
    payload = {
        "summary": {
            "item_count": len(ordered_items),
            "at_risk_count": sum(1 for item in ordered_items if item["status"] == "at_risk"),
            "breach_count": sum(1 for item in ordered_items if item["status"] == "breach"),
            "next_due_target": ordered_items[0]["target"] if ordered_items else None,
            "slowest_lane": max(lane_summaries, key=lambda lane: lane["estimated_days_total"])["lane"] if lane_summaries else None,
        },
        "lanes": lane_summaries,
        "items": ordered_items,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "sla_report.json").write_text(json.dumps(payload, indent=2))
    (output / "sla_report.md").write_text(_render_markdown(payload))
    return payload


def _status_for_item(item: dict[str, Any], due_in_days: int) -> str:
    if item["severity"] == "high" and item["blocking"] and due_in_days > 2:
        return "breach"
    if item["severity"] == "high" and due_in_days > 4:
        return "breach"
    if item["severity"] == "critical" and due_in_days > 2:
        return "breach"
    if item["blocking"] and due_in_days > 2:
        return "at_risk"
    if due_in_days > 5:
        return "at_risk"
    return "on_track"


def _status_rank(status: str) -> int:
    order = {"breach": 0, "at_risk": 1, "on_track": 2}
    return order.get(status, 99)


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Support Delivery Forecast",
        "",
        f"- Planned items: `{payload['summary']['item_count']}`",
        f"- At risk: `{payload['summary']['at_risk_count']}`",
        f"- Breaches: `{payload['summary']['breach_count']}`",
        f"- Next due target: `{payload['summary']['next_due_target']}`",
        f"- Slowest lane: `{payload['summary']['slowest_lane']}`",
        "",
        "## Lane Summary",
        "",
        "| lane | items | blocking | estimated_days_total | at_risk | breaches |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for lane in payload["lanes"]:
        lines.append(
            f"| {lane['lane']} | {lane['item_count']} | {lane['blocking_count']} | "
            f"{lane['estimated_days_total']} | {lane['at_risk_count']} | {lane['breach_count']} |"
        )

    lines.extend(["", "## Item Forecast", "", "| status | due_date | target | severity | effort_points | deliverable |", "| --- | --- | --- | --- | ---: | --- |"])
    for item in payload["items"]:
        lines.append(
            f"| {item['status']} | {item['due_date']} | {item['target']} | {item['severity']} | "
            f"{item['effort_points']} | {item['deliverable']} |"
        )
    return "\n".join(lines)
