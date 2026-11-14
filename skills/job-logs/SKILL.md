---
name: job-logs
description: Keep a record of every job (a training run, sampling or scoring run, ablation, data pull, migration, or anything else with its own run folder) as a brief log entry plus one live SUMMARY.md, with results and conclusions (preliminary while it runs, final when it ends), proposed next steps, and an adversarial critique once it finishes. Use whenever starting, monitoring, or finishing a job, and when comparing or tuning experiments.
---

# Job logs

A job is any piece of work with its own run folder, from a data migration to a training experiment. Every job gets the same record: an entry in a log and one `SUMMARY.md` in its run folder. The log is `outputs/OUTPUTS.md` in a session folder, or `experiments/EXPERIMENTS.md` in a tool repo; where each file lives is in `workspace-layout`.

## Log entries

The log is for scanning what was done and what came of it without opening every folder: one brief entry per job, newest last.

- **Heading**: `## YYYYMMDD-<slug>`, the run folder's name, so headings and anchors are unique.
- **Title and links**: a one-line title and a link to the job's `SUMMARY.md`. When a job's record and data are in different places (a tool repo and a session folder), link both, and the entries in both logs link to each other.
- **Question**: a sentence or two on what the job answers or produces: the hypothesis it tests, or the result it must deliver.
- **Results**: the headline numbers or outputs, condensed from `SUMMARY.md`.
- **Conclusions**: a sentence or two on what the results mean, labeled preliminary or final.
- **Next steps**: once finished, one line each, condensed from `SUMMARY.md`.

Keep entries brief; everything else belongs in `SUMMARY.md`. Write the entry when the job starts, not after it worked out.

## SUMMARY.md

The one file a reader opens to understand a job, while it runs and after. It contains:

- **Last updated**: ISO 8601 timestamp at the top, so a reader can tell how stale it is.
- **Log entry**: a link to the job's entry, using the heading anchor (e.g. `../OUTPUTS.md#20261106-lr-warmup` or `../EXPERIMENTS.md#20261106-lr-warmup`).
- **Question**: what the job answers or produces, as in the log entry.
- **Inputs, parameters, and code**: enough to rerun it: input data paths, full config, any random seeds, code version (commit hash, or tool name and version), and the exact command.
- **Time**: start time, end time (or "running"), and duration so far or in total.
- **Status**: what has completed, what is still running or queued (with progress, e.g. `step 4500/8000`), and anything that failed. When the job ends, mark it finished or failed.
- **Results**: what was measured or produced, without interpretation: metrics, counts, and plots, with where the outputs are. While the job runs, the results so far, marked as partial; when it ends, the final results, all of them, not only the favorable ones.
- **Conclusions**: what the results mean for the question, each tied to the results that support it, with how confident it is and what remains unsettled. Negative and inconclusive conclusions count, not only wins. While the job runs, **preliminary conclusions**, labeled as such; when it ends, **final conclusions**.
- **Next steps**: once finished, the follow-up experiments or jobs the conclusions call for, each with what it would answer, why the conclusions call for it, and its rough cost. Final only after the critique.
- **Critique**: once finished, the reviewers' objections and how each was resolved (below).

Overwrite `SUMMARY.md` in place, as a current snapshot, not an append-only history. Update it at a cadence that matches how fast the job produces new information, every ~10 minutes by default, and once more when it ends. Bring the log entry's results and conclusions up to date at milestones, not on every refresh.

## Adversarial critique

After a job finishes and its final conclusions and next steps are drafted, have them critiqued by adversarial reviewers before they are treated as settled:

1. **Launch reviewers.** Start at least one adversarial agent (a subagent or separate session with fresh context, not the agent that ran the job). Use two or three with different angles, one on the conclusions and one on the next steps, when the conclusions will steer further work. Give them the `SUMMARY.md`, the log entry, and access to the outputs and code, and ask them to argue against the conclusions, not to confirm them.
2. **What they attack.** For the conclusions: whether the results support them, whether the results themselves are sound, confounds, leakage or train/eval contamination, too few seeds or samples, metric choice, cherry-picked examples, unverified outputs, comparisons across data or schema versions, and alternative explanations. For the next steps: whether each would actually answer its question, whether a cheaper or more decisive option exists, what is missing (controls, baselines, ablations), and whether the list follows from the conclusions or just from momentum.
3. **Resolve each objection.** Check it against the data, running a quick analysis if needed. Then accept it and revise the conclusions or next steps, or reject it with a stated reason. Don't drop objections silently.
4. **Record it.** Put the objections and their resolutions in `SUMMARY.md` under **Critique**, and update the log entry to the post-critique conclusions and next steps.

## Upkeep

- The logs and `SUMMARY.md` are records, not data: the no-overwrite rule in `data-safety` and the versioning in `data-contracts` don't apply to them.
- Commit as `git-workflow` requires, at milestones: the log entry and `SUMMARY.md` when the job starts, `SUMMARY.md` and the preliminary results and conclusions when a stage finishes or something notable happens, the final results, conclusions, and next steps when it ends, and the critique once resolved. Refreshing `SUMMARY.md` every ~10 minutes does not mean committing every ~10 minutes.
- Keep a job's data in its own `outputs/<YYYYMMDD-slug>/` and don't move it, so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the logs hold history. Don't duplicate one into the other: next steps the plan adopts move into `PLAN.md`, and the log keeps them as proposed.
