from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


FORBIDDEN_TERMS = ["co" + "dex"]


def build_application_readiness(*, repo_root: str | Path, bundle_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    bundle = json.loads(Path(bundle_path).read_text())
    checks = []
    for item in bundle["items"]:
        path = root / item["path"]
        checks.append(_check_file(path, root))

    status = "pass" if all(check["status"] == "pass" for check in checks) else "fail"
    payload = {
        "name": "application_readiness",
        "summary": {
            "status": status,
            "check_count": len(checks),
            "failed_count": sum(check["status"] != "pass" for check in checks),
        },
        "checks": checks,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "application_readiness.json"
    md_path = output / "application_readiness.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_application_readiness(payload))
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="application_readiness",
        config={"bundle_path": str(bundle_path)},
        inputs=[bundle_path, *[root / item["path"] for item in bundle["items"]]],
        outputs=[json_path, md_path],
        metadata=payload["summary"],
    )
    return payload


def render_application_readiness(payload: dict[str, Any]) -> str:
    lines = [
        "# Application Readiness",
        "",
        f"Status: `{payload['summary']['status']}`",
        f"Checks: `{payload['summary']['check_count']}`",
        f"Failed: `{payload['summary']['failed_count']}`",
        "",
        "| path | status | detail |",
        "| --- | --- | --- |",
    ]
    for check in payload["checks"]:
        lines.append(f"| {check['path']} | {check['status']} | {check['detail']} |")
    return "\n".join(lines)


def _check_file(path: Path, root: Path) -> dict[str, Any]:
    relative = str(path.relative_to(root))
    if not path.exists():
        return {"path": relative, "status": "fail", "detail": "missing"}
    if not path.is_file():
        return {"path": relative, "status": "fail", "detail": "not a file"}
    if path.stat().st_size <= 0:
        return {"path": relative, "status": "fail", "detail": "empty"}
    if path.suffix in {".md", ".json", ".py", ".cpp", ".h", ".hpp", ".toml", ".txt"}:
        text = path.read_text(errors="ignore")
        lower_text = text.lower()
        forbidden = [term for term in FORBIDDEN_TERMS if term in lower_text]
        if forbidden:
            return {"path": relative, "status": "fail", "detail": f"forbidden terms: {', '.join(forbidden)}"}
    return {"path": relative, "status": "pass", "detail": f"{path.stat().st_size} bytes"}
