# Release Blockers Guide

`scripts/generate_release_blockers.py` turns the release checklist and release matrix into a concrete blocker list.

Use it to answer the practical question: what still needs to be cleared before treating a release candidate as healthy?

```bash
make release-blockers
```

Outputs:

- `outputs/release_blockers/release_blockers.json`
- `outputs/release_blockers/release_blockers.md`
