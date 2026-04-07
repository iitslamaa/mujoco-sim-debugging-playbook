# Artifact Action Register

- Actions: `4`
- Current status: `fail`
- Projected terminal status: `pass`
- Top risk artifact: `outputs/support_readiness/support_readiness.json`

| priority | target | owner | phase | expected_impact |
| --- | --- | --- | --- | --- |
| P0 | outputs/support_readiness/support_readiness.json | artifact-integrity | Clear support report bundle | Reduce breach pressure on the support-report bundle. |
| P0 | outputs/scenario_plan/scenario_plan.json | artifact-integrity | Clear support report bundle | Reduce breach pressure on the support-report bundle. |
| P1 | Stabilize top risks | artifact-integrity | Stabilize top risks | Prevent the current at-risk phase from becoming a breach. |
| P2 | full_refresh_projection | artifact-program | Full artifact refresh | Move the artifact surface from fail to pass. |

## Action Notes

- `P0` `outputs/support_readiness/support_readiness.json`: High-risk artifact should move to a more specialized owner.
- `P0` `outputs/scenario_plan/scenario_plan.json`: High-risk artifact should move to a more specialized owner.
- `P1` `Stabilize top risks`: This is the nearest-due recovery phase in the current delivery forecast.
- `P2` `full_refresh_projection`: History shows a full refresh is the path to a pass state.