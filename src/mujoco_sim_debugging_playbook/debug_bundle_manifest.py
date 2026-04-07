from __future__ import annotations

import json
from pathlib import Path


def build_debug_bundle_manifest(*, bundle_root: str | Path, output_dir: str | Path) -> dict:
    root = Path(bundle_root)
    latest = sorted(root.glob("*"))[-1]
    files = sorted(p.name for p in latest.iterdir())
    payload = {"summary": {"bundle": latest.name, "file_count": len(files)}, "files": files}
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "debug_bundle_manifest.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "debug_bundle_manifest.md").write_text(
        "# Debug Bundle Manifest\n\n" + f"- Bundle: `{latest.name}`\n- Files: `{len(files)}`\n\n" + "\n".join(f"- {f}" for f in files)
    )
    return payload
