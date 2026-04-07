# Why does episode 5 fail under randomized conditions?

## Short Answer

Hard randomized episode with worst controller `expert_pd`. Recommended first step: Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; raise joint damping.

## Evidence

- Difficulty `1.1246`, success `0.000`, delay `4`, noise `0.0167`.

## Recommended Action

Reduce control delay or switch to the guarded/learned policy family; add observation smoothing; raise joint damping.

## Tradeoff

Mitigations that improve robustness can trade off speed, energy, or nominal performance.

## Supporting Context

This randomized episode had `0.000` success rate with worst controller `expert_pd`. The playbook's best control_dt sweep setting is `0.01`.

## Related Incident

- Incident id: `INC-005`
- Target: `episode 5`
