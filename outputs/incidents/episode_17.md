# Incident Bundle: INC-003

- Target: `episode 17`
- Kind: `randomized_episode`
- Priority score: `215.77`

## Summary

Hard randomized episode with worst controller `expert_pd`.

## Evidence

Difficulty `1.1577`, success `0.000`, delay `0`, noise `0.0094`.

## Next Action

Lower actuator gain; raise joint damping.

## Recommendation Context

- Recommendation: Lower actuator gain; raise joint damping.
- Tradeoff: Mitigations that improve robustness can trade off speed, energy, or nominal performance.
- Supporting evidence: This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.

## Anomaly Context

```json
{
  "episode": 17,
  "difficulty_score": 1.1577372914512094,
  "avg_final_error": 0.15773729145120932,
  "success_rate": 0.0,
  "best_controller": "rl_policy",
  "worst_controller": "expert_pd",
  "worst_final_error": 0.15906712664537617,
  "joint_damping": 0.8849033957559737,
  "actuator_gain": 46.42217069731403,
  "sensor_noise_std": 0.009361803923376447,
  "control_delay_steps": 0
}
```
