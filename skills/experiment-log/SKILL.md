---
name: experiment-log
description: Keep a datestamped experiment log, with one folder per experiment for its status and results, when experimenting on a model or algorithm. Use whenever running, comparing, or tuning experiments (training runs, hyperparameter changes, ablations, algorithm variants) and when recording their results.
---

# Experiment log

When experimenting on a model or an algorithm, keep a datestamped experiment log: an index file plus one folder per experiment. Where it lives depends on whether the work has become a tool yet (see "From session to tool" in `workspace-layout`):

- **Session folder only**: the log is the session's `outputs/OUTPUTS.md` (see `workspace-layout`), which indexes every run in `outputs/`, experiments included. Session folders have no `experiments/` folder.
  ```
  outputs/
    OUTPUTS.md
    20261106-lr-warmup/
      SUMMARY.md
  ```
- **Session folder plus tool repository**: the log is the tool repo's `experiments/EXPERIMENTS.md`, with the records in `experiments/<slug>/`. The data stays in the session folder's `outputs/<slug>/`, under the same slug, and the session's `OUTPUTS.md` entry for the run links to the record in the tool repo.
  ```
  <tool>/experiments/            <session>/outputs/
    EXPERIMENTS.md                 OUTPUTS.md
    20261106-lr-warmup/            20261106-lr-warmup/
      SUMMARY.md                      results, logs, checkpoints
  ```

## Log entries

In either file, each experiment has one entry, newest last, headed `## YYYYMMDD-<slug>` (the folder name, so headings and anchors are unique), followed by a one-line title and a link to the experiment's folder. Each experiment entry has:

- **Question / hypothesis**: what the experiment is meant to show.
- **Setup**: code version (commit hash), config and changed parameters, data, seed, command run.
- **Findings**: a short summary of the results and what they mean, including negative and inconclusive results, and what to try next.

Write the entry when the experiment starts and add the findings when it finishes, not after the fact.

## Experiment folders

One folder per experiment, named `YYYYMMDD-<slug>` (the date it started plus a 2–4 word kebab-case slug), matching its entry. The log summarizes; the folder holds the evidence.

- **Session folder only**: `outputs/<YYYYMMDD-slug>/` holds everything: `SUMMARY.md`, configs, the exact command or script, results tables, plots, logs, checkpoints. `OUTPUTS.md` and `SUMMARY.md` are tracked in git; the rest is gitignored with the rest of `outputs/`.
- **Session folder plus tool repository**: the tool repo's `experiments/<YYYYMMDD-slug>/` holds only the record: `SUMMARY.md`, configs, the exact command, and a link to the data. The data (results, logs, checkpoints, plots) goes in the session folder's `outputs/<YYYYMMDD-slug>/`, because data is not part of a tool repository.

## SUMMARY.md

Each experiment folder has one `SUMMARY.md` that says where the experiment stands while it runs:

- **Last updated**: ISO 8601 timestamp at the top, so a reader can tell how stale it is.
- **Log entry**: a link to this experiment's entry in the log, using the heading anchor (`../OUTPUTS.md#20261106-lr-warmup` in a session folder, `../EXPERIMENTS.md#20261106-lr-warmup` in a tool repo).
- **Done**: which runs, seeds, or stages have completed.
- **Not done**: what is still running or queued, with progress where known (e.g. `step 4500/8000`), and anything that failed.
- **Preliminary interpretation**: what the results so far suggest, and how confident that is.

`SUMMARY.md` is a running summary, not data: the no-overwrite rule in `data-safety` and the versioning in `data-contracts` don't apply. Overwrite it in place, as a current snapshot, not an append-only history. Update it at a cadence that matches how fast the experiment produces new information, every ~10 minutes by default. When the experiment finishes, mark it finished in `SUMMARY.md` and write the findings into the log entry.

## Upkeep

- Commit often, as `git-workflow` requires: the entry when the experiment starts, `SUMMARY.md` as it changes, the findings when it ends. Don't hold the experiment back for one commit at the end.
- Keep an experiment's data in its own `outputs/<YYYYMMDD-slug>/` and don't move it, so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the experiment log holds history. Don't duplicate one into the other.
