# Support Command Catalog Guide

`scripts/generate_support_command_catalog.py` extracts the main setup and validation commands from the support documentation into a machine-readable catalog.

Use it when you want a compact command surface for onboarding, support handoff, or terminal-driven debugging.

```bash
make support-command-catalog
```

Outputs:

- `outputs/support_command_catalog/support_command_catalog.json`
- `outputs/support_command_catalog/support_command_catalog.md`
