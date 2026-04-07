# Why does episode 17 fail under randomized conditions?

## Short Answer

Hard randomized episode with worst controller `expert_pd`. Recommended first step: Lower actuator gain; raise joint damping.

## Evidence

- Difficulty `1.1577`, success `0.000`, delay `0`, noise `0.0094`.

## Recommended Action

Lower actuator gain; raise joint damping.

## Tradeoff

Mitigations that improve robustness can trade off speed, energy, or nominal performance.

## Supporting Context

This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.

## Related Incident

- Incident id: `INC-003`
- Target: `episode 17`
