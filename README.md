# mujoco-sim-debugging-playbook

> A support-first MuJoCo project for reproducing simulation failures, running parameter sweeps, training a PyTorch policy, and packaging diagnostics, docs, and artifacts around robot control behavior.

## Why this exists

This repo is designed to be more than "a robot moving in simulation."

It is deliberately structured like a miniature simulation support lab:

- a reproducible robot task
- parameter sensitivity experiments
- support-case reproduction artifacts
- user-facing debugging docs
- issue templates, CI, Docker, and contributor workflows

It demonstrates:

- robotics simulation familiarity with MuJoCo
- Python engineering around experiments and reproducibility
- debugging instincts around unstable or degraded control behavior
- clear technical writing for user enablement
- support-triage thinking for user-reported failures
- PyTorch fluency through a learned imitation baseline, training curves, checkpoints, and evaluation rollouts
- Linux-style tooling with bash, Docker, CI, and GitHub workflows

The core task is a planar 2-DoF robotic arm reaching for sampled workspace targets. A baseline inverse-kinematics-plus-PD controller is evaluated while varying important simulation and control parameters such as damping, actuator gain, noise, delay, and control frequency.

## Project highlights

- Baseline reaching controller using analytical inverse kinematics
- Config-driven experiment runner for repeatable sweeps
- Metrics for convergence, overshoot, oscillation, control effort, and success rate
- Plot generation for parameter sensitivity studies
- Markdown report generation summarizing results
- Troubleshooting guide that frames the repo like a simulation support/debugging playbook
- Support-case library with response-draft generation
- Diagnostics bundles with environment capture and scenario comparisons
- PyTorch imitation-learning pipeline with dataset generation, training, and policy evaluation
- Online RL fine-tuning stage that adapts the imitation policy inside MuJoCo
- Static dashboard for browsing artifacts, environment details, and support cases
- Multi-controller benchmark comparing expert, learned, and guarded hybrid control
- Domain-randomization evaluation that measures policy robustness under changing physics
- Automated case-study generation that turns experiment outputs into polished narratives
- Regression snapshot and diff tooling for tracking behavior drift over time
- Threshold-based regression gates for catching unacceptable drift in CI
- Historical trend reporting for tracking metric drift across snapshots
- Artifact manifests and a provenance index for tying outputs back to code, inputs, and Git state
- Commit-linked release notes for summarizing code, metric, and artifact changes between Git SHAs
- Scenario-level anomaly analysis that pinpoints brittle controller/scenario combinations and hard randomized episodes
- Automated mitigation recommendations that turn anomalies into actionable tuning guidance
- A synthesized support triage queue that prioritizes what an engineer should inspect first
- Incident bundles that package top-priority issues into handoff-ready case files
- Demo GIF generation for a stronger GitHub landing page
- Docker and `Makefile` workflows for reproducible local setup
- GitHub issue templates and CI for public-repo readiness

![PyTorch policy rollout](outputs/media/reacher_demo.gif)

![Training curve](outputs/learning/training/training_curve.png)

## Repository layout

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── cases/
│   └── issue_cases/
├── configs/
├── docs/
├── outputs/
├── scripts/
├── src/mujoco_sim_debugging_playbook/
└── tests/
```

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e . --no-build-isolation
```

## Docker

```bash
docker compose build
docker compose run --rm sim-debug
```

## Quickstart

```bash
make install
make test
make baseline
make support-case
make diagnostics
make train-policy
make eval-policy
make train-rl
make eval-rl
make benchmark
make randomization
make anomalies
make recommendations
make triage
make incidents
make case-studies
make snapshot
make regression-diff
make regression-check
make regression-history
make provenance
make release-notes
make demo-gif
make dashboard
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

## Run a support case

```bash
python scripts/run_issue_case.py --case actuator_gain_overshoot
```

This generates a support-style Markdown response draft under `outputs/support_cases/` using the saved sweep summaries.

## Train a PyTorch policy

```bash
python scripts/train_torch_policy.py --dataset-episodes 20 --epochs 80
python scripts/evaluate_torch_policy.py --episodes 8
```

This pipeline:

- collects expert rollouts from the analytical MuJoCo controller
- builds an imitation dataset
- trains a multilayer PyTorch policy network
- saves checkpoints and a training curve
- evaluates the learned policy back in MuJoCo

## Fine-tune with RL

```bash
python scripts/train_rl_policy.py --iterations 12 --episodes-per-iteration 6
python scripts/evaluate_rl_policy.py --episodes 8
```

This stage starts from the imitation policy and performs online policy-gradient adaptation directly in MuJoCo.

## Dashboard and demo media

```bash
python scripts/generate_demo_gif.py \
  --trace outputs/learning/evaluation/traces/episode_000.json \
  --output outputs/media/reacher_demo.gif \
  --title "PyTorch policy rollout"

