from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


def _run(command: list[str], cwd: str | Path) -> str:
    completed = subprocess.run(command, cwd=Path(cwd), check=True, capture_output=True, text=True)
    return completed.stdout.strip()


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_release_notes(
    *,
    repo_root: str | Path,
    base_ref: str,
    head_ref: str,
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    commit_subjects = _run(
        ["git", "log", "--format=%H%x09%s", f"{base_ref}..{head_ref}"],
        cwd=root,
    ).splitlines()
    commits = []
    for line in commit_subjects:
        if not line:
            continue
        sha, subject = line.split("\t", 1)
        commits.append({"sha": sha, "subject": subject})

    changed_files = [
        line for line in _run(["git", "diff", "--name-only", base_ref, head_ref], cwd=root).splitlines() if line
    ]
    shortstat = _run(["git", "diff", "--shortstat", base_ref, head_ref], cwd=root)

    provenance = _read_json(root / "outputs" / "provenance" / "index.json")
    regression_gate = _read_json(root / "outputs" / "regression" / "gate" / "regression_gate.json")
    regression_history = _read_json(root / "outputs" / "regression" / "history" / "history.json")

    changed_areas = _categorize_files(changed_files)
    payload = {
        "base_ref": base_ref,
        "head_ref": head_ref,
        "commit_count": len(commits),
        "commits": commits,
        "changed_files": changed_files,
        "changed_areas": changed_areas,
        "diffstat": shortstat,
        "regression_gate": {
            "status": regression_gate["status"],
            "violation_count": regression_gate["violation_count"],
        },
        "regression_trends": regression_history["trend_summary"],
        "provenance_summary": provenance["summary"],
    }

    (output_path / "release_notes.json").write_text(json.dumps(payload, indent=2))
    _write_markdown(payload, output_path / "release_notes.md")
    return payload


def _categorize_files(paths: list[str]) -> dict[str, int]:
    buckets = {
        "docs": 0,
        "dashboard": 0,
        "scripts": 0,
        "core_python": 0,
        "tests": 0,
        "outputs": 0,
        "ci": 0,
        "other": 0,
    }
    for path in paths:
        if path.startswith("docs/") or path == "README.md":
            buckets["docs"] += 1
        elif path.startswith("dashboard/"):
            buckets["dashboard"] += 1
        elif path.startswith("scripts/"):
            buckets["scripts"] += 1
        elif path.startswith("src/"):
            buckets["core_python"] += 1
        elif path.startswith("tests/"):
            buckets["tests"] += 1
        elif path.startswith("outputs/"):
            buckets["outputs"] += 1
        elif path.startswith(".github/") or path == "Makefile":
            buckets["ci"] += 1
        else:
            buckets["other"] += 1
    return {key: value for key, value in buckets.items() if value}


def _write_markdown(payload: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Release Notes",
        "",
        f"Comparison: `{payload['base_ref']}` -> `{payload['head_ref']}`",
        "",
        f"Commits included: `{payload['commit_count']}`",
        "",
        f"Diffstat: {payload['diffstat'] or 'n/a'}",
        "",
        "## Regression status",
        "",
        f"- Gate status: `{payload['regression_gate']['status']}`",
        f"- Gate violations: `{payload['regression_gate']['violation_count']}`",
        "",
        "## Provenance coverage",
        "",
        f"- Manifest count: `{payload['provenance_summary']['manifest_count']}`",
        f"- Run types: `{', '.join(payload['provenance_summary']['run_types'])}`",
        "",
        "## Changed areas",
        "",
    ]
    for area, count in payload["changed_areas"].items():
        lines.append(f"- `{area}`: {count} files")

    lines.extend(["", "## Commits", ""])
    for commit in payload["commits"]:
        lines.append(f"- `{commit['sha'][:7]}` {commit['subject']}")

    lines.extend(["", "## Trend summary", ""])
    for metric, summary in payload["regression_trends"].items():
        latest = summary["latest"]
        latest_text = "n/a" if latest is None else f"{latest:.4f}"
        lines.append(
            f"- `{metric}`: {summary['direction']} ({summary['delta']:.4f}), latest `{latest_text}`"
        )

    lines.extend(["", "## Changed files", ""])
    for changed_file in payload["changed_files"][:60]:
        lines.append(f"- `{changed_file}`")
    if len(payload["changed_files"]) > 60:
        lines.append(f"- ... and {len(payload['changed_files']) - 60} more")

    Path(path).write_text("\n".join(lines))
