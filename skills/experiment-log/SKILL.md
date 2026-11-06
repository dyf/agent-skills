---
name: experiment-log
description: Keep a datestamped experiment log when experimenting on a model or algorithm. Use whenever running, comparing, or tuning experiments (training runs, hyperparameter changes, ablations, algorithm variants) and when recording their results.
---

# Experiment log

When experimenting on a model or an algorithm, keep a datestamped experiment log: `EXPERIMENTS.md` at the top level of the session working folder, or of the project repo when the experiments live there.

- One entry per experiment, newest last, headed `## YYYY-MM-DD HH:MM — <short title>`.
- Each entry records what was tried and what happened:
  - **Question / hypothesis**: what the experiment is meant to show.
  - **Setup**: code version (commit hash), config and changed parameters, data, seed, command run.
  - **Results**: the numbers, with paths to logs, checkpoints, and plots. Include negative and inconclusive results.
  - **Takeaway**: what it means and what to try next.
- Write the entry when the experiment starts and fill in results when it finishes, not after the fact. Commit the log with the code that produced the results.
- `PLAN.md` holds current thinking; the experiment log holds history. Don't duplicate one into the other.
