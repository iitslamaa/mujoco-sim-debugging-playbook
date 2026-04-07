from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_artifact_freshness(
    *,
    root: str | Path,
    artifact_paths: list[str | Path],
    reference_paths: list[str | Path],
) -> dict[str, Any]:
    root = Path(root)
    references = [root / Path(path) for path in reference_paths]
    existing_references = [path for path in references if path.exists()]
    latest_reference_mtime = max((path.stat().st_mtime for path in existing_references), default=0.0)

    rows = []
    for artifact in artifact_paths:
        path = root / Path(artifact)
        exists = path.exists()
        mtime = path.stat().st_mtime if exists else 0.0
        status = "missing"
        if exists:
            status = "fresh" if mtime >= latest_reference_mtime else "stale"
        rows.append(
            {
                "artifact": str(Path(artifact)),
                "exists": exists,
                "status": status,
                "age_delta_seconds": round(latest_reference_mtime - mtime, 3) if exists else None,
            }
        )

    return {
        "summary": {
            "artifact_count": len(rows),
            "fresh_count": sum(1 for row in rows if row["status"] == "fresh"),
            "stale_count": sum(1 for row in rows if row["status"] == "stale"),
            "missing_count": sum(1 for row in rows if row["status"] == "missing"),
        },
        "rows": rows,
    }


def render_artifact_freshness_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Freshness",
        "",
        f"- Artifacts checked: `{payload['summary']['artifact_count']}`",
        f"- Fresh: `{payload['summary']['fresh_count']}`",
        f"- Stale: `{payload['summary']['stale_count']}`",
        f"- Missing: `{payload['summary']['missing_count']}`",
        "",
        "| artifact | status | age_delta_seconds |",
        "| --- | --- | ---: |",
    ]
    for row in payload["rows"]:
        delta = "--" if row["age_delta_seconds"] is None else f"{row['age_delta_seconds']:.3f}"
        lines.append(f"| {row['artifact']} | {row['status']} | {delta} |")
    return "\n".join(lines)


def write_artifact_freshness(
    *,
    root: str | Path,
    output_dir: str | Path,
    artifact_paths: list[str | Path],
    reference_paths: list[str | Path],
) -> dict[str, Any]:
    payload = build_artifact_freshness(
        root=root,
        artifact_paths=artifact_paths,
        reference_paths=reference_paths,
    )
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "artifact_freshness.json").write_text(json.dumps(payload, indent=2))
    (output_path / "artifact_freshness.md").write_text(render_artifact_freshness_markdown(payload))
    return payload