python scripts/generate_dashboard.py
```

This produces:

- `outputs/media/reacher_demo.gif`
- `dashboard/index.html`
- `dashboard/data.json`

## Run a controller benchmark

```bash
python scripts/run_controller_benchmark.py
```

This benchmark compares:

- `expert_pd`
- `torch_policy`
- `hybrid_guardrail`

across a scenario suite with baseline, noise-heavy, delay-heavy, and low-damping/high-gain conditions.

## Run domain-randomization evaluation

```bash
python scripts/run_domain_randomization.py
```

This evaluates controllers under episode-to-episode randomized damping, friction, actuator gain, observation noise, and control delay.

## Generate a case study

```bash
python scripts/generate_case_studies.py
```

This produces a higher-level writeup and summary visual from the benchmark and domain-randomization outputs.

## Track regressions

```bash
python scripts/create_regression_snapshot.py --name current
python scripts/compare_regression_snapshots.py \
  --left outputs/regression/snapshots/baseline_reference.json \
  --right outputs/regression/snapshots/current.json
```

This captures a summary snapshot and generates a diff report against a reference snapshot.

## Enforce regression thresholds

```bash
python scripts/check_regressions.py \
  --left outputs/regression/snapshots/baseline_reference.json \
  --right outputs/regression/snapshots/current.json \
  --thresholds configs/regression_thresholds.json \
  --output-dir outputs/regression/gate
```

This evaluates the diff against explicit policy limits and writes a pass/fail gate report.

## Build regression history

```bash
python scripts/build_regression_history.py \
  --snapshot-dir outputs/regression/snapshots \
  --output-dir outputs/regression/history \
  --gate-report outputs/regression/gate/regression_gate.json
```

This compiles saved snapshots into a small history dataset with trend summaries and a multi-metric plot.

## Build provenance artifacts

```bash
python scripts/backfill_provenance_manifests.py
python scripts/build_provenance_index.py
```

This writes per-run `manifest.json` files plus a repo-level provenance index for browsing generated outputs.

## Generate release notes

```bash
python scripts/generate_release_notes.py \
  --base 9947b32 \
  --head HEAD \
  --output-dir outputs/releases/latest
```

This produces a compact release summary that ties together Git commits, changed files, regression status, and provenance coverage.

## Generate anomaly analysis

```bash
python scripts/generate_anomaly_report.py \
  --benchmark outputs/controller_benchmark/benchmark_summary.json \
  --randomization outputs/domain_randomization/evaluation_rows.json \
  --output-dir outputs/anomalies
```

This ranks the riskiest benchmark cases, highlights the hardest randomized episodes, and estimates which simulator parameters correlate most with difficulty.

## Generate mitigation recommendations

```bash
python scripts/generate_recommendations.py \
  --anomalies outputs/anomalies/anomaly_report.json \
  --sweeps outputs/interesting_sweeps/combined_summary.json \
  --output-dir outputs/recommendations
```

This turns anomaly findings into concrete follow-up actions with supporting sweep evidence and tradeoff notes.

## Generate a support triage queue

```bash
python scripts/generate_triage_queue.py \
  --anomalies outputs/anomalies/anomaly_report.json \
  --recommendations outputs/recommendations/recommendations.json \
  --regression-gate outputs/regression/gate/regression_gate.json \
  --release-notes outputs/releases/latest/release_notes.json \
  --output-dir outputs/triage
```

This prioritizes the highest-value follow-up items using anomaly severity, release scope, and current regression state.

## Generate incident bundles

```bash
python scripts/generate_incident_bundles.py \
  --triage outputs/triage/triage_queue.json \
  --anomalies outputs/anomalies/anomaly_report.json \
  --recommendations outputs/recommendations/recommendations.json \
  --output-dir outputs/incidents \
  --limit 5
```

This creates handoff-ready case files for the highest-priority support items.

## Generate a diagnostics bundle

```bash
python scripts/generate_diagnostics_bundle.py \
  --summary outputs/baseline/summary.json \
  --label baseline \
  --summary outputs/interesting_sweeps/actuator_gain_18p0/summary.json \
  --label actuator_gain_18
