# Artifact Capacity Plan

- Owners tracked: `3`
- Overloaded owners: `1`
- Phases tracked: `3`
- Rebalance items: `2`
- Highest-pressure phase: `Clear support report bundle`

## Owner Load

| owner | status | phases | commands | breaches | at_risk |
| --- | --- | ---: | ---: | ---: | ---: |
| artifact-reporting | overloaded | 1 | 5 | 1 | 0 |
| artifact-integrity | healthy | 1 | 2 | 0 | 1 |
| dashboard-maintenance | healthy | 1 | 1 | 0 | 1 |

## Phase Actions

| phase | owner | status | commands | shift | action |
| --- | --- | --- | ---: | ---: | --- |
| Clear support report bundle | artifact-reporting | breach | 5 | 4 | Split this phase across reporting and integrity owners. |
| Stabilize top risks | artifact-integrity | at_risk | 2 | 0 | Keep current staffing and monitor progress. |
| Clear dashboard lag | dashboard-maintenance | at_risk | 1 | 0 | Keep current staffing and monitor progress. |

## Rebalance Items

| status | phase | artifact | current_owner | recommended_owner | risk_score | reason |
| --- | --- | --- | --- | --- | ---: | --- |
| breach | Clear support report bundle | outputs/support_readiness/support_readiness.json | artifact-reporting | artifact-integrity | 1.551 | High-risk artifact should move to a more specialized owner. |
| breach | Clear support report bundle | outputs/scenario_plan/scenario_plan.json | artifact-reporting | artifact-integrity | 1.550 | High-risk artifact should move to a more specialized owner. |