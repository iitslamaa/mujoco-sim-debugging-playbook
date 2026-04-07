# Dashboard Snapshot Milestones Guide

The dashboard snapshot milestones artifact turns the current, next, and terminal states into a short progression.

It highlights:

- the current readiness state
- the next forecasted state
- the terminal target state
- forecast confidence

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_milestones.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/milestones.json`
- `outputs/dashboard_snapshots/milestones.md`
