from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_repro_bundle_index(
    *,
    repro_inventory_path: str | Path,
    debug_bundle_manifest_path: str | Path,
    output_dir: str | Path,
) -> dict:
    repro = _read_json(repro_inventory_path)
    bundle = _read_json(debug_bundle_manifest_path)
    entries = []
    for case in repro["cases"]:
        entries.append(
            {
                "case_id": case["case_id"],
                "title": case["title"],
                "bundle": bundle["summary"]["bundle"],
                "bundle_file_count": bundle["summary"]["file_count"],
            }
        )
    payload = {
        "summary": {
            "entry_count": len(entries),
            "bundle": bundle["summary"]["bundle"],
        },
        "entries": entries,
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "repro_bundle_index.json").write_text(json.dumps(payload, indent=2))
    (out / "repro_bundle_index.md").write_text(
        "# Repro Bundle Index\n\n"
        f"- Bundle: `{payload['summary']['bundle']}`\n"
        f"- Entries: `{payload['summary']['entry_count']}`\n"
        + "\n".join(
            f"- `{entry['case_id']}` -> bundle `{entry['bundle']}` ({entry['bundle_file_count']} files)"
            for entry in entries
        )
        + "\n"
    )
    return payload
