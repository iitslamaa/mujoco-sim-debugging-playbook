from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_incident_bundles(
    *,
    triage_queue_path: str | Path,
    anomaly_report_path: str | Path,
    recommendation_report_path: str | Path,
    output_dir: str | Path,
    limit: int = 5,
) -> dict[str, Any]:
    triage = _read_json(triage_queue_path)
    anomalies = _read_json(anomaly_report_path)
    recommendations = _read_json(recommendation_report_path)

    rec_lookup = {item["target"]: item for item in recommendations["recommendations"]}
    anomaly_lookup = {
        **{f"{item['scenario']} / {item['controller']}": item for item in anomalies["benchmark_anomalies"]["top_cases"]},
        **{f"episode {item['episode']}": item for item in anomalies["randomization_anomalies"]["episodes"]},
    }

    bundles = []
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    for index, item in enumerate(triage["items"][:limit], start=1):
        recommendation = rec_lookup.get(item["target"])
        anomaly = anomaly_lookup.get(item["target"])
        slug = _slugify(item["target"])
        bundle = {
            "id": f"INC-{index:03d}",
            "target": item["target"],
            "kind": item["kind"],
            "priority_score": item["priority_score"],
            "summary": item["summary"],
            "evidence": item["evidence"],
            "next_action": item["next_action"],
            "recommendation": recommendation,
            "anomaly_context": anomaly,
            "bundle_path": f"outputs/incidents/{slug}.md",
        }
        bundles.append(bundle)
        (output / f"{slug}.json").write_text(json.dumps(bundle, indent=2))
        (output / f"{slug}.md").write_text(_render_bundle_markdown(bundle))

    payload = {
        "summary": {
            "count": len(bundles),
            "top_incident": bundles[0]["id"] if bundles else None,
        },
        "bundles": bundles,
    }
    (output / "index.json").write_text(json.dumps(payload, indent=2))
    (output / "index.md").write_text(_render_index_markdown(payload))
    return payload


def _slugify(value: str) -> str:
    slug = value.lower().replace(" / ", "_").replace(" ", "_").replace("-", "_")
    return "".join(ch for ch in slug if ch.isalnum() or ch == "_").strip("_")


def _render_bundle_markdown(bundle: dict[str, Any]) -> str:
    lines = [
        f"# Incident Bundle: {bundle['id']}",
        "",
        f"- Target: `{bundle['target']}`",
        f"- Kind: `{bundle['kind']}`",
        f"- Priority score: `{bundle['priority_score']:.2f}`",
        "",
        "## Summary",
        "",
        bundle["summary"],
        "",
        "## Evidence",
        "",
        bundle["evidence"],
        "",
        "## Next Action",
        "",
        bundle["next_action"],
        "",
    ]
    if bundle.get("recommendation"):
        lines.extend(
            [
                "## Recommendation Context",
                "",
                f"- Recommendation: {bundle['recommendation']['recommendation']}",
                f"- Tradeoff: {bundle['recommendation']['tradeoff']}",
                f"- Supporting evidence: {bundle['recommendation']['evidence']}",
                "",
            ]
        )
    if bundle.get("anomaly_context"):
        lines.extend(
            [
                "## Anomaly Context",
                "",
                f"```json\n{json.dumps(bundle['anomaly_context'], indent=2)}\n```",
                "",
            ]
        )
    return "\n".join(lines)


def _render_index_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Incident Bundles",
        "",
        f"Bundle count: `{payload['summary']['count']}`",
        "",
        "| id | target | kind | priority_score | bundle |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for bundle in payload["bundles"]:
        lines.append(
            f"| {bundle['id']} | {bundle['target']} | {bundle['kind']} | {bundle['priority_score']:.2f} | {bundle['bundle_path']} |"
        )
    return "\n".join(lines)
