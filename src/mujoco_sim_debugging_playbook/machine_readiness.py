from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_machine_readiness(
    *,
    machine_profile_path: str | Path,
    doctor_path: str | Path,
    compatibility_path: str | Path,
    output_dir: str | Path,
) -> dict:
    machine = _read_json(machine_profile_path)
    doctor = _read_json(doctor_path)
    compatibility = _read_json(compatibility_path)

    failing_checks = [
        check["name"]
        for check in doctor["checks"] + compatibility["checks"]
        if check["status"] == "warn"
    ]
    status = "pass" if not failing_checks else "warn"
    payload = {
        "summary": {
            "status": status,
            "system": machine["summary"]["system"],
            "machine": machine["summary"]["machine"],
            "warning_count": len(failing_checks),
        },
        "warnings": failing_checks,
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "machine_readiness.json").write_text(json.dumps(payload, indent=2))
    (out / "machine_readiness.md").write_text(
        "# Machine Readiness\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- System: `{payload['summary']['system']}`\n"
        f"- Machine: `{payload['summary']['machine']}`\n"
        f"- Warnings: `{payload['summary']['warning_count']}`\n"
    )
    return payload
