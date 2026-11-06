---
name: experiment-log
description: Keep a datestamped experiment log, with one folder per experiment for its results, when experimenting on a model or algorithm. Use whenever running, comparing, or tuning experiments (training runs, hyperparameter changes, ablations, algorithm variants) and when recording their results.
---

# Experiment log

When experimenting on a model or an algorithm, keep all experiments under one top-level `experiments/` folder in the repo (or session working folder):

```
experiments/
  EXPERIMENTS.md
  20261106-lr-warmup/
  20261107-wider-decoder/
```

## EXPERIMENTS.md

The index of every experiment, one entry each, newest last, headed `## YYYY-MM-DD — <short title>`, with a link to the experiment's folder. Each entry has:

- **Question / hypothesis**: what the experiment is meant to show.
- **Setup**: code version (commit hash), config and changed parameters, data, seed, command run.
- **Findings**: a short summary of the results and what they mean, including negative and inconclusive results, and what to try next.

Write the entry when the experiment starts and add the findings when it finishes, not after the fact.

## Experiment folders

One subfolder per experiment, named `YYYYMMDD-<slug>` to match its entry. It holds everything the experiment produced: results tables, plots, logs, configs, and the exact command or script that ran it. `EXPERIMENTS.md` summarizes; the folder holds the evidence.

- Commit the entry, the folder, and the code that produced the results together.
- Large files (checkpoints, big arrays) can be gitignored, but keep them in the folder so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the experiment log holds history. Don't duplicate one into the other.
