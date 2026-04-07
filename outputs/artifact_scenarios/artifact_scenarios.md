# Artifact Scenarios

- Baseline status: `fail`
- Baseline failures: `5`
- Baseline warnings: `0`

| scenario | status | failures | warnings | stale_count | refresh_steps |
| --- | --- | ---: | ---: | ---: | ---: |
| Dashboard refresh only | fail | 4 | 0 | 5 | 5 |
| Support report sprint | fail | 1 | 1 | 1 | 1 |
| Top-risk stabilization | fail | 3 | 1 | 4 | 4 |
| Full artifact refresh | pass | 0 | 0 | 0 | 0 |

## Scenario Notes

### Dashboard refresh only

- Refresh the public dashboard artifact while leaving the support-report bundle untouched.
- Top risk artifact after changes: `outputs/support_readiness/support_readiness.json`

### Support report sprint

- Refresh the support-report bundle but leave the dashboard artifact stale.
- Top risk artifact after changes: `dashboard/data.json`

### Top-risk stabilization

- Refresh the highest-risk support outputs first, but leave lower-risk artifacts pending.
- Top risk artifact after changes: `outputs/ops_review/ops_review.json`

### Full artifact refresh

- Refresh every stale artifact so the published surface is fully current.
- Top risk artifact after changes: `outputs/scenario_plan/scenario_plan.json`
