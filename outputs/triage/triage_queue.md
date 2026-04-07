# Support Triage Queue

Open triage items: `11`

Top priority: `episode 1`

| priority_score | kind | target | summary | next_action |
| ---: | --- | --- | --- | --- |
| 217.09 | randomized_episode | episode 1 | Hard randomized episode with worst controller `expert_pd`. | Reduce control delay or switch to the guarded/learned policy family; lower actuator gain. |
| 216.67 | randomized_episode | episode 14 | Hard randomized episode with worst controller `expert_pd`. | Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; lower actuator gain. |
| 215.77 | randomized_episode | episode 17 | Hard randomized episode with worst controller `expert_pd`. | Lower actuator gain; raise joint damping. |
| 215.15 | randomized_episode | episode 9 | Hard randomized episode with worst controller `rl_policy`. | Add observation smoothing; lower actuator gain. |
| 212.46 | randomized_episode | episode 5 | Hard randomized episode with worst controller `expert_pd`. | Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; raise joint damping. |
| 86.56 | benchmark_case | low_damping_high_gain / expert_pd | Elevated benchmark risk in `low_damping_high_gain` for `expert_pd`. | Increase joint damping and reduce actuator gain before changing controller structure. |
| 85.96 | benchmark_case | low_damping_high_gain / hybrid_guardrail | Elevated benchmark risk in `low_damping_high_gain` for `hybrid_guardrail`. | Increase joint damping and reduce actuator gain before changing controller structure. |
| 54.44 | benchmark_case | noise_heavy / expert_pd | Elevated benchmark risk in `noise_heavy` for `expert_pd`. | Add observation filtering or slightly lower controller aggressiveness under noisy sensing. |
| 54.41 | benchmark_case | noise_heavy / hybrid_guardrail | Elevated benchmark risk in `noise_heavy` for `hybrid_guardrail`. | Add observation filtering or slightly lower controller aggressiveness under noisy sensing. |
| 54.35 | benchmark_case | delay_heavy / expert_pd | Elevated benchmark risk in `delay_heavy` for `expert_pd`. | Increase control frequency or use a more delay-tolerant guarded policy blend. |
| 25.00 | release_review | 9947b32 -> HEAD | Recent change range to review from a support and release perspective. | Check changed areas with the highest file counts first and confirm docs, CI, and artifacts stayed aligned. |

## Evidence

- `episode 1`: Difficulty `1.1709`, success `0.000`, delay `5`, noise `0.0068`.
- `episode 14`: Difficulty `1.1667`, success `0.000`, delay `5`, noise `0.0110`.
- `episode 17`: Difficulty `1.1577`, success `0.000`, delay `0`, noise `0.0094`.
- `episode 9`: Difficulty `1.1515`, success `0.000`, delay `1`, noise `0.0172`.
- `episode 5`: Difficulty `1.1246`, success `0.000`, delay `4`, noise `0.0167`.
- `low_damping_high_gain / expert_pd`: Risk score `0.3656`, final error `0.0571`.
- `low_damping_high_gain / hybrid_guardrail`: Risk score `0.3596`, final error `0.0567`.
- `noise_heavy / expert_pd`: Risk score `0.0444`, final error `0.0474`.
- `noise_heavy / hybrid_guardrail`: Risk score `0.0441`, final error `0.0474`.
- `delay_heavy / expert_pd`: Risk score `0.0435`, final error `0.0442`.
- `9947b32 -> HEAD`: 31 files changed, 4413 insertions(+), 20 deletions(-)