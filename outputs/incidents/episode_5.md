# Incident Bundle: INC-005

- Target: `episode 5`
- Kind: `randomized_episode`
- Priority score: `212.46`

## Summary

Hard randomized episode with worst controller `expert_pd`.

## Evidence

Difficulty `1.1246`, success `0.000`, delay `4`, noise `0.0167`.

## Next Action

Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; raise joint damping.

## Recommendation Context

- Recommendation: Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; raise joint damping.
- Tradeoff: Mitigations that improve robustness can trade off speed, energy, or nominal performance.
- Supporting evidence: This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.

## Anomaly Context

```json
{
  "episode": 5,
  "difficulty_score": 1.12455734536996,
  "avg_final_error": 0.12455734536995995,
  "success_rate": 0.0,
  "best_controller": "rl_policy",
  "worst_controller": "expert_pd",
  "worst_final_error": 0.13033066401262156,
  "joint_damping": 1.058942999724618,
  "actuator_gain": 37.2397730888738,
  "sensor_noise_std": 0.01674931029848154,
  "control_delay_steps": 4
}
```
