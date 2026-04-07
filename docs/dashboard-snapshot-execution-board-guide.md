# Dashboard Snapshot Execution Board Guide

The dashboard snapshot execution board turns the current resolution plan into a lightweight lane view.

It highlights:

- active versus planned work lanes
- which phase is currently in focus
- how many items sit in each lane

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_execution_board.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/execution_board.json`
- `outputs/dashboard_snapshots/execution_board.md`
