# Environment Doctor Guide

Run the environment doctor to capture the current local setup, verify the main support/debugging tools, and emit actionable setup recommendations.

```bash
python scripts/run_environment_doctor.py
```

Outputs:

- `outputs/environment_doctor/doctor.json`
- `outputs/environment_doctor/doctor.md`

This is useful before reproducing a user issue, validating a machine, or checking whether the local environment is ready for container and CI-style workflows.
