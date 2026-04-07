# Dashboard Snapshot Review Guide

The dashboard snapshot review rolls the monitor summary into a concise reviewer-facing note.

It highlights:

- the current and projected status
- the current top alert
- the immediate next focus
- any remaining blockers before the dashboard state feels settled

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_review.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/review.json`
- `outputs/dashboard_snapshots/review.md`
