# Repro Readiness Guide

`scripts/generate_repro_readiness.py` turns the repro bundle index and support intake checklist into a simple readiness verdict.

Use it to decide whether a case is ready for real debugging work or still missing support context.

```bash
make repro-readiness
```

Outputs:

- `outputs/repro_readiness/repro_readiness.json`
- `outputs/repro_readiness/repro_readiness.md`
