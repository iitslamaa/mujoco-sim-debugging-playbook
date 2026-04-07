# Artifact Executive Summary

- Status: `fail`
- Failures: `5`
- Top risk artifact: `outputs/support_readiness/support_readiness.json`
- Top risk score: `1.551`
- Breach phase: `Clear support report bundle`
- Overloaded owner: `artifact-reporting`

## Wins

- The artifact-readiness gate is surfacing crisp failures rather than ambiguous warnings.
- The capacity model narrowed the highest-pressure phase to `Clear support report bundle`.
- The recovery plan can still reach `fail` -> `pass` with the current three-phase structure.

## Risks

- Top artifact risk remains `outputs/support_readiness/support_readiness.json` at score `1.551`.
- Delivery forecast shows `Clear support report bundle` in breach with due date `2026-04-15`.
- Owner `artifact-reporting` is overloaded with `5` commands across active phases.

## Next Actions

| artifact | phase | owner | action |
| --- | --- | --- | --- |
| outputs/support_readiness/support_readiness.json | Clear support report bundle | artifact-integrity | High-risk artifact should move to a more specialized owner. |
| outputs/scenario_plan/scenario_plan.json | Clear support report bundle | artifact-integrity | High-risk artifact should move to a more specialized owner. |