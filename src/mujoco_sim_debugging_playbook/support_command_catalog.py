from __future__ import annotations

import json
from pathlib import Path


def build_support_command_catalog(
    *,
    setup_cheatsheet_path: str | Path,
    output_dir: str | Path,
) -> dict:
    text = Path(setup_cheatsheet_path).read_text()
    commands = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith("```") and not line.endswith(":")
    ]
    entries = [
        {"command": command, "category": "setup" if "bootstrap" in command or "doctor" in command else "validation"}
        for command in commands
    ]
    payload = {
        "summary": {"command_count": len(entries)},
        "entries": entries,
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "support_command_catalog.json").write_text(json.dumps(payload, indent=2))
    (out / "support_command_catalog.md").write_text(
        "# Support Command Catalog\n\n"
        + "\n".join(f"- `{entry['command']}` ({entry['category']})" for entry in entries)
        + "\n"
    )
    return payload
