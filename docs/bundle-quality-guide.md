# Bundle Quality Guide

`scripts/generate_bundle_quality.py` upgrades the debug-bundle check from simple presence validation to an evidence-quality summary.

Use it to see whether a support bundle contains the kinds of files that actually help reproduce and diagnose issues.

```bash
make bundle-quality
```

Outputs:

- `outputs/bundle_quality/bundle_quality.json`
- `outputs/bundle_quality/bundle_quality.md`
