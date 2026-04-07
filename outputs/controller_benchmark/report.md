# Controller Benchmark

Expert, learned, and guarded hybrid controllers compared across scenario stressors.

## baseline

| controller | success_rate | final_error_mean | overshoot_mean | oscillation_mean | control_energy_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| expert_pd | 0.625 | 0.0422 | 0.0009 | 0.8944 | 170.8597 |
| hybrid_guardrail | 0.625 | 0.0424 | 0.0009 | 0.8944 | 170.8502 |
| torch_policy | 0.625 | 0.0442 | 0.0010 | 0.8915 | 168.9969 |

Best success in this scenario: `expert_pd` at `0.625` success rate.

## delay_heavy

| controller | success_rate | final_error_mean | overshoot_mean | oscillation_mean | control_energy_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| hybrid_guardrail | 0.625 | 0.0437 | 0.0015 | 0.8872 | 170.5882 |
| expert_pd | 0.625 | 0.0442 | 0.0011 | 0.8872 | 171.2312 |
| torch_policy | 0.625 | 0.0442 | 0.0010 | 0.8915 | 168.9969 |

Best success in this scenario: `hybrid_guardrail` at `0.625` success rate.

## low_damping_high_gain

| controller | success_rate | final_error_mean | overshoot_mean | oscillation_mean | control_energy_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| torch_policy | 0.625 | 0.0536 | 0.0013 | 0.9555 | 159.5685 |
| hybrid_guardrail | 0.625 | 0.0567 | 0.0008 | 0.9648 | 179.4843 |
| expert_pd | 0.625 | 0.0571 | 0.0008 | 0.9634 | 179.3650 |

Best success in this scenario: `torch_policy` at `0.625` success rate.

## noise_heavy

| controller | success_rate | final_error_mean | overshoot_mean | oscillation_mean | control_energy_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| torch_policy | 0.500 | 0.0466 | 0.0009 | 0.8168 | 169.1158 |
| expert_pd | 0.500 | 0.0474 | 0.0008 | 0.8355 | 171.0286 |
| hybrid_guardrail | 0.500 | 0.0474 | 0.0008 | 0.8355 | 171.0074 |

Best success in this scenario: `torch_policy` at `0.500` success rate.
