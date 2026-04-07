# Dashboard Snapshot Monitor Guide

The dashboard snapshot monitor combines the preserved snapshot history, drift analysis, and alert feed into a single high-level monitoring summary.

It is useful when you want one artifact that answers:

- what the current status is
- where the biggest recovery happened
- when the first preserved `pass` state appears
- which alert matters most right now

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_monitor.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/monitor.json`
- `outputs/dashboard_snapshots/monitor.md`
