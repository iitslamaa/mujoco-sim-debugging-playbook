# Release Dry Run Guide

`scripts/generate_release_dry_run.py` condenses release blockers, machine readiness, and environment alignment into one release-candidate verdict.

Use it to answer the practical question of whether the current environment and validation state are good enough to proceed with a release candidate.

```bash
make release-dry-run
```

Outputs:

- `outputs/release_dry_run/release_dry_run.json`
- `outputs/release_dry_run/release_dry_run.md`
