# Dependency Snapshot Guide

Use the dependency snapshot to capture the current `pip freeze` surface from the environment report.

```bash
python scripts/generate_dependency_snapshot.py
```

Outputs:

- `outputs/dependency_snapshot/dependency_snapshot.json`
- `outputs/dependency_snapshot/dependency_snapshot.md`
