---
name: experiment-log
description: Keep a datestamped experiment log, with one folder per experiment for its summary and results, when experimenting on a model or algorithm. Use whenever running, comparing, or tuning experiments (training runs, hyperparameter changes, ablations, algorithm variants) and when recording their results.
---

# Experiment log

When experimenting on a model or an algorithm, record every experiment: an entry in the log and a run folder with a `SUMMARY.md`. Where these live, and what each file contains, is defined in `workspace-layout`:

- **Session folder only**: the log is `outputs/OUTPUTS.md`, and each experiment is a run folder in `outputs/`.
- **Session folder plus tool repository**: the log is the tool repo's `experiments/EXPERIMENTS.md`, each experiment's record (`SUMMARY.md` and configs) is in `experiments/<YYYYMMDD-slug>/`, and its data is in the session folder's `outputs/<YYYYMMDD-slug>/`.

## What experiments add

On top of the general rules for log entries and `SUMMARY.md`:

- **Purpose** states the question or hypothesis the experiment tests.
- **Results** include negative and inconclusive outcomes, not only wins, and say what to try next.
- **Inputs, parameters, and code** in `SUMMARY.md` are specific enough to rerun the experiment: commit hash, full config, seed, and exact command.
- Write the log entry when the experiment starts, not after it worked out.

## Upkeep

- Commit as `git-workflow` requires, at milestones: the log entry and `SUMMARY.md` when the experiment starts, `SUMMARY.md` when a stage finishes or something notable happens, and the results when it ends. Refreshing `SUMMARY.md` every ~10 minutes does not mean committing every ~10 minutes.
- Keep an experiment's data in its own `outputs/<YYYYMMDD-slug>/` and don't move it, so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the experiment log holds history. Don't duplicate one into the other.
