# Dashboard Snapshot Closeout Guide

The dashboard snapshot closeout report makes an explicit closeout decision for the current snapshot state.

It captures:

- whether the current state is ready to close
- who still owns the remaining work
- how many items remain
- what blockers still prevent closeout

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_closeout.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/closeout.json`
- `outputs/dashboard_snapshots/closeout.md`
