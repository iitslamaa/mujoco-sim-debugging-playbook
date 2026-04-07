# Bundle Verifier Guide

`scripts/generate_bundle_verifier.py` validates the generated debug bundle manifest and emits a simple pass/warn summary.

Use it before sharing a support bundle to confirm the manifest has enough captured evidence.

```bash
make bundle-verifier
```

Outputs:

- `outputs/bundle_verifier/bundle_verifier.json`
- `outputs/bundle_verifier/bundle_verifier.md`
