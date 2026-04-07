from __future__ import annotations
import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_machine_profile(*, environment_report_path: str | Path, output_dir: str | Path) -> dict:
    env = _read_json(environment_report_path)
    payload = {"summary": {"system": env["platform"]["system"], "machine": env["platform"]["machine"], "python": env["platform"]["python_version"]}}
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "machine_profile.json").write_text(json.dumps(payload, indent=2))
    (out / "machine_profile.md").write_text(f"# Machine Profile\n\n- System: `{payload['summary']['system']}`\n- Machine: `{payload['summary']['machine']}`\n- Python: `{payload['summary']['python']}`\n")
    return payload
