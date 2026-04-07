from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_support_response_template(
    *,
    support_session_note_path: str | Path,
    response_rubric_path: str | Path,
    output_dir: str | Path,
) -> dict:
    session = _read_json(support_session_note_path)
    rubric = _read_json(response_rubric_path)
    required = [item["criterion"] for item in rubric["criteria"] if item["status"] == "required"]
    payload = {
        "summary": {
            "status": session["summary"]["status"],
            "required_section_count": len(required),
        },
        "sections": [
            {"title": "Reproduction", "prompt": "List the exact command or config used to reproduce the issue."},
            {"title": "Observed behavior", "prompt": "Describe what happened and what was expected instead."},
            {"title": "Evidence", "prompt": "Attach the most relevant plots, logs, or bundle files."},
            {"title": "Next action", "prompt": session["next_step"]},
        ],
        "required_criteria": required,
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "support_response_template.json").write_text(json.dumps(payload, indent=2))
    (out / "support_response_template.md").write_text(
        "# Support Response Template\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Required sections: `{payload['summary']['required_section_count']}`\n"
        + "\n".join(f"- {section['title']}: {section['prompt']}" for section in payload["sections"])
        + "\n"
    )
    return payload
