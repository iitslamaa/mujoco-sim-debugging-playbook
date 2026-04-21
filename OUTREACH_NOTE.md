# Outreach Note

## Repo Strategy

Keep this repository as the full engineering record. It shows iteration, tests, generated artifacts, and breadth.

For outreach, do not send someone into the whole repo cold. Link the focused packet first:

- `outputs/hiring_manager_packet/hiring_manager_packet.md` for an engineering manager
- `EARTHMOVING_SIMULATION_PACKET.md`
- `outputs/earthmoving_dashboard/index.html`
- `outputs/earthmoving_role_brief/role_brief.md`

If a reviewer wants depth, the rest of the repo is there as evidence.

## Short Recruiter Message

```text
Hi [Name],

I know you suggested reconnecting later, but I wanted to send one focused update because I took your feedback seriously.

Since we last spoke, I built a MuJoCo-based autonomous construction simulation track around the areas your Simulation role emphasizes: terrain deformation, earthmoving scenarios, soil parameter calibration, randomized scale evaluation, sim-to-field gap reporting, jobsite productivity scoring, failure replay bundles, ML-ready datasets, a surrogate evaluator, simple blade-plan search, and a small C++ terrain kernel with a Python-vs-C++ benchmark.

It is not a production soil solver, and I call that out clearly in the project. The goal was to demonstrate the kind of simulation/evaluation infrastructure I understand autonomy teams need: realistic-enough physics, deterministic replay, performance metrics, calibration workflow, cycle-time and productivity evaluation, and tooling that supports ML autonomy validation.

The best entry point is here:
[repo link]/EARTHMOVING_SIMULATION_PACKET.md

I would be grateful for a chance to be reconsidered or pointed toward the strongest next step.

Best,
Lama
```

## Short Hiring Manager Message

```text
Hi [Name],

I applied for Bedrock's Simulation Engineer role and wanted to send a focused technical artifact rather than only re-forwarding my resume.

I built a MuJoCo-based autonomous earthmoving simulation track that is aimed at the problems your posting calls out: deformable terrain, soil calibration, sim-to-field gaps, batch evaluation, release gates, jobsite productivity scoring, ML-ready datasets, simple blade-plan search, and native terrain-kernel performance.

The most manager-friendly entry point is:
[repo link]/outputs/hiring_manager_packet/hiring_manager_packet.md

I am careful in the packet about what this is and is not: it is not a production soil solver, but it does show the validation workflow I would expect an autonomy simulation team to need: measurable physics approximations, deterministic replay, calibration targets, deployment-style metrics, and a path toward faster native kernels.

If this is close to the kind of simulation work your team needs, I would be grateful for the chance to talk.

Best,
Lama
```

## What To Emphasize In Conversation

- You built toward the exact feedback instead of arguing with it.
- You understand the difference between a toy demo and a production simulator.
- You can explain limitations honestly.
- You can work across Python tooling, C++ kernels, simulation content, deployment metrics, and generated artifacts.
- You are excited about construction autonomy specifically, not just robotics in the abstract.

## Timing

If reaching out before a suggested follow-up window has passed, frame it as a brief progress update rather than a formal re-application push.
