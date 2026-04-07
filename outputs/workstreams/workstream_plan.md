# Support Workstream Plan

- Active lanes: `1`
- Planned items: `5`
- Blocking items: `2`
- Estimated points: `22`
- Top lane: `incident_backfill`

## incident_backfill

- Items: `5`
- Blocking: `2`
- Estimated points: `22`

| severity | target | effort | deliverable | recommended_action |
| --- | --- | --- | --- | --- |
| high | low_damping_high_gain / expert_pd | large (5 pts) | Create a reproducible incident bundle and attach trace evidence. | Increase joint damping and reduce actuator gain before changing controller structure. |
| high | low_damping_high_gain / hybrid_guardrail | large (5 pts) | Create a reproducible incident bundle and attach trace evidence. | Increase joint damping and reduce actuator gain before changing controller structure. |
| medium | noise_heavy / expert_pd | medium (4 pts) | Create a reproducible incident bundle and attach trace evidence. | Add observation filtering or slightly lower controller aggressiveness under noisy sensing. |
| medium | noise_heavy / hybrid_guardrail | medium (4 pts) | Create a reproducible incident bundle and attach trace evidence. | Add observation filtering or slightly lower controller aggressiveness under noisy sensing. |
| medium | delay_heavy / expert_pd | medium (4 pts) | Create a reproducible incident bundle and attach trace evidence. | Increase control frequency or use a more delay-tolerant guarded policy blend. |

### Rationale

- `low_damping_high_gain / expert_pd`: Elevated benchmark risk in `low_damping_high_gain` for `expert_pd`.
- `low_damping_high_gain / hybrid_guardrail`: Elevated benchmark risk in `low_damping_high_gain` for `hybrid_guardrail`.
- `noise_heavy / expert_pd`: Elevated benchmark risk in `noise_heavy` for `expert_pd`.
- `noise_heavy / hybrid_guardrail`: Elevated benchmark risk in `noise_heavy` for `hybrid_guardrail`.
- `delay_heavy / expert_pd`: Elevated benchmark risk in `delay_heavy` for `expert_pd`.
