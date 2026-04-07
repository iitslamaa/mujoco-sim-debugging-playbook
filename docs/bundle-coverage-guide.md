# Bundle Coverage Guide

`scripts/generate_bundle_coverage.py` combines bundle quality with the repro bundle index to show whether the current debug bundle covers the documented repro cases.

Use it when you want to know whether the captured evidence surface is broad enough to support troubleshooting.

```bash
make bundle-coverage
```

Outputs:

- `outputs/bundle_coverage/bundle_coverage.json`
- `outputs/bundle_coverage/bundle_coverage.md`
