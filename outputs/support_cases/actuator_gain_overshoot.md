# Support Case: Higher actuator gain improves speed but destabilizes final approach

## User report

I raised actuator_gain because the arm looked too sluggish. It moves faster now, but success rate actually dropped and I see a lot more wobble near the goal. Why would more authority make performance worse?

## Reproduction

```bash
python scripts/run_sweep.py --config configs/interesting_sweeps.json
```

## Investigation checklist

- Compare success rate, overshoot, and control energy together
- Explain the interaction between gain, damping, and delay
- Confirm that the user did not retune controller gains when changing actuator strength

## Observed sweep summary

- Parameter: `actuator_gain`
- Best success rate: `18.0` -> `0.833`
- Worst success rate: `38.0` -> `0.250`
- Highest overshoot: `70.0` -> `0.0042`

| value | success_rate | final_error_mean | overshoot_mean | oscillation_mean |
| --- | ---: | ---: | ---: | ---: |
| 18.0 | 0.833 | 0.0228 | 0.0014 | 0.7931 |
| 28.0 | 0.667 | 0.0414 | 0.0006 | 0.8716 |
| 38.0 | 0.250 | 0.0705 | 0.0011 | 0.9181 |
| 52.0 | 0.250 | 0.0943 | 0.0028 | 0.9808 |
| 70.0 | 0.333 | 0.0875 | 0.0042 | 0.9852 |

## Suggested support response

Thanks for the detailed report. I was able to reproduce the behavior with the documented sweep outputs.

- Explain why more aggressive actuation can amplify oscillation
- Recommend retuning the controller after changing actuator authority
- Point the user to the actuator gain sweep report and plot

## Next actions

- Re-run the baseline and the relevant sweep while keeping the same seed.
- Compare the generated plot and `combined_summary.json` for this parameter.
- If the behavior still looks surprising, inspect one per-episode trace and tune one variable at a time.
