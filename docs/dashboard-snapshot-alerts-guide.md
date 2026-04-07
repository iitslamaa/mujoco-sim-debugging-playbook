# Dashboard Snapshot Alerts Guide

The dashboard snapshot alerts report turns major timeline changes into a small operator-style alert feed.

It highlights:

- the first preserved snapshot that reaches `pass`
- large failure-count drops
- large maintenance-risk drops
- status transitions into `pass`

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_alerts.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/alerts.json`
- `outputs/dashboard_snapshots/alerts.md`
