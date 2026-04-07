# PyTorch Learning Guide

This repository includes a PyTorch imitation-learning baseline to show that the project is not only about hand-written control and debugging. It also covers model training, checkpointing, evaluation, and artifact packaging.

## Workflow

1. Collect expert demonstrations from the analytical MuJoCo controller.
2. Build a state-action dataset from observed joint state, target coordinates, inverse-kinematics targets, and joint error.
3. Train a multilayer PyTorch policy network to predict torques.
4. Evaluate the learned policy back in MuJoCo.
5. Save checkpoints, learning curves, evaluation summaries, and a rollout GIF.

## Commands

```bash
python scripts/train_torch_policy.py --dataset-episodes 24 --epochs 60
python scripts/evaluate_torch_policy.py --episodes 8
```

## Why this matters

This matters for roles that care about robot learning because it shows:

- comfort with PyTorch models and training loops
- reproducible experiment packaging around learned policies
- ability to evaluate a model in the same simulation stack used for debugging
- ability to compare expert-vs-learned behavior, not just run one or the other

## Current learned policy setup

- architecture: multilayer perceptron with LayerNorm and ReLU blocks
- training objective: torque imitation with MSE loss
- optimizer: AdamW
- scheduler: cosine annealing
- inputs: observed qpos, qvel, target XY, desired joint angles, and joint error

