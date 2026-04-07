# Support Coverage Gaps

- Open triage items: `11`
- Fully covered items: `6`
- Items needing follow-up: `5`
- Critical items missing coverage: `0`
- Top gap target: `low_damping_high_gain / expert_pd`

| gap_score | severity | target | missing_artifacts | next_best_asset |
| ---: | --- | --- | --- | --- |
| 43.28 | high | low_damping_high_gain / expert_pd | incident_bundle, knowledge_base_entry | Capture a reproducible incident bundle with traces and supporting evidence. |
| 42.98 | high | low_damping_high_gain / hybrid_guardrail | incident_bundle, knowledge_base_entry | Capture a reproducible incident bundle with traces and supporting evidence. |
| 36.18 | critical | episode 1 | -- | No immediate follow-up needed. |
| 36.11 | critical | episode 14 | -- | No immediate follow-up needed. |
| 35.96 | critical | episode 17 | -- | No immediate follow-up needed. |
| 35.86 | critical | episode 9 | -- | No immediate follow-up needed. |
| 35.41 | critical | episode 5 | -- | No immediate follow-up needed. |
| 27.22 | medium | noise_heavy / expert_pd | incident_bundle, knowledge_base_entry | Capture a reproducible incident bundle with traces and supporting evidence. |
| 27.20 | medium | noise_heavy / hybrid_guardrail | incident_bundle, knowledge_base_entry | Capture a reproducible incident bundle with traces and supporting evidence. |
| 27.17 | medium | delay_heavy / expert_pd | incident_bundle, knowledge_base_entry | Capture a reproducible incident bundle with traces and supporting evidence. |
| 4.17 | low | 9947b32 -> HEAD | -- | No gap detected; keep the release review in the audit trail. |

## Coverage Detail

- `low_damping_high_gain / expert_pd`: incident=False, kb=False, recommendation=True, escalation=True
- `low_damping_high_gain / hybrid_guardrail`: incident=False, kb=False, recommendation=True, escalation=True
- `episode 1`: incident=True, kb=True, recommendation=True, escalation=True
- `episode 14`: incident=True, kb=True, recommendation=True, escalation=True
- `episode 17`: incident=True, kb=True, recommendation=True, escalation=True
- `episode 9`: incident=True, kb=True, recommendation=True, escalation=True
- `episode 5`: incident=True, kb=True, recommendation=True, escalation=True
- `noise_heavy / expert_pd`: incident=False, kb=False, recommendation=True, escalation=True
- `noise_heavy / hybrid_guardrail`: incident=False, kb=False, recommendation=True, escalation=True
- `delay_heavy / expert_pd`: incident=False, kb=False, recommendation=True, escalation=True
- `9947b32 -> HEAD`: incident=False, kb=False, recommendation=False, escalation=True