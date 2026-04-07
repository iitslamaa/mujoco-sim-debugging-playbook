# Support Triage Reply Guide

`scripts/generate_support_triage_reply.py` turns the response template, session note, and intake checklist into a first-pass triage reply.

Use it when you want a consistent starting point for responding to a GitHub issue or forum thread.

```bash
make support-triage-reply
```

Outputs:

- `outputs/support_triage_reply/support_triage_reply.json`
- `outputs/support_triage_reply/support_triage_reply.md`
