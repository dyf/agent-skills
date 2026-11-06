---
name: experiment-log
description: Keep a datestamped experiment log, with one folder per experiment for its status and results, when experimenting on a model or algorithm. Use whenever running, comparing, or tuning experiments (training runs, hyperparameter changes, ablations, algorithm variants) and when recording their results.
---

# Experiment log

When experimenting on a model or an algorithm, keep all experiments under one top-level `experiments/` folder at the root of the session folder or tool repository:

```
experiments/
  EXPERIMENTS.md
  20261106-lr-warmup/
    STATUS.md
  20261107-wider-decoder/
```

## EXPERIMENTS.md

The index of every experiment, one entry each, newest last, headed `## YYYYMMDD-<slug>` (the folder name, so headings and anchors are unique), followed by a one-line title and a link to the experiment's folder. Each entry has:

- **Question / hypothesis**: what the experiment is meant to show.
- **Setup**: code version (commit hash), config and changed parameters, data, seed, command run.
- **Findings**: a short summary of the results and what they mean, including negative and inconclusive results, and what to try next.

Write the entry when the experiment starts and add the findings when it finishes, not after the fact.

## Experiment folders

One subfolder per experiment, named `YYYYMMDD-<slug>` (the date it started plus a 2–4 word kebab-case slug), matching its entry. `EXPERIMENTS.md` summarizes; the folder holds the evidence. What goes in it depends on whether the work has become a tool yet (see "From session to tool" in `session-setup`):

- **Session folder only**: everything the experiment produced — results tables, plots, logs, checkpoints, configs, and the exact command or script that ran it.
- **Session folder plus tool repository**: the tool repo's folder holds only the record — `STATUS.md`, configs, the exact command, and a link to where the data is. The experiment's input and output data (results, logs, checkpoints, plots) live in a session folder, under `outputs/<YYYYMMDD-slug>/` with the same slug, because data is not part of a tool repository.

## STATUS.md

Each experiment folder has one `STATUS.md` that says where the experiment stands while it runs:

- **Last updated**: ISO 8601 timestamp at the top, so a reader can tell how stale it is.
- **Log entry**: a link to this experiment's entry in `EXPERIMENTS.md`, using the heading anchor (e.g. `../EXPERIMENTS.md#20261106-lr-warmup`).
- **Done**: which runs, seeds, or stages have completed.
- **Not done**: what is still running or queued, with progress where known (e.g. `step 4500/8000`), and anything that failed.
- **Preliminary interpretation**: what the results so far suggest, and how confident that is.

`STATUS.md` is a status report, not data: the no-overwrite rule in `data-safety` and the versioning in `data-contracts` don't apply. Overwrite it in place, as a current snapshot, not an append-only history. Update it at a cadence that matches how fast the experiment produces new information, every ~10 minutes by default. When the experiment finishes, mark it finished in `STATUS.md` and write the findings into `EXPERIMENTS.md`.

## Upkeep

- Commit often, as `git-workflow` requires: the entry when the experiment starts, results and `STATUS.md` as they land, the findings when it ends. Don't hold the experiment back for one commit at the end.
- In a session folder, large files (checkpoints, big arrays) can be gitignored, but keep them in the experiment folder so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the experiment log holds history. Don't duplicate one into the other.
