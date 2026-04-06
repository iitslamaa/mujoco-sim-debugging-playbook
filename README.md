# mujoco-sim-debugging-playbook

> A reproducible MuJoCo project exploring how physics and control parameters affect a robotic reaching task, with experiment sweeps, plots, and debugging notes.

## Why this exists

This repo is designed to be more than "a robot moving in simulation."

It demonstrates:

- robotics simulation familiarity with MuJoCo
- Python engineering around experiments and reproducibility
- debugging instincts around unstable or degraded control behavior
- clear technical writing for user enablement

The core task is a planar 2-DoF robotic arm reaching for sampled workspace targets. A baseline inverse-kinematics-plus-PD controller is evaluated while varying important simulation and control parameters such as damping, actuator gain, noise, delay, and control frequency.

## Project highlights

- Baseline reaching controller using analytical inverse kinematics
- Config-driven experiment runner for repeatable sweeps
- Metrics for convergence, overshoot, oscillation, control effort, and success rate
- Plot generation for parameter sensitivity studies
- Markdown report generation summarizing results
- Troubleshooting guide that frames the repo like a simulation support/debugging playbook

## Repository layout

```text
.
├── configs/
│   ├── baseline.json
│   ├── interesting_sweeps.json
│   └── stress_sweeps.json
├── docs/
│   └── troubleshooting.md
├── scripts/
│   ├── plot_results.py
│   ├── run_baseline.py
│   └── run_sweep.py
├── src/mujoco_sim_debugging_playbook/
│   ├── assets/
│   │   └── planar_reacher.xml
│   ├── config.py
│   ├── controller.py
│   ├── experiment.py
│   ├── metrics.py
│   ├── plot.py
│   ├── report.py
│   └── simulation.py
└── tests/
    ├── test_config.py
    └── test_metrics.py
```

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## Run a baseline experiment

```bash
python scripts/run_baseline.py --episodes 12
```

This writes metrics and episode traces to `outputs/baseline/`.

## Run a parameter sweep

```bash
python scripts/run_sweep.py --config configs/interesting_sweeps.json
```

This produces:

- per-scenario JSON summaries
- combined CSV outputs
- sensitivity plots
- a generated Markdown report

## What each experiment tests

`configs/interesting_sweeps.json` focuses on realistic debugging scenarios:

- `joint_damping`: tests sluggishness vs. stability
- `actuator_gain`: tests underpowered vs. aggressive control
- `sensor_noise_std`: tests noisy observations and target tracking degradation
- `control_dt`: tests lower control rates and aliasing-like behavior
- `control_delay_steps`: tests latency-induced overshoot and recovery issues
- `friction_loss`: tests energy loss and convergence difficulty

`configs/stress_sweeps.json` pushes harder into regimes that often create interview-worthy failure cases:

- high delay with high gain
- low damping with aggressive actuators
- noisy sensing at reduced control rate
- compounded friction plus underactuation

## Key findings to look for

Once you run the sweeps, the most useful patterns to discuss are:

- lower damping often improves speed until oscillation dominates
- high actuator gain can reduce steady-state error but worsen overshoot
- delay hurts more when the controller is aggressive
- noise can make success rate collapse before average error looks terrible
- changing control rate can quietly shift the system from smooth to unstable

## Troubleshooting

The debugging guide lives in [docs/troubleshooting.md](/Users/lamayassine/mujoco/docs/troubleshooting.md) and covers:

- exploding trajectories
- oscillation and limit-cycle behavior
- success in one configuration but failure in another
- timestep and delay sensitivity
- how to inspect traces instead of guessing

## Resume framing

Built a public MuJoCo simulation project to analyze how control and physics parameters affect robotic reaching performance; created reproducible sweeps, visualized failure patterns, and documented debugging workflows for instability, observation noise, latency, and controller tuning.

