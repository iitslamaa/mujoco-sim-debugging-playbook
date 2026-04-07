# Support Escalation Brief Guide

`scripts/generate_support_escalation_brief.py` packages the triage reply, session note, and release blockers into a concise escalation brief.

Use it when a support issue needs to move from first response into deeper engineering review.

```bash
make support-escalation-brief
```

Outputs:

- `outputs/support_escalation_brief/support_escalation_brief.json`
- `outputs/support_escalation_brief/support_escalation_brief.md`
