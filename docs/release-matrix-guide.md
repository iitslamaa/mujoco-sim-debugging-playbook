# Release Matrix Guide

`scripts/generate_release_matrix.py` combines release-checklist status and compatibility status into a compact release-readiness matrix.

Use it to summarize whether a release candidate looks healthy across core validation dimensions.

```bash
make release-matrix
```

Outputs:

- `outputs/release_matrix/release_matrix.json`
- `outputs/release_matrix/release_matrix.md`
