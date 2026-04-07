from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.environment import capture_environment_report


def file_digest(path: str | Path) -> str | None:
    candidate = Path(path)
    if not candidate.exists() or not candidate.is_file():
        return None
    digest = hashlib.sha256()
    with candidate.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_entry(path: str | Path, repo_root: str | Path) -> dict[str, Any]:
    candidate = Path(path)
    root = Path(repo_root).resolve()
    resolved = candidate.resolve()
    try:
        relative = str(resolved.relative_to(root))
    except ValueError:
        relative = str(candidate)
    return {
        "path": relative,
        "exists": resolved.exists(),
        "sha256": file_digest(resolved),
        "size_bytes": resolved.stat().st_size if resolved.exists() and resolved.is_file() else None,
    }


def write_manifest(
    *,
    repo_root: str | Path,
    output_dir: str | Path,
    run_type: str,
    config: dict[str, Any] | None = None,
    inputs: list[str | Path] | None = None,
    outputs: list[str | Path] | None = None,
    metadata: dict[str, Any] | None = None,
) -> Path:
    root = Path(repo_root).resolve()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    payload = {
        "run_type": run_type,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "environment": capture_environment_report(root),
        "config": config or {},
        "inputs": [manifest_entry(item, root) for item in (inputs or [])],
        "outputs": [manifest_entry(item, root) for item in (outputs or [])],
        "metadata": metadata or {},
    }
    destination = output_path / "manifest.json"
    destination.write_text(json.dumps(payload, indent=2))
    return destination


def build_provenance_index(
    *,
    repo_root: str | Path,
    manifest_paths: list[str | Path],
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    manifests = []
    for manifest_path in manifest_paths:
        payload = json.loads(Path(manifest_path).read_text())
        payload["manifest_path"] = str(Path(manifest_path).resolve().relative_to(root))
        manifests.append(payload)

    manifests.sort(key=lambda item: item.get("created_at", ""), reverse=True)
    summary = {
        "manifest_count": len(manifests),
        "run_types": sorted({item["run_type"] for item in manifests}),
        "latest_git_head": manifests[0]["environment"]["tooling"]["git_head"] if manifests else None,
        "latest_created_at": manifests[0]["created_at"] if manifests else None,
    }
    payload = {
        "summary": summary,
        "manifests": manifests,
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "index.json").write_text(json.dumps(payload, indent=2))
    _write_markdown(payload, output_path / "index.md")
    return payload


def _write_markdown(payload: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Provenance Index",
        "",
        f"Manifest count: `{payload['summary']['manifest_count']}`",
        "",
        f"Latest Git HEAD: `{payload['summary']['latest_git_head']}`",
        "",
        "| run_type | created_at | manifest | dirty | outputs |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for manifest in payload["manifests"]:
        lines.append(
            f"| {manifest['run_type']} | {manifest['created_at']} | {manifest['manifest_path']} | "
            f"{'yes' if manifest['environment']['tooling'].get('git_is_dirty') else 'no'} | {len(manifest.get('outputs', []))} |"
        )
    Path(path).write_text("\n".join(lines))
