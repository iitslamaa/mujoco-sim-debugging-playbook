# Dashboard Snapshot Scorecard Guide

The dashboard snapshot scorecard condenses the current snapshot stack into a compact KPI summary.

It captures:

- current and projected status
- closeout state
- handoff ownership
- alert and blocker counts
- dominant transition

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_scorecard.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/scorecard.json`
- `outputs/dashboard_snapshots/scorecard.md`
