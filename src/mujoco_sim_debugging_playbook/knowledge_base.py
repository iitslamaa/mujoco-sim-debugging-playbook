from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_knowledge_base(
    *,
    incidents_index_path: str | Path,
    recommendations_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    incidents = _read_json(incidents_index_path)
    recommendations = _read_json(recommendations_path)

    rec_lookup = {item["target"]: item for item in recommendations["recommendations"]}
    entries = []
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    for bundle in incidents["bundles"]:
        recommendation = rec_lookup.get(bundle["target"])
        question = _question_for_bundle(bundle)
        answer = _answer_for_bundle(bundle, recommendation)
        slug = _slugify(bundle["target"])
        entry = {
            "id": bundle["id"],
            "target": bundle["target"],
            "question": question,
            "answer": answer,
            "article_path": f"outputs/knowledge_base/{slug}.md",
        }
        entries.append(entry)
        (output / f"{slug}.md").write_text(_render_article(entry, bundle, recommendation))

    payload = {
        "summary": {
            "count": len(entries),
        },
        "entries": entries,
    }
    (output / "index.json").write_text(json.dumps(payload, indent=2))
    (output / "index.md").write_text(_render_index(payload))
    return payload


def _question_for_bundle(bundle: dict[str, Any]) -> str:
    if bundle["kind"] == "randomized_episode":
        return f"Why does {bundle['target']} fail under randomized conditions?"
    if bundle["kind"] == "benchmark_case":
        return f"Why is {bundle['target']} a high-risk benchmark case?"
    return f"How should I handle {bundle['target']}?"


def _answer_for_bundle(bundle: dict[str, Any], recommendation: dict[str, Any] | None) -> str:
    action = recommendation["recommendation"] if recommendation else bundle["next_action"]
    return f"{bundle['summary']} Recommended first step: {action}"


def _slugify(value: str) -> str:
    slug = value.lower().replace(" / ", "_").replace(" ", "_").replace("-", "_")
    return "".join(ch for ch in slug if ch.isalnum() or ch == "_").strip("_")


def _render_article(entry: dict[str, Any], bundle: dict[str, Any], recommendation: dict[str, Any] | None) -> str:
    lines = [
        f"# {entry['question']}",
        "",
        "## Short Answer",
        "",
        entry["answer"],
        "",
        "## Evidence",
        "",
        f"- {bundle['evidence']}",
        "",
        "## Recommended Action",
        "",
        recommendation["recommendation"] if recommendation else bundle["next_action"],
        "",
    ]
    if recommendation:
        lines.extend(
            [
                "## Tradeoff",
                "",
                recommendation["tradeoff"],
                "",
                "## Supporting Context",
                "",
                recommendation["evidence"],
                "",
            ]
        )
    lines.extend(
        [
            "## Related Incident",
            "",
            f"- Incident id: `{bundle['id']}`",
            f"- Target: `{bundle['target']}`",
            "",
        ]
    )
    return "\n".join(lines)


def _render_index(payload: dict[str, Any]) -> str:
    lines = [
        "# Knowledge Base",
        "",
        f"Entry count: `{payload['summary']['count']}`",
        "",
        "| id | question | article |",
        "| --- | --- | --- |",
    ]
    for entry in payload["entries"]:
        lines.append(f"| {entry['id']} | {entry['question']} | {entry['article_path']} |")
    return "\n".join(lines)
