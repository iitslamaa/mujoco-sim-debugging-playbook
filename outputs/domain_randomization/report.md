# Domain Randomization Report

Controllers evaluated under episode-to-episode randomized simulator parameters.

| controller | success_rate | final_error_mean | overshoot_mean | oscillation_mean | control_energy_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| hybrid_guardrail | 0.222 | 0.0901 | 0.0008 | 0.9754 | 166.4058 |
| expert_pd | 0.222 | 0.0952 | 0.0009 | 0.9729 | 170.8299 |
| torch_policy | 0.167 | 0.0900 | 0.0055 | 0.9751 | 154.4788 |
| rl_policy | 0.167 | 0.0900 | 0.0055 | 0.9751 | 154.4787 |

Most robust by success rate: `hybrid_guardrail`.
