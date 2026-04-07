# Incident Bundle: INC-004

- Target: `episode 9`
- Kind: `randomized_episode`
- Priority score: `215.15`

## Summary

Hard randomized episode with worst controller `rl_policy`.

## Evidence

Difficulty `1.1515`, success `0.000`, delay `1`, noise `0.0172`.

## Next Action

Add observation smoothing; lower actuator gain.

## Recommendation Context

- Recommendation: Add observation smoothing; lower actuator gain.
- Tradeoff: Mitigations that improve robustness can trade off speed, energy, or nominal performance.
- Supporting evidence: This randomized episode had `0.000` success rate with worst controller `rl_policy`. The playbook's best control_dt sweep setting is `0.01`.

## Anomaly Context

```json
{
  "episode": 9,
  "difficulty_score": 1.151461366675756,
  "avg_final_error": 0.1514613666757561,
  "success_rate": 0.0,
  "best_controller": "hybrid_guardrail",
  "worst_controller": "rl_policy",
  "worst_final_error": 0.15414417465008007,
  "joint_damping": 1.3510857586984368,
  "actuator_gain": 53.06512399670722,
  "sensor_noise_std": 0.017233493284833652,
  "control_delay_steps": 1
}
```
