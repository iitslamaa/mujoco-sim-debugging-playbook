# Repro Bundle Index Guide

`scripts/generate_repro_bundle_index.py` links documented repro cases to the current debug-bundle manifest.

Use it to show which support cases are covered by the latest captured evidence bundle.

```bash
make repro-bundle-index
```

Outputs:

- `outputs/repro_bundle_index/repro_bundle_index.json`
- `outputs/repro_bundle_index/repro_bundle_index.md`
