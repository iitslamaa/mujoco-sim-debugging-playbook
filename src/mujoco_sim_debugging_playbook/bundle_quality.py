from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_bundle_quality(
    *,
    bundle_manifest_path: str | Path,
    bundle_verifier_path: str | Path,
    output_dir: str | Path,
) -> dict:
    manifest = _read_json(bundle_manifest_path)
    verifier = _read_json(bundle_verifier_path)
    files = manifest["files"]
    evidence_hits = sum(
        1 for name in files if any(token in name for token in ("environment", "diagnostics", "summary"))
    )
    status = "pass" if verifier["summary"]["status"] == "pass" and evidence_hits >= 3 else "warn"
    payload = {
        "summary": {
            "status": status,
            "file_count": manifest["summary"]["file_count"],
            "evidence_hit_count": evidence_hits,
        },
        "high_value_files": [
            name for name in files if any(token in name for token in ("environment", "diagnostics", "summary"))
        ],
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "bundle_quality.json").write_text(json.dumps(payload, indent=2))
    (out / "bundle_quality.md").write_text(
        "# Bundle Quality\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Files: `{payload['summary']['file_count']}`\n"
        f"- High-value files: `{payload['summary']['evidence_hit_count']}`\n"
    )
    return payload
