# Environment Alignment Guide

`scripts/generate_environment_alignment.py` combines the environment diff, toolchain inventory, and dependency snapshot into a single alignment summary.

Use it to see whether the local machine, installed tools, and dependency set are aligned enough for reproducible debugging.

```bash
make environment-alignment
```

Outputs:

- `outputs/environment_alignment/environment_alignment.json`
- `outputs/environment_alignment/environment_alignment.md`
