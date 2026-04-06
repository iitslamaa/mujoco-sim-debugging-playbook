# Troubleshooting Guide

This project is intentionally built like a small simulation-support playbook. The point is not only to run a controller, but to diagnose why behavior changes when the simulation or control loop changes.

## Symptom: the arm oscillates around the target

Common causes:

- high `actuator_gain`
- low `joint_damping`
- delayed control updates
- low derivative damping in the controller

What to inspect:

- joint error traces over time
- end-effector distance to target
- control effort spikes
- whether oscillation appears only after the target is nearly reached

Typical fix directions:

- increase `joint_damping`
- reduce `actuator_gain`
- increase controller `kd`
- reduce `control_delay_steps`

## Symptom: behavior is stable but too slow

Common causes:

- high `joint_damping`
- large `friction_loss`
- low `actuator_gain`
- conservative `kp`

What to inspect:

- settling time
- final error after the episode horizon
- whether success rate is high but convergence is late

Typical fix directions:

- increase `actuator_gain`
- reduce damping or friction
- raise `kp` carefully and watch for overshoot

## Symptom: performance collapses when noise is enabled

Common causes:

- controller overreacts to noisy observations
- the system only looks robust in perfectly clean simulation
- success threshold is too tight for the observation quality

What to inspect:

- success rate versus mean final error
- control effort variance
- whether only some targets become brittle

Typical fix directions:

- lower `kp`
- raise `kd`
- add simple observation filtering
- document sensitivity instead of hiding it

## Symptom: small timestep or control-rate changes produce very different results

Common causes:

- controller tuned to one update rate
- unstable interaction between aggressive gains and low-rate control
- hidden sensitivity to sample-and-hold behavior

What to inspect:

- identical target sets run under different `control_dt`
- overshoot and oscillation index instead of only reward
- whether failure appears only on targets near the workspace boundary

Typical fix directions:

- retune gains for the new control period
- shorten control delay
- lower actuator aggressiveness

## Symptom: one parameter setting succeeds and a nearby one fails

This is exactly the kind of pattern worth documenting. Do not hand-wave it away.

What to do:

1. Compare per-episode traces for the same random seed and target set.
2. Check whether failure is due to one bad target or a broad performance shift.
3. Look at overshoot, settling time, and control effort together.
4. Write down whether the failure mode is instability, sluggishness, or sensitivity to noise/delay.

## Debugging workflow

1. Start from the baseline config.
2. Change one variable at a time.
3. Keep seeds fixed while comparing behaviors.
4. Use both scalar metrics and time-series traces.
5. Summarize what changed in plain language, not only in plots.

