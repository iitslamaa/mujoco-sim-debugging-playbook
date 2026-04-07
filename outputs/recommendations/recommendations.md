# Mitigation Recommendations

Recommended follow-up actions synthesized from anomaly analysis and sweep evidence.

## Prioritized actions

| target | severity | recommendation | tradeoff |
| --- | ---: | --- | --- |
| low_damping_high_gain / expert_pd | 0.3656 | Increase joint damping and reduce actuator gain before changing controller structure. | Higher damping reduces aggressiveness and may slightly slow settling. |
| low_damping_high_gain / hybrid_guardrail | 0.3596 | Increase joint damping and reduce actuator gain before changing controller structure. | Higher damping reduces aggressiveness and may slightly slow settling. |
| noise_heavy / expert_pd | 0.0444 | Add observation filtering or slightly lower controller aggressiveness under noisy sensing. | Filtering helps stability but can add lag and reduce responsiveness. |
| noise_heavy / hybrid_guardrail | 0.0441 | Add observation filtering or slightly lower controller aggressiveness under noisy sensing. | Filtering helps stability but can add lag and reduce responsiveness. |
| delay_heavy / expert_pd | 0.0435 | Increase control frequency or use a more delay-tolerant guarded policy blend. | Higher control frequency increases compute cost and can amplify noisy actuation if left untuned. |
| episode 1 | 1.1709 | Reduce control delay or switch to the guarded/learned policy family; lower actuator gain. | Mitigations that improve robustness can trade off speed, energy, or nominal performance. |
| episode 14 | 1.1667 | Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; lower actuator gain. | Mitigations that improve robustness can trade off speed, energy, or nominal performance. |
| episode 17 | 1.1577 | Lower actuator gain; raise joint damping. | Mitigations that improve robustness can trade off speed, energy, or nominal performance. |
| episode 9 | 1.1515 | Add observation smoothing; lower actuator gain. | Mitigations that improve robustness can trade off speed, energy, or nominal performance. |
| episode 5 | 1.1246 | Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; raise joint damping. | Mitigations that improve robustness can trade off speed, energy, or nominal performance. |

## Supporting evidence

- `low_damping_high_gain / expert_pd`: Highest benchmark risk is in `low_damping_high_gain`. Sweep evidence shows the best joint damping setting in the playbook is `5.5` with `0.0665` final error.
- `low_damping_high_gain / hybrid_guardrail`: Highest benchmark risk is in `low_damping_high_gain`. Sweep evidence shows the best joint damping setting in the playbook is `5.5` with `0.0665` final error.
- `noise_heavy / expert_pd`: The noisy scenario is among the top anomaly cases. Sweep rows around sensor noise show best success at `0.02` with `0.333` success.
- `noise_heavy / hybrid_guardrail`: The noisy scenario is among the top anomaly cases. Sweep rows around sensor noise show best success at `0.02` with `0.333` success.
- `delay_heavy / expert_pd`: Delay-heavy behavior is elevated in the benchmark, and the sweep suggests lower control_dt (`0.01`) gives the strongest success profile.
- `episode 1`: This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.
- `episode 14`: This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.
- `episode 17`: This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.
- `episode 9`: This randomized episode had `0.000` success rate with worst controller `rl_policy`. The playbook's best control_dt sweep setting is `0.01`.
- `episode 5`: This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.

## Sweep parameter rankings

| parameter | best_value | best_success_rate | worst_value | worst_success_rate |
| --- | ---: | ---: | ---: | ---: |
| actuator_gain | 18.0 | 0.833 | 52.0 | 0.250 |
| control_delay_steps | 0 | 0.250 | 6 | 0.250 |
| control_dt | 0.01 | 0.667 | 0.06 | 0.167 |
| friction_loss | 0.1 | 0.250 | 0.0 | 0.250 |
| joint_damping | 5.5 | 0.250 | 0.4 | 0.250 |
| sensor_noise_std | 0.02 | 0.333 | 0.0 | 0.250 |