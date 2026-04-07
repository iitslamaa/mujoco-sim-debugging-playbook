# Artifact Handoff

- Status: `fail`
- Top risk artifact: `outputs/support_readiness/support_readiness.json`
- Breach phase: `Clear support report bundle`
- Handoff owner: `artifact-reporting`
- Critical alerts: `2`
- Actions included: `3`

## Headlines

- Artifact status is fail with 5 failures.
- Top risk remains outputs/support_readiness/support_readiness.json at 1.551.
- Trend direction is improving toward pass.

## Alerts

- [critical] Artifact readiness is failing: Current artifact status is fail with 5 failures.
- [critical] Recovery phase in breach: Clear support report bundle is in breach and due on 2026-04-15.
- [warning] Owner overloaded: artifact-reporting is overloaded with 5 commands.

## Actions

- P0 outputs/support_readiness/support_readiness.json -> artifact-integrity: Reduce breach pressure on the support-report bundle.
- P0 outputs/scenario_plan/scenario_plan.json -> artifact-integrity: Reduce breach pressure on the support-report bundle.
- P1 Stabilize top risks -> artifact-integrity: Prevent the current at-risk phase from becoming a breach.

## Owner Context

- Owner: `artifact-reporting`
- Status: `overloaded`
- Command count: `5`
- Phase count: `1`