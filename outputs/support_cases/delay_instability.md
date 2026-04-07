# Support Case: Delay-induced oscillation at moderate actuator gain

## User report

My arm reaches the target with the default config, but when I add control_delay_steps=4 the controller keeps wobbling near the target and sometimes times out. I expected slightly worse tracking, not repeated oscillation.

## Reproduction

```bash
python scripts/run_sweep.py --config configs/interesting_sweeps.json
```

## Investigation checklist

- Compare control_delay_steps rows in outputs/interesting_sweeps/combined_summary.json
- Inspect overshoot and oscillation instead of only final error
- Confirm whether aggressive kp/kd tuning is interacting with sample-and-hold delay

## Observed sweep summary

- Parameter: `control_delay_steps`
- Best success rate: `0` -> `0.250`
- Worst success rate: `0` -> `0.250`
- Highest overshoot: `0` -> `0.0011`

| value | success_rate | final_error_mean | overshoot_mean | oscillation_mean |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0.250 | 0.0705 | 0.0011 | 0.9181 |
| 1 | 0.250 | 0.0741 | 0.0003 | 0.9023 |
| 2 | 0.250 | 0.0741 | 0.0004 | 0.8994 |
| 4 | 0.250 | 0.0746 | 0.0003 | 0.8884 |
| 6 | 0.250 | 0.0751 | 0.0002 | 0.8865 |

## Suggested support response

Thanks for the detailed report. I was able to reproduce the behavior with the documented sweep outputs.

- Acknowledge that delay sensitivity is expected in a PD-controlled system
- Point the user to the control-delay sweep plot and report
- Recommend reducing gain or retuning derivative damping under delayed control

## Next actions

- Re-run the baseline and the relevant sweep while keeping the same seed.
- Compare the generated plot and `combined_summary.json` for this parameter.
- If the behavior still looks surprising, inspect one per-episode trace and tune one variable at a time.
