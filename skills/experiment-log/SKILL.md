---
name: experiment-log
description: Keep the record of every run, a brief entry in the index log (OUTPUTS.md or EXPERIMENTS.md) plus one live SUMMARY.md, and for experiments on a model or algorithm, findings, proposed next experiments, and an adversarial critique. Use whenever starting, monitoring, or finishing a run, and whenever running, comparing, or tuning experiments (training runs, hyperparameter changes, ablations, algorithm variants).
---

# Experiment log

Every run, a standard run or an experiment, gets an entry in an index log and exactly one `SUMMARY.md`. Where the logs and run folders live is defined by the folder layouts in `workspace-layout`. An experiment is a run that tests a question about a model or algorithm; the parts marked *experiments* apply only to them.

## The logs: OUTPUTS.md and EXPERIMENTS.md

Each is a log: one brief entry per run folder, so a reader can scan what was done and what came of it without opening every folder.

- `OUTPUTS.md`, in a session folder's `outputs/`, logs every run in that session: standard runs and experiments. In a session folder only, it is also the session's experiment log.
- `EXPERIMENTS.md`, in a tool repo's `experiments/`, logs every experiment on the tool. After the session-to-tool transition, it starts with a note linking back to the session `OUTPUTS.md` it grew from.

Each entry, newest last:

- **Heading**: `## YYYYMMDD-<slug>`, the run folder's name, so headings and anchors are unique.
- **Title and link**: a one-line title and a link to the run's folder. For a tool experiment, the session's `OUTPUTS.md` entry links to the record in the tool repo, and the tool's `EXPERIMENTS.md` entry links to both the record and the data in the session folder.
- **Purpose**: a sentence or two on what the run is for; for an experiment, the question or hypothesis it tests.
- **Findings**: a sentence or two condensed from `SUMMARY.md`'s findings, labeled preliminary or final.
- **Next experiments** (*experiments*, once finished): one line each, condensed from `SUMMARY.md`.

Keep entries brief; everything else belongs in `SUMMARY.md`. Write the entry when the run starts, not after it worked out.

## SUMMARY.md

The one file a reader opens to understand a run, while it runs and after. For a standard run or a session-only experiment, it is in the run's `outputs/<YYYYMMDD-slug>/`; for a tool experiment, it is with the record in the tool repo's `experiments/<YYYYMMDD-slug>/`, not with the data. It contains:

- **Last updated**: ISO 8601 timestamp at the top, so a reader can tell how stale it is.
- **Index entry**: a link to the run's entry in its log, using the heading anchor (`../OUTPUTS.md#20261106-lr-warmup` in a session folder, `../EXPERIMENTS.md#20261106-lr-warmup` in a tool repo).
- **Purpose**: what the run is for; for an experiment, the question or hypothesis it tests.
- **Inputs, parameters, and code**: input data paths, parameters and config, the code version (commit hash, or tool name and version), and the exact command. For an experiment, enough to rerun it, including the full config and seed.
- **Time**: start time, end time (or "running"), and duration so far or in total.
- **Status**: what has completed, what is still running or queued (with progress, e.g. `step 4500/8000`), and anything that failed. When the run ends, mark it finished or failed.
- **Findings**: while the run is going, **Preliminary findings**: what the results so far suggest, the evidence, and how confident that is; label them preliminary, not conclusions. When it ends, **Final findings**: the conclusions it supports, the numbers behind them, and what it did not settle, including negative and inconclusive outcomes, not only wins.
- **Next experiments** (*experiments*, once finished): proposed follow-ups, each with the question it answers, why the findings call for it, and its rough cost. Final only after the critique.
- **Critique** (*experiments*, once finished): the reviewers' objections and how each was resolved (below).

Overwrite `SUMMARY.md` in place, as a current snapshot, not an append-only history. Update it at a cadence that matches how fast the run produces new information, every ~10 minutes by default, and once more when it ends. Bring the log entry's findings up to date at milestones, not on every refresh.

## Adversarial critique

After an experiment finishes and its final findings and next experiments are drafted, have them critiqued by adversarial reviewers before they are treated as settled:

1. **Launch reviewers.** Start at least one adversarial agent (a subagent or separate session with fresh context, not the agent that ran the experiment), and preferably two or three with different angles: one on the findings, one on the next experiments. Give them the `SUMMARY.md`, the log entry, and access to the outputs and code, and ask them to argue against the conclusions, not to confirm them.
2. **What they attack.** For the findings: whether the evidence supports the claim, confounds, leakage or train/eval contamination, too few seeds or samples, metric choice, cherry-picked examples, comparisons across data or schema versions, and alternative explanations. For the next experiments: whether each one would actually answer its question, whether a cheaper or more decisive experiment exists, what is missing (controls, baselines, ablations), and whether the list follows from the findings or just from momentum.
3. **Resolve each objection.** Check it against the data, running a quick analysis if needed. Then accept it and revise the findings or next experiments, or reject it with a stated reason. Don't drop objections silently.
4. **Record it.** Put the objections and their resolutions in `SUMMARY.md` under **Critique**, and update the log entry to the post-critique findings and next experiments.

## Upkeep

- The logs and `SUMMARY.md` are records, not data: the no-overwrite rule in `data-safety` and the versioning in `data-contracts` don't apply to them.
- Commit as `git-workflow` requires, at milestones: the log entry and `SUMMARY.md` when the run starts, `SUMMARY.md` and the preliminary findings when a stage finishes or something notable happens, the final findings (and next experiments) when it ends, and the critique once resolved. Refreshing `SUMMARY.md` every ~10 minutes does not mean committing every ~10 minutes.
- Keep a run's data in its own `outputs/<YYYYMMDD-slug>/` and don't move it, so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the logs hold history. Don't duplicate one into the other.
