from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_impact_analysis(*, dependency_map_path: str | Path) -> dict[str, Any]:
    dependency_map = _read_json(dependency_map_path)
    reverse: dict[str, list[str]] = {}
    for row in dependency_map["rows"]:
        for dep in row["dependencies"]:
            reverse.setdefault(dep, []).append(row["artifact"])

    rows = []
    for dependency, impacted in sorted(reverse.items()):
        unique = sorted(set(impacted))
        rows.append(
            {
                "dependency": dependency,
                "impact_count": len(unique),
                "impacted_artifacts": unique,
            }
        )

    rows.sort(key=lambda row: (-row["impact_count"], row["dependency"]))
    return {
        "summary": {
            "dependency_count": len(rows),
            "most_impactful_dependency": rows[0]["dependency"] if rows else None,
            "max_impact_count": rows[0]["impact_count"] if rows else 0,
        },
        "rows": rows,
    }


def render_impact_analysis_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Impact Analysis",
        "",
        f"- Dependencies tracked: `{payload['summary']['dependency_count']}`",
        f"- Most impactful dependency: `{payload['summary']['most_impactful_dependency']}`",
        f"- Max impact count: `{payload['summary']['max_impact_count']}`",
        "",
        "| dependency | impact_count |",
        "| --- | ---: |",
    ]
    for row in payload["rows"]:
        lines.append(f"| {row['dependency']} | {row['impact_count']} |")
    lines.extend(["", "## Downstream Impact", ""])
    for row in payload["rows"][:10]:
        lines.append(f"### {row['dependency']}")
        lines.append("")
        for artifact in row["impacted_artifacts"]:
            lines.append(f"- {artifact}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_impact_analysis(*, dependency_map_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    payload = build_impact_analysis(dependency_map_path=dependency_map_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "impact_analysis.json").write_text(json.dumps(payload, indent=2))
    (output / "impact_analysis.md").write_text(render_impact_analysis_markdown(payload))
    return payload
