from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_release_dry_run(
    *,
    release_blockers_path: str | Path,
    machine_readiness_path: str | Path,
    environment_alignment_path: str | Path,
    output_dir: str | Path,
) -> dict:
    blockers = _read_json(release_blockers_path)
    machine = _read_json(machine_readiness_path)
    alignment = _read_json(environment_alignment_path)
    statuses = [
        blockers["summary"]["status"],
        machine["summary"]["status"],
        alignment["summary"]["status"],
    ]
    final_status = "pass" if all(status == "pass" for status in statuses) else "warn"
    payload = {
        "summary": {
            "status": final_status,
            "blocker_count": blockers["summary"]["blocker_count"],
            "machine_warning_count": machine["summary"]["warning_count"],
            "missing_tool_count": alignment["summary"]["missing_tool_count"],
        },
        "recommendation": (
            "Proceed with release validation."
            if final_status == "pass"
            else "Clear environment and release blockers before shipping."
        ),
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "release_dry_run.json").write_text(json.dumps(payload, indent=2))
    (out / "release_dry_run.md").write_text(
        "# Release Dry Run\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Blockers: `{payload['summary']['blocker_count']}`\n"
        f"- Machine warnings: `{payload['summary']['machine_warning_count']}`\n"
        f"- Missing tools: `{payload['summary']['missing_tool_count']}`\n"
        f"- Recommendation: {payload['recommendation']}\n"
    )
    return payload
