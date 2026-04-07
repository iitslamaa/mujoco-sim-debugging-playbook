# Machine Profile Guide

`scripts/generate_machine_profile.py` turns the diagnostics environment snapshot into a compact machine profile.

Use it when you want a reproducible summary of the local host that produced experiment or support artifacts.

```bash
make machine-profile
```

Outputs:

- `outputs/machine_profile/machine_profile.json`
- `outputs/machine_profile/machine_profile.md`
