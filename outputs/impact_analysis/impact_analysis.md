# Impact Analysis

- Dependencies tracked: `17`
- Most impactful dependency: `outputs/scenario_plan/scenario_plan.json`
- Max impact count: `3`

| dependency | impact_count |
| --- | ---: |
| outputs/scenario_plan/scenario_plan.json | 3 |
| outputs/support_ops/support_ops.json | 3 |
| outputs/support_readiness/support_readiness.json | 3 |
| outputs/capacity/capacity_plan.json | 2 |
| outputs/ops_review/ops_review.json | 2 |
| outputs/scorecard/scorecard.json | 2 |
| outputs/anomalies/anomaly_report.json | 1 |
| outputs/briefing_note/briefing_note.json | 1 |
| outputs/releases/latest/release_notes.json | 1 |
| outputs/sla/sla_report.json | 1 |
| outputs/support_gaps/support_gaps.json | 1 |
| scripts/generate_briefing_note.py | 1 |
| scripts/generate_dashboard.py | 1 |
| scripts/generate_ops_review.py | 1 |
| scripts/generate_scenario_plan.py | 1 |
| scripts/generate_scorecard.py | 1 |
| scripts/generate_support_readiness.py | 1 |

## Downstream Impact

### outputs/scenario_plan/scenario_plan.json

- dashboard/data.json
- outputs/briefing_note/briefing_note.json
- outputs/scorecard/scorecard.json

### outputs/support_ops/support_ops.json

- outputs/ops_review/ops_review.json
- outputs/scorecard/scorecard.json
- outputs/support_readiness/support_readiness.json

### outputs/support_readiness/support_readiness.json

- dashboard/data.json
- outputs/scenario_plan/scenario_plan.json
- outputs/scorecard/scorecard.json

### outputs/capacity/capacity_plan.json

- outputs/ops_review/ops_review.json
- outputs/support_readiness/support_readiness.json

### outputs/ops_review/ops_review.json

- dashboard/data.json
- outputs/briefing_note/briefing_note.json

### outputs/scorecard/scorecard.json

- dashboard/data.json
- outputs/briefing_note/briefing_note.json

### outputs/anomalies/anomaly_report.json

- outputs/ops_review/ops_review.json

### outputs/briefing_note/briefing_note.json

- dashboard/data.json

### outputs/releases/latest/release_notes.json

- outputs/support_readiness/support_readiness.json

### outputs/sla/sla_report.json

- outputs/support_readiness/support_readiness.json
