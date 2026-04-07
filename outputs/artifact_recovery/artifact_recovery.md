# Artifact Recovery Roadmap

- Current status: `fail`
- Current failures: `5`
- Phases: `3`
- Top risk artifact: `outputs/support_readiness/support_readiness.json`
- Target status: `pass`

| phase | expected_status | expected_failures | goal |
| --- | --- | ---: | --- |
| 1: Stabilize top risks | fail | 3 | Reduce the highest-impact stale artifacts first to shrink maintenance risk quickly. |
| 2: Clear support report bundle | fail | 1 | Refresh the support-report bundle so the public support surface is nearly current. |
| 3: Clear dashboard lag | pass | 0 | Refresh the public dashboard so the surfaced state matches the refreshed support reports. |

## Phase Plan

### Phase 1: Stabilize top risks

- Goal: Reduce the highest-impact stale artifacts first to shrink maintenance risk quickly.
- Expected status after phase: `fail`
- Expected failures after phase: `3`
- Focus artifacts:
- `outputs/support_readiness/support_readiness.json`
- `outputs/scenario_plan/scenario_plan.json`
- Commands:
- `python scripts/generate_support_readiness.py`
- `python scripts/generate_scenario_plan.py`

### Phase 2: Clear support report bundle

- Goal: Refresh the support-report bundle so the public support surface is nearly current.
- Expected status after phase: `fail`
- Expected failures after phase: `1`
- Focus artifacts:
- `outputs/scenario_plan/scenario_plan.json`
- `outputs/support_readiness/support_readiness.json`
- `outputs/ops_review/ops_review.json`
- `outputs/scorecard/scorecard.json`
- `outputs/briefing_note/briefing_note.json`
- Commands:
- `python scripts/generate_scenario_plan.py`
- `python scripts/generate_support_readiness.py`
- `python scripts/generate_ops_review.py`
- `python scripts/generate_scorecard.py`
- `python scripts/generate_briefing_note.py`

### Phase 3: Clear dashboard lag

- Goal: Refresh the public dashboard so the surfaced state matches the refreshed support reports.
- Expected status after phase: `pass`
- Expected failures after phase: `0`
- Focus artifacts:
- `dashboard/data.json`
- Commands:
- `python scripts/generate_dashboard.py`
