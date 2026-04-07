# Why does episode 9 fail under randomized conditions?

## Short Answer

Hard randomized episode with worst controller `rl_policy`. Recommended first step: Add observation smoothing; lower actuator gain.

## Evidence

- Difficulty `1.1515`, success `0.000`, delay `1`, noise `0.0172`.

## Recommended Action

Add observation smoothing; lower actuator gain.

## Tradeoff

Mitigations that improve robustness can trade off speed, energy, or nominal performance.

## Supporting Context

This randomized episode had `0.000` success rate with worst controller `rl_policy`. The playbook's best control_dt sweep setting is `0.01`.

## Related Incident

- Incident id: `INC-004`
- Target: `episode 9`
