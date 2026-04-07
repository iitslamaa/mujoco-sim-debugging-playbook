# Interview Guide

Use this repo to steer the conversation toward the exact skills required for technical solutions engineering in robotics simulation.

## Story to tell

This project was intentionally built as a support-first simulation repo. The goal was not just to run a MuJoCo robot, but to recreate the daily work of helping users diagnose unstable behavior, understand parameter sensitivity, and self-serve through documentation.

## Points to emphasize

- The repo includes reproducible experiment configs instead of ad hoc notebooks.
- It includes support-style issue cases with suggested investigation and response structure.
- It includes Docker, bash-friendly scripts, Make targets, and CI to show comfort with Linux developer workflows.
- It includes user-facing docs and issue templates, not only simulator code.
- The work is framed around reproducing failures and reducing support load.

## Honest framing

You should not claim this is Isaac Lab experience if it is not. The stronger framing is:

> I built a MuJoCo-based simulation support lab to mirror the kind of user enablement and debugging work I would expect in Isaac Lab. The tooling is different, but the operating model is the same: reproduce issues, isolate variables, explain behavior clearly, and improve documentation so users can unblock themselves faster.

