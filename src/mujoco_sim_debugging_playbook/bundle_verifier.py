from __future__ import annotations
import json
from pathlib import Path


def build_bundle_verifier(*, bundle_manifest_path: str | Path, output_dir: str | Path) -> dict:
    manifest = json.loads(Path(bundle_manifest_path).read_text())
    payload = {"summary": {"file_count": manifest["summary"]["file_count"], "status": "pass" if manifest["summary"]["file_count"] >= 5 else "warn"}}
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "bundle_verifier.json").write_text(json.dumps(payload, indent=2))
    (out / "bundle_verifier.md").write_text(f"# Bundle Verifier\n\n- Status: `{payload['summary']['status']}`\n- Files: `{payload['summary']['file_count']}`\n")
    return payload
