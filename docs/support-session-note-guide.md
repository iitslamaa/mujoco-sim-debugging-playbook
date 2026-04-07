# Support Session Note Guide

`scripts/generate_support_session_note.py` merges the intake checklist, repro inventory, and response rubric into a single support-session brief.

Use it to structure a debugging handoff before writing a GitHub issue response or partner follow-up.

```bash
make support-session-note
```

Outputs:

- `outputs/support_session_note/support_session_note.json`
- `outputs/support_session_note/support_session_note.md`
