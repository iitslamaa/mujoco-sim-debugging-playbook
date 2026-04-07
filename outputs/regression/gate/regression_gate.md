# Regression Gate

Comparison: `baseline_reference` -> `current`

Status: **PASS**

Violation count: `0`

## Violations

- None

## Scalar checks

| metric | delta | min | max | passed |
| --- | ---: | ---: | ---: | --- |
| baseline_success_rate | 0.0000 | -0.0500 | -- | yes |
| baseline_final_error_mean | 0.0000 | -- | 0.0200 | yes |
| imitation_success_rate | 0.0000 | -0.0800 | -- | yes |
| imitation_final_error_mean | 0.0000 | -- | 0.0300 | yes |
| rl_success_rate | 0.0000 | -0.0800 | -- | yes |
| rl_final_error_mean | 0.0000 | -- | 0.0300 | yes |

## Controller checks

### benchmark_success_rate_by_controller

| controller | delta | min | max | passed |
| --- | ---: | ---: | ---: | --- |
| expert_pd | 0.0000 | -0.1000 | -- | yes |
| hybrid_guardrail | 0.0000 | -0.1000 | -- | yes |
| torch_policy | 0.0000 | -0.1000 | -- | yes |

### randomization_success_rate_by_controller

| controller | delta | min | max | passed |
| --- | ---: | ---: | ---: | --- |
| expert_pd | 0.0000 | -0.1200 | -- | yes |
| hybrid_guardrail | 0.0000 | -0.1200 | -- | yes |
| rl_policy | 0.0000 | -0.1200 | -- | yes |
| torch_policy | 0.0000 | -0.1200 | -- | yes |

### randomization_final_error_by_controller

| controller | delta | min | max | passed |
| --- | ---: | ---: | ---: | --- |
| expert_pd | 0.0000 | -- | 0.0400 | yes |
| hybrid_guardrail | 0.0000 | -- | 0.0400 | yes |
| rl_policy | 0.0000 | -- | 0.0400 | yes |
| torch_policy | 0.0000 | -- | 0.0400 | yes |
