# Dependency Map

- Artifacts mapped: `6`
- Max dependency count: `6`

| artifact | dependency_count | existing_dependency_count |
| --- | ---: | ---: |
| dashboard/data.json | 6 | 6 |
| outputs/support_readiness/support_readiness.json | 6 | 6 |
| outputs/scenario_plan/scenario_plan.json | 2 | 2 |
| outputs/ops_review/ops_review.json | 4 | 4 |
| outputs/scorecard/scorecard.json | 4 | 4 |
| outputs/briefing_note/briefing_note.json | 4 | 4 |

## Dependencies

### dashboard/data.json

- scripts/generate_dashboard.py
- outputs/support_readiness/support_readiness.json
- outputs/scenario_plan/scenario_plan.json
- outputs/ops_review/ops_review.json
- outputs/scorecard/scorecard.json
- outputs/briefing_note/briefing_note.json

### outputs/support_readiness/support_readiness.json

- scripts/generate_support_readiness.py
- outputs/support_ops/support_ops.json
- outputs/support_gaps/support_gaps.json
- outputs/sla/sla_report.json
- outputs/capacity/capacity_plan.json
- outputs/releases/latest/release_notes.json

### outputs/scenario_plan/scenario_plan.json

- scripts/generate_scenario_plan.py
- outputs/support_readiness/support_readiness.json

### outputs/ops_review/ops_review.json

- scripts/generate_ops_review.py
- outputs/support_ops/support_ops.json
- outputs/capacity/capacity_plan.json
- outputs/anomalies/anomaly_report.json

### outputs/scorecard/scorecard.json

- scripts/generate_scorecard.py
- outputs/support_ops/support_ops.json
- outputs/support_readiness/support_readiness.json
- outputs/scenario_plan/scenario_plan.json

### outputs/briefing_note/briefing_note.json

- scripts/generate_briefing_note.py
- outputs/scorecard/scorecard.json
- outputs/ops_review/ops_review.json
- outputs/scenario_plan/scenario_plan.json
