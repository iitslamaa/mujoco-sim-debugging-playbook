# Incident Bundle: INC-001

- Target: `episode 1`
- Kind: `randomized_episode`
- Priority score: `217.09`

## Summary

Hard randomized episode with worst controller `expert_pd`.

## Evidence

Difficulty `1.1709`, success `0.000`, delay `5`, noise `0.0068`.

## Next Action

Reduce control delay or switch to the guarded/learned policy family; lower actuator gain.

## Recommendation Context

- Recommendation: Reduce control delay or switch to the guarded/learned policy family; lower actuator gain.
- Tradeoff: Mitigations that improve robustness can trade off speed, energy, or nominal performance.
- Supporting evidence: This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.

## Anomaly Context

```json
{
  "episode": 1,
  "difficulty_score": 1.1708717748779893,
  "avg_final_error": 0.17087177487798924,
  "success_rate": 0.0,
  "best_controller": "rl_policy",
  "worst_controller": "expert_pd",
  "worst_final_error": 0.18158924545080263,
  "joint_damping": 1.729174779325379,
  "actuator_gain": 46.894996522872425,
  "sensor_noise_std": 0.006776718264752566,
  "control_delay_steps": 5
}
```
