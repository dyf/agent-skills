---
name: experiment-log
description: Keep a datestamped experiment log, with one folder per experiment for its summary and results, when experimenting on a model or algorithm. Use whenever running, comparing, or tuning experiments (training runs, hyperparameter changes, ablations, algorithm variants) and when recording their results: preliminary findings while running, final findings and proposed next experiments when finished, critiqued by adversarial reviewers.
---

# Experiment log

When experimenting on a model or an algorithm, record every experiment: an entry in the log and a run folder with a `SUMMARY.md`. Where these live, and what each file contains, is defined in `workspace-layout`:

- **Session folder only**: the log is `outputs/OUTPUTS.md`, and each experiment is a run folder in `outputs/`.
- **Session folder plus tool repository**: the log is the tool repo's `experiments/EXPERIMENTS.md`, each experiment's record (`SUMMARY.md` and configs) is in `experiments/<YYYYMMDD-slug>/`, and its data is in the session folder's `outputs/<YYYYMMDD-slug>/`.

## What experiments add

On top of the general rules for log entries and `SUMMARY.md`:

- **Purpose** states the question or hypothesis the experiment tests.
- **Inputs, parameters, and code** in `SUMMARY.md` are specific enough to rerun the experiment: commit hash, full config, seed, and exact command.
- Write the log entry when the experiment starts, not after it worked out.
- **While it runs**, the log entry and `SUMMARY.md` carry **Preliminary findings**: what the results so far suggest about the hypothesis and how confident that is. Keep them current as stages finish and as new results arrive, so a reader can see where the experiment is heading before it ends. Label them preliminary; don't state them as conclusions.
- **When it ends**, replace them with **Final findings**: the answer to the question, including negative and inconclusive outcomes, not only wins, and the evidence for it. Then propose **Next experiments**: the follow-ups the findings call for, each with the question it answers and why.

## Adversarial critique

After an experiment finishes and its final findings and next experiments are drafted, have them critiqued by adversarial reviewers before they are treated as settled:

1. **Launch reviewers.** Start at least one adversarial agent (a subagent or separate session with fresh context, not the agent that ran the experiment), and preferably two or three with different angles: one on the findings, one on the next experiments. Give them the `SUMMARY.md`, the log entry, and access to the outputs and code, and ask them to argue against the conclusions, not to confirm them.
2. **What they attack.** For the findings: whether the evidence supports the claim, confounds, leakage or train/eval contamination, too few seeds or samples, metric choice, cherry-picked examples, comparisons across data or schema versions, and alternative explanations. For the next experiments: whether each one would actually answer its question, whether a cheaper or more decisive experiment exists, what is missing (controls, baselines, ablations), and whether the list follows from the findings or just from momentum.
3. **Resolve each objection.** Check it against the data, running a quick analysis if needed. Then accept it and revise the findings or next experiments, or reject it with a stated reason. Don't drop objections silently.
4. **Record it.** Put the objections and their resolutions in `SUMMARY.md` under **Critique**, and note in the log entry any finding or next experiment the critique changed. The log's final findings and next experiments are the post-critique versions.

## Upkeep

- Commit as `git-workflow` requires, at milestones: the log entry and `SUMMARY.md` when the experiment starts, `SUMMARY.md` and the preliminary findings when a stage finishes or something notable happens, the final findings and next experiments when it ends, and the critique once resolved. Refreshing `SUMMARY.md` every ~10 minutes does not mean committing every ~10 minutes.
- Keep an experiment's data in its own `outputs/<YYYYMMDD-slug>/` and don't move it, so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the experiment log holds history. Don't duplicate one into the other.
