# Incident Bundle: INC-002

- Target: `episode 14`
- Kind: `randomized_episode`
- Priority score: `216.67`

## Summary

Hard randomized episode with worst controller `expert_pd`.

## Evidence

Difficulty `1.1667`, success `0.000`, delay `5`, noise `0.0110`.

## Next Action

Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; lower actuator gain.

## Recommendation Context

- Recommendation: Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; lower actuator gain.
- Tradeoff: Mitigations that improve robustness can trade off speed, energy, or nominal performance.
- Supporting evidence: This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.

## Anomaly Context

```json
{
  "episode": 14,
  "difficulty_score": 1.166659123947502,
  "avg_final_error": 0.16665912394750193,
  "success_rate": 0.0,
  "best_controller": "rl_policy",
  "worst_controller": "expert_pd",
  "worst_final_error": 0.17820569813513884,
  "joint_damping": 3.782089089350272,
  "actuator_gain": 47.668466249738096,
  "sensor_noise_std": 0.011028728485583719,
  "control_delay_steps": 5
}
```
