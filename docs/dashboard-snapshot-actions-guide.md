# Dashboard Snapshot Actions Guide

The dashboard snapshot actions report turns the current digest and closeout state into a short prioritized action register.

It captures:

- the current state
- who owns the next work
- the ordered remaining actions

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_actions.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/actions.json`
- `outputs/dashboard_snapshots/actions.md`