```

This writes:

- `outputs/diagnostics/diagnostics.md`
- `outputs/diagnostics/environment.json`
- per-episode trace plots under each experiment output directory

## Public-repo / support-facing assets

- [support-playbook.md](/Users/lamayassine/mujoco/docs/support-playbook.md)
- [release-validation.md](/Users/lamayassine/mujoco/docs/release-validation.md)
- [diagnostics-guide.md](/Users/lamayassine/mujoco/docs/diagnostics-guide.md)
- [dashboard/index.html](/Users/lamayassine/mujoco/dashboard/index.html)
- [learning-guide.md](/Users/lamayassine/mujoco/docs/learning-guide.md)
- [case-study-guide.md](/Users/lamayassine/mujoco/docs/case-study-guide.md)
- [regression-guide.md](/Users/lamayassine/mujoco/docs/regression-guide.md)
- [provenance-guide.md](/Users/lamayassine/mujoco/docs/provenance-guide.md)
- [index.md](/Users/lamayassine/mujoco/outputs/provenance/index.md)
- [release_notes.md](/Users/lamayassine/mujoco/outputs/releases/latest/release_notes.md)
- [bug_report.yml](/Users/lamayassine/mujoco/.github/ISSUE_TEMPLATE/bug_report.yml)
- [support_request.yml](/Users/lamayassine/mujoco/.github/ISSUE_TEMPLATE/support_request.yml)
- [ci.yml](/Users/lamayassine/mujoco/.github/workflows/ci.yml)
- [CONTRIBUTING.md](/Users/lamayassine/mujoco/CONTRIBUTING.md)
- [Dockerfile](/Users/lamayassine/mujoco/Dockerfile)

## What each experiment tests

`configs/interesting_sweeps.json` focuses on realistic debugging scenarios:

- `joint_damping`: tests sluggishness vs. stability
- `actuator_gain`: tests underpowered vs. aggressive control
- `sensor_noise_std`: tests noisy observations and target tracking degradation
- `control_dt`: tests lower control rates and aliasing-like behavior
- `control_delay_steps`: tests latency-induced overshoot and recovery issues
- `friction_loss`: tests energy loss and convergence difficulty

`configs/stress_sweeps.json` pushes harder into regimes that often produce more severe and interesting failure cases:

- high delay with high gain
- low damping with aggressive actuators
- noisy sensing at reduced control rate
- compounded friction plus underactuation

## Included support cases

- `actuator_gain_overshoot`: a user makes the arm faster but accidentally worsens overshoot and success rate
- `delay_instability`: a user adds control delay and sees wobble near the target
- `noisy_observation_regression`: a user enables sensor noise and sees success collapse before mean error looks awful

These are intentionally written like public support tickets: a problem statement, a repro command, a checklist, and a draft response.

## Diagnostics and provenance

Each experiment now captures more than scalar metrics:

- summary data with environment metadata
- per-episode trace manifests
- trace plots for visual debugging
- comparison tooling for baseline-vs-candidate analysis

That makes the repo easier to talk about as a real engineering/debugging system instead of only an academic experiment.

## PyTorch learning workflow

The repo now includes a learned baseline rather than only a hand-written controller:

- expert data is generated from MuJoCo controller rollouts
- state vectors include joint position, joint velocity, and target coordinates
- a PyTorch MLP policy is trained to imitate expert torques
- checkpoints, loss curves, and evaluation summaries are saved as reproducible artifacts
- the learned policy can be compared directly against the expert controller
- the imitation policy can be fine-tuned online with RL and re-evaluated in the same simulator

## Controller benchmark

The repo also includes a robustness benchmark for comparing controllers under stress:

- expert PD control
- learned PyTorch policy
- a hybrid guardrail controller that falls back toward expert behavior when state error grows

That makes the project more interesting than a simple baseline-vs-policy comparison because it shows evaluation, failure analysis, and pragmatic safety-minded controller design.

## Domain randomization

The repo also evaluates how controllers generalize when simulator parameters shift every episode:

- joint damping is randomized
- friction loss is randomized
- actuator gain is randomized
- observation noise is randomized
- control delay is randomized

This gives the project a stronger robustness and sim-to-real flavored evaluation story.

## Generated case studies

The repo can also synthesize raw experiment outputs into polished summary artifacts:

- a Markdown case study
- a summary graphic for quick scanning
- reusable conclusions grounded in benchmark and randomization results

## Regression tracking

The repo can snapshot its current performance surface and compare it against a saved reference:

- baseline metrics
- imitation and RL evaluation metrics
- controller benchmark aggregates
- domain-randomization robustness aggregates

That makes it easier to treat the project like a maintained platform instead of a one-time report.

## Key findings to look for

Once you run the sweeps, the most useful patterns to discuss are:

- lower damping often improves speed until oscillation dominates
- high actuator gain can reduce steady-state error but worsen overshoot
- delay hurts more when the controller is aggressive
- noise can make success rate collapse before average error looks terrible
- changing control rate can quietly shift the system from smooth to unstable

## Troubleshooting

The debugging guide lives in [troubleshooting.md](/Users/lamayassine/mujoco/docs/troubleshooting.md) and covers:

- exploding trajectories
- oscillation and limit-cycle behavior
- success in one configuration but failure in another
- timestep and delay sensitivity
- how to inspect traces instead of guessing
