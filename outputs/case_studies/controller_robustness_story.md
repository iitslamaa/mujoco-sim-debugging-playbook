# Case Study: Controller Robustness Under Stress and Randomization

This case study summarizes how different controller strategies behave under curated stress scenarios and randomized simulator conditions.

## Main observations

- In `baseline`, the strongest controller was `expert_pd` with `0.625` success rate and `0.0422` mean final error.
- In `delay_heavy`, the strongest controller was `hybrid_guardrail` with `0.625` success rate and `0.0437` mean final error.
- In `low_damping_high_gain`, the strongest controller was `torch_policy` with `0.625` success rate and `0.0536` mean final error.
- In `noise_heavy`, the strongest controller was `torch_policy` with `0.500` success rate and `0.0466` mean final error.

## Domain-randomization summary

| controller | success_rate | final_error_mean | control_energy_mean |
| --- | ---: | ---: | ---: |
| hybrid_guardrail | 0.222 | 0.0901 | 166.4058 |
| expert_pd | 0.222 | 0.0952 | 170.8299 |
| torch_policy | 0.167 | 0.0900 | 154.4788 |
| rl_policy | 0.167 | 0.0900 | 154.4787 |

## Interpretation

- The expert controller remains a strong baseline in nominal settings.
- The learned policy can match or exceed the expert in some noisy or aggressive regimes.
- The hybrid controller is useful when robustness matters more than peak nominal efficiency.
- Randomized evaluations reveal stability gaps that are easy to miss in fixed-scenario testing.

## Suggested next investigations

- Increase domain randomization during training instead of only at evaluation time.
- Compare deterministic policy evaluation against stochastic rollout sampling.
- Add explicit risk metrics for actuator saturation and recovery latency.
