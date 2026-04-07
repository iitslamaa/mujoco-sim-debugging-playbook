# Support Playbook

This repository is designed to look and feel like a miniature robotics support environment rather than a one-off experiment.

## What this playbook demonstrates

- reproducing user-reported simulation issues with exact commands
- narrowing failures to one parameter or subsystem at a time
- writing user-facing responses that are specific, actionable, and calm
- turning repeated support questions into better docs, issue templates, and examples

## Triage workflow

1. Confirm the user goal and exact failure mode.
2. Collect the command, config, environment, and artifact paths.
3. Reproduce with a fixed seed and known config.
4. Compare scalar metrics and time-series traces.
5. Respond with:
   - what was reproduced
   - what most likely caused it
   - exact next steps
   - relevant docs and outputs

## Included support cases

- `actuator_gain_overshoot`
- `delay_instability`
- `noisy_observation_regression`

Run one with:

```bash
python scripts/run_issue_case.py --case actuator_gain_overshoot
```

The output is a Markdown response draft and repro checklist under `outputs/support_cases/`.

## Why this workflow is useful

- users report a confusing training or sim behavior
- the engineer reproduces it under a controlled setup
- metrics and traces are used to explain the failure
- docs and examples are updated to lower future support load
