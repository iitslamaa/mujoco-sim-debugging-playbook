# Machine Readiness Guide

`scripts/generate_machine_readiness.py` combines machine profile, environment doctor, and compatibility checks into a single host-level readiness verdict.

Use it when you want a concise answer to whether a machine looks ready to reproduce or support a MuJoCo workflow.

```bash
make machine-readiness
```

Outputs:

- `outputs/machine_readiness/machine_readiness.json`
- `outputs/machine_readiness/machine_readiness.md`
