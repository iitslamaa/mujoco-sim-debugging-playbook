# Diagnostics Bundle

Automatically generated environment and experiment diagnostics.

## Environment

- Platform: `Darwin 25.2.0`
- Machine: `arm64`
- Python: `3.10.2`
- MuJoCo: `3.6.0`
- NumPy: `2.2.6`
- Git HEAD: `141f2e7b251c51afbda3f9bee04c61433060c4c6`

## Experiment summaries

| label | success_rate | final_error_mean | overshoot_mean | oscillation_mean | worst_episode |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.100 | 0.0943 | 0.0007 | 0.9799 | 9 |
| actuator_gain_18 | 0.833 | 0.0228 | 0.0014 | 0.7931 | 4 |

## Comparisons

| baseline | candidate | success_delta | final_error_delta | overshoot_delta | oscillation_delta |
| --- | --- | ---: | ---: | ---: | ---: |
| baseline | actuator_gain_18 | 0.733 | -0.0715 | 0.0008 | -0.1868 |
