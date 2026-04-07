# Dashboard Snapshot Alert Packet Guide

The dashboard snapshot alert packet turns the current action register into a compact severity-tagged alert feed.

It captures:

- the current status
- the current owner
- the active critical and warning alerts

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_alert_packet.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/alert_packet.json`
- `outputs/dashboard_snapshots/alert_packet.md`
