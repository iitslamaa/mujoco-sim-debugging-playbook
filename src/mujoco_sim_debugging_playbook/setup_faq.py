from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_setup_faq(*, doctor_path: str | Path, compatibility_path: str | Path, output_dir: str | Path) -> dict:
    doctor = _read_json(doctor_path)
    compatibility = _read_json(compatibility_path)
    entries = [
        {
            "question": "How do I know whether my environment is ready?",
            "answer": f"Current doctor status is {doctor['summary']['status']} with {doctor['summary']['warning_count']} warnings.",
        },
        {
            "question": "What should I install first if setup is incomplete?",
            "answer": doctor["recommendations"][0],
        },
        {
            "question": "What compatibility risk is currently visible?",
            "answer": compatibility["checks"][-1]["detail"],
        },
    ]
    payload = {"summary": {"entry_count": len(entries)}, "entries": entries}
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "setup_faq.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "setup_faq.md").write_text("# Setup FAQ\n\n" + "\n".join(f"- Q: {e['question']}\n  A: {e['answer']}" for e in entries))
    return payload
