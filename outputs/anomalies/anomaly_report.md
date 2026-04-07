# Anomaly Report

Scenario-level anomaly analysis across the controller benchmark and domain randomization suite.

## Highest-risk benchmark cases

| scenario | controller | risk_score | success_gap | error_gap | energy_gap |
| --- | --- | ---: | ---: | ---: | ---: |
| low_damping_high_gain | expert_pd | 0.3656 | 0.0000 | 0.0034 | 19.7965 |
| low_damping_high_gain | hybrid_guardrail | 0.3596 | 0.0000 | 0.0030 | 19.9158 |
| noise_heavy | expert_pd | 0.0444 | 0.0000 | 0.0008 | 1.9128 |
| noise_heavy | hybrid_guardrail | 0.0441 | 0.0000 | 0.0008 | 1.8916 |
| delay_heavy | expert_pd | 0.0435 | 0.0000 | 0.0005 | 2.2343 |
| baseline | torch_policy | 0.0403 | 0.0000 | 0.0020 | 0.0000 |
| baseline | hybrid_guardrail | 0.0318 | 0.0000 | 0.0002 | 1.8533 |
| baseline | expert_pd | 0.0279 | 0.0000 | 0.0000 | 1.8627 |

## Hardest randomized episodes

| episode | difficulty_score | best | worst | avg_final_error | success_rate | delay | noise | gain | damping |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1.1709 | rl_policy | expert_pd | 0.1709 | 0.0000 | 5 | 0.0068 | 46.8950 | 1.7292 |
| 14 | 1.1667 | rl_policy | expert_pd | 0.1667 | 0.0000 | 5 | 0.0110 | 47.6685 | 3.7821 |
| 17 | 1.1577 | rl_policy | expert_pd | 0.1577 | 0.0000 | 0 | 0.0094 | 46.4222 | 0.8849 |
| 9 | 1.1515 | hybrid_guardrail | rl_policy | 0.1515 | 0.0000 | 1 | 0.0172 | 53.0651 | 1.3511 |
| 5 | 1.1246 | rl_policy | expert_pd | 0.1246 | 0.0000 | 4 | 0.0167 | 37.2398 | 1.0589 |
| 13 | 1.1133 | hybrid_guardrail | rl_policy | 0.1133 | 0.0000 | 1 | 0.0009 | 54.7156 | 1.8944 |
| 4 | 1.1101 | hybrid_guardrail | torch_policy | 0.1101 | 0.0000 | 4 | 0.0117 | 34.5466 | 3.3071 |
| 6 | 1.0962 | hybrid_guardrail | torch_policy | 0.0962 | 0.0000 | 3 | 0.0176 | 30.2195 | 3.8086 |

## Parameter effects

| parameter | correlation_with_difficulty |
| --- | ---: |
| friction_loss | -0.4415 |
| control_delay_steps | 0.2885 |
| actuator_gain | 0.2842 |
| joint_damping | -0.1272 |
| sensor_noise_std | -0.0623 |