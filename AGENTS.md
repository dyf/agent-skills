# AGENTS.md

<!-- Generated from skills/*/SKILL.md by scripts/build_agents_md.py. Edit the skills, not this file. -->

Workspace-level guidance for all agents. These are standing rules — follow them without being asked.

## Workspace layout

Decide first where the work belongs:

- **Session folder only**: the default. For an immediate, short-lived task — a one-off analysis, a data pull, a migration, a quick investigation — and for early experiments that may later become a tool. Everything lives in the session folder: code, plan, experiment log, data.
- **Session folder plus tool repository**: for work on a tool or model of your own that has its own repo (e.g. morphogen). Each session of work on the tool still gets its own session folder. The tool's code, plan, and experiment log live in the tool repo, on a feature branch per `git-workflow`; the data the session reads and writes lives in the session folder.
- **Any other repository** (one you don't own, such as a shared library you contribute to, or a config repo like `agent-skills`): follow that repo's existing conventions. Don't add a `PLAN.md` or the folder layouts below, or restructure it to match the tool-repository rules. Keep your plan in a session folder for the task if one is needed.

### From session to tool

Tools grow out of session experiments. Work starts in a session folder, and the experiment log (`outputs/OUTPUTS.md` and each experiment's `outputs/<YYYYMMDD-slug>/`) stays there until the code becomes a tool.

Make that transition deliberately, when the code needs to be reused, installed, or maintained beyond the session:

1. Create the tool repository with its language's packaging conventions (below), a `README.md`, and a `PLAN.md`, and move the code into it.
2. Start the tool repo's `experiments/EXPERIMENTS.md` with a note at the top, above the entries, linking back to the session folder's `outputs/OUTPUTS.md`, which stays where it is as history.
3. From then on, sessions interact with the tool: new experiment records and `SUMMARY.md` go in the tool repo, and their data goes in the session folder under `outputs/<YYYYMMDD-slug>/`.

Until that transition happens, there is no tool repository, and nothing goes anywhere but the session folder.

### Session folders

1. Create a folder under the workspace root (the directory that holds your projects, e.g. `~/projects/`) named `YYYYMMDD-<slug>`, where `<slug>` is 2–4 words (kebab-case) describing the task. Example: `20260820-aind-schema-migration`.
2. Initialize it as a git repo with `tmp/`, `data/`, and `.venv/` gitignored, `outputs/` gitignored except for its index and summary files (`OUTPUTS.md` and each `SUMMARY.md`), plus a `README.md` (see `readme`) and a `PLAN.md`:
   ```
   git init
   mkdir tmp data outputs
   printf "tmp/\ndata/\n.venv/\noutputs/**\n!outputs/**/\n!outputs/OUTPUTS.md\n!outputs/*/SUMMARY.md\n" > .gitignore
   printf "# <slug>\n\n<what this task is for>\n" > README.md
   printf "# Plan\n\n<goal, approach, open questions, next steps>\n" > PLAN.md
   git add .gitignore README.md PLAN.md && git commit -m "chore: init session folder"
   ```
3. Create a virtual environment: `uv venv .venv`

### Tool repositories

A tool repository is meant to be installed, imported, and maintained, so it follows the standard packaging and style conventions for its language. Use the ecosystem's usual project file, source layout, test location, and formatter/linter rather than inventing a structure. For Python:

- `pyproject.toml` as the single project file, managed with `uv` (see `python-uv`); package code under `src/<package>/`, tests under `tests/`.
- PEP 8 style, enforced with `ruff check` and `ruff format`; type hints on public functions.
- Entry points declared in `pyproject.toml` (`[project.scripts]`), not ad-hoc scripts at the top level.

For other languages, follow the equivalent standard (e.g. `Cargo.toml` and `rustfmt`/`clippy` for Rust, `go.mod` and `gofmt` for Go, `package.json` with ESLint and Prettier for TypeScript).

### Folder layouts

These are the complete layouts. Beyond them, add only what the language or tooling expects (e.g. `uv.lock`, `docs/`, `.github/`).

Session folders never have an `experiments/` folder. All of a session's runs, experiments included, go in `outputs/`, one folder per run, indexed by `outputs/OUTPUTS.md`.

#### Session folder, on its own

```
20261106-<slug>/
  README.md            purpose and usage (see `readme`)
  PLAN.md              this session's plan
  .gitignore           tmp/, data/, .venv/, and outputs/ except OUTPUTS.md and SUMMARY.md files
  .venv/               uv environment (gitignored)
  *.py, *.ipynb        scripts and notebooks
  data/                input data (gitignored)
  outputs/
    OUTPUTS.md         index of the run folders, and the session's experiment log (tracked)
    20261106-<slug>/   one run: SUMMARY.md (tracked) plus its outputs and logs. A standard run,
                       staged and verified per `data-safety`, or an experiment
  tmp/                 transient files: downloads, intermediate outputs, debug dumps (gitignored)
```

#### Session folder working on a tool

The same, except that a tool experiment's record and `SUMMARY.md` live in the tool repo, and the session keeps only its data. Standard runs still have their `SUMMARY.md` here. `OUTPUTS.md` still indexes every run folder, and links each tool experiment to its record.

```
20261106-<slug>/
  README.md            purpose and usage, naming the tool and its version or commit
  PLAN.md              this session's task
  .gitignore           same as above
  .venv/               uv environment with the tool installed (gitignored)
  *.py, *.ipynb        scripts and notebooks that drive the tool
  data/                input data the tool reads (gitignored)
  outputs/
    OUTPUTS.md         index of the run folders (tracked)
    20261106-<slug>/   one run's outputs and logs: a standard run, with its SUMMARY.md (tracked),
                       or one tool experiment's data, named with the same slug as its record
                       in the tool repo (gitignored)
  tmp/                 transient files (gitignored)
```

#### Tool repository

Code, plan, and experiment records only. Data, run outputs, and scratch files are never part of a tool repository, including experiment data: the tool reads and writes them at locations outside the repo (a session folder, shared storage, a database), passed in by path or config.

```
<tool>/
  README.md            purpose and usage (see `readme`)
  PLAN.md              the tool's direction
  pyproject.toml       project file (or the language's equivalent)
  uv.lock              locked dependencies
  .gitignore           .venv/ and build artifacts
  .venv/               uv development environment (gitignored)
  src/<package>/       package code
  tests/               tests
  experiments/
    EXPERIMENTS.md     experiment log, starting with a link back to the session OUTPUTS.md it grew from
    20261106-<slug>/   one experiment's record: SUMMARY.md, configs, command, and a link to its data
                       in the session folder's outputs/20261106-<slug>/
```

### OUTPUTS.md

`OUTPUTS.md` is to the session's runs what `EXPERIMENTS.md` is to a tool's experiments. One entry per run folder, newest last, headed `## YYYYMMDD-<slug>` (the folder name), followed by a one-line title and a link to the folder. Write the entry when the run starts and complete it when the run ends.

- **Standard run**: purpose, setup (code version, inputs, command), and outcome (what it produced, whether it was verified and applied per `data-safety`).
- **Experiment in a session folder only**: the experiment entry format from `experiment-log` (question, setup, findings). This makes `OUTPUTS.md` the session's experiment log.
- **Experiment on a tool**: purpose and a link to its record in the tool repo's `EXPERIMENTS.md`; the findings live there.

### SUMMARY.md

Every run folder has a `SUMMARY.md`: each `outputs/<YYYYMMDD-slug>/` in a session folder, and each `experiments/<YYYYMMDD-slug>/` in a tool repo (for a tool experiment, the summary lives with the record, not with the data). It is the one file a reader opens to understand a run, while it runs and after. It contains:

- **Last updated**: ISO 8601 timestamp at the top, so a reader can tell how stale it is.
- **Index entry**: a link to the run's entry in its index file, using the heading anchor (`../OUTPUTS.md#20261106-lr-warmup` in a session folder, `../EXPERIMENTS.md#20261106-lr-warmup` in a tool repo).
- **Purpose**: what the run is for, and for an experiment, the question it answers.
- **Inputs, parameters, and code**: input data paths, parameters and config, the code version (commit hash, or tool name and version), and the exact command.
- **Time**: start time, end time (or "running"), and duration so far or in total.
- **Status**: what has completed, what is still running or queued (with progress, e.g. `step 4500/8000`), and anything that failed. When the run ends, mark it finished or failed.
- **Preliminary interpretation**: what the results so far suggest, and how confident that is.

`SUMMARY.md` is a running summary, not data: the no-overwrite rule in `data-safety` and the versioning in `data-contracts` don't apply. Overwrite it in place, as a current snapshot, not an append-only history. Update it at a cadence that matches how fast the run produces new information, every ~10 minutes by default, and once more when it ends.

### PLAN.md

Keep a `PLAN.md` at the root of every session folder and every tool repository of your own. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

- The file is the live plan: goal, approach, open questions, next steps.
- Update it whenever the plan changes, not after the fact.
- No changelog. History lives in git and the experiment log, not in the plan.

When a session works on a tool, the two plans have different scopes:

- The tool repo's `PLAN.md` is the tool's direction: goals, roadmap, open design questions. It outlives any one session.
- The session folder's `PLAN.md` is this session's task: what we are doing now, and how it moves the tool's plan forward.

## Git workflow

All work on remote repositories happens on feature branches, never directly on `main` or `master`.

- **Branch names**: follow conventional format — `<type>/<short-description>` (e.g. `feat/add-subject-validator`, `fix/missing-modality-field`, `chore/update-deps`)
- **Commit messages**: use [Conventional Commits](https://www.conventionalcommits.org/) — `<type>(<scope>): <description>` (e.g. `feat(schema): add optional funder field`)

Common types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `ci`

- **Commit often**: commit after every major step (e.g. a working script, a completed transformation, a plan change), in every repository you work in, including session folders. Don't let significant work accumulate uncommitted.
- **Keep published branches current**: once a feature branch is published (pushed to the remote), push each local commit to it as you make it, not in one batch at the end. The remote should never lag far behind local work, so progress is visible and nothing is lost if the local copy goes away.

## Data safety

Never overwrite data in place. Always write to a new file or location, verify the output, then replace or rename. If a transformation goes wrong, the original must still exist.

### Dry runs and test runs

Scripts that write to or modify a database must always support two safety modes:

- **Dry run** — log every intended write action without executing it. Dry run is the default; real writes require an explicit flag.
- **Test run** — process one record (or a small fixed number) instead of the full set, with real writes enabled. Good for verifying the logic end-to-end before committing to a full run.

Implement these as CLI flags (`--dry-run`, `--test-run`) or environment variables. Make it impossible to accidentally run the full destructive path without explicitly opting out of dry run.

When space permits, stage outputs (in a session folder, `outputs/<YYYYMMDD-slug>/`; for a tool, the output location it was given) and verify them before committing destructive changes.

## Data contracts

Data that code produces for later use — model weights and checkpoints, result tables, processed outputs — must carry a version. Logs are exempt.

### The version

- Define the version once in code, next to the code that writes the data (e.g. `RESULTS_SCHEMA_VERSION = 3`). One constant per kind of output.
- Write it into the data itself, not only the filename: a key in the checkpoint dict, a field in the file's metadata or header, a column in the table.
- The version describes the data contract, not the code. It changes only when the answer to "will this break or mislead downstream users?" is yes:
  - **Structure**: fields, columns, or tensors added, removed, renamed, retyped, or reshaped; file layout changes.
  - **Semantic comparability**: the same field now means something different, so values from the old and new versions can't be compared directly — new units, normalization, coordinate frame, metric definition, preprocessing, or a model architecture whose weights don't load the old way.
- Refactors, speedups, and bug fixes that leave the output structure and meaning unchanged do not change the version.
- Use a single integer that only goes up. If you need to say what changed, keep a short changelog comment beside the constant (one line per version).

### Responsibilities

- Every developer who changes what gets written maintains the version. Bump it in the same commit as the change; a change to output structure or meaning without a bump is a bug.
- Code that reads the data checks the version and fails with a clear error on a version it doesn't support (e.g. "checkpoint is v2, this code needs v3 — retrain"). Never silently load or compare data across versions.
- When results from different versions end up side by side (tables, plots, experiment logs), record the version so the mismatch is visible.

## Logging

- Write code so it always emits useful log messages that convey meaningful progress: what stage it is in and how far through it (`rows 12000/50000`, `file 3/8`), not just "working..." or nothing at all. Log at whatever cadence makes sense for the work, but prefer every 10–60 seconds — often enough to show the process is alive and moving, rarely enough that the log stays readable.
- Timestamp every log message (ISO 8601 wall-clock, not only elapsed seconds). Long runs are read back hours later; "step 4500, t=2415" says nothing about when it happened or whether the process is still alive.
- Prefer JSONL for logs that will be read by code: one JSON object per line, with `ts`, and the quantities as fields rather than formatted into a string. Keep human-readable progress lines separate if they are needed at all.
- Agents should timestamp their messages back to the user when reporting on running or completed work (e.g. "09:12 — training at step 4500/8000"), so the user can tell how stale a status is and how long things took.

## Long-running tasks

Anything that runs for more than a couple of minutes (training, sampling, bulk downloads, large scoring runs) is a long job, and both the job and the agent watching it have duties.

- **The job logs progress as `logging` requires** (cadence, timestamps, JSONL). For a long job, make the progress convertible into an ETA (`step 4500/8000`, `neurons 120/216`, bytes or rows done), and add the rate or the ETA itself when it is cheap to compute. A job that is silent for several minutes is indistinguishable from a hung one.
- **Run it in the background, logging to a file** in the run's session folder, under `outputs/<YYYYMMDD-slug>/`, for every kind of run: standard runs and experiments alike. Never run it in a foreground call that blocks the session or is killed by a timeout.
- **The agent monitors the log and reports without being asked.** Post a short progress summary every few minutes — one or two lines: the time, where the job is, the rate, the ETA, anything unusual (a loss that stopped falling, a stage that is slower than expected, a warning). Do this on a schedule, not only when the job finishes, so the user never has to ask for a status update. Use a monitor on the log file when one is available rather than polling by hand.
- **Keep the run's `SUMMARY.md` current** (see `workspace-layout`), every ~10 minutes by default and once more when the job ends.
- **If the log goes quiet**, say so and check whether the process is alive before assuming it is working.
- **When the job ends**, report the outcome in one message that stands on its own: whether it succeeded, how long it took, where the outputs are, the headline numbers, and what happens next. Chained stages (train → sample → score) are reported as they complete, not only at the end of the chain.
- **Set the next step up before waiting.** While a job runs, do the work that does not depend on its result (docs, tests, the analysis script that will read its output) so the result is used the moment it lands.

## Experiment log

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

### Log entries

In either file, each experiment has one entry, newest last, headed `## YYYYMMDD-<slug>` (the folder name, so headings and anchors are unique), followed by a one-line title and a link to the experiment's folder. Each experiment entry has:

- **Question / hypothesis**: what the experiment is meant to show.
- **Setup**: code version (commit hash), config and changed parameters, data, seed, command run.
- **Findings**: a short summary of the results and what they mean, including negative and inconclusive results, and what to try next.

Write the entry when the experiment starts and add the findings when it finishes, not after the fact.

### Experiment folders

One folder per experiment, named `YYYYMMDD-<slug>` (the date it started plus a 2–4 word kebab-case slug), matching its entry. The log summarizes; the folder holds the evidence.

- **Session folder only**: `outputs/<YYYYMMDD-slug>/` holds everything: `SUMMARY.md`, configs, the exact command or script, results tables, plots, logs, checkpoints. `OUTPUTS.md` and `SUMMARY.md` are tracked in git; the rest is gitignored with the rest of `outputs/`.
- **Session folder plus tool repository**: the tool repo's `experiments/<YYYYMMDD-slug>/` holds only the record: `SUMMARY.md`, configs, the exact command, and a link to the data. The data (results, logs, checkpoints, plots) goes in the session folder's `outputs/<YYYYMMDD-slug>/`, because data is not part of a tool repository.

### SUMMARY.md

Every experiment folder has a `SUMMARY.md`, as every run folder does. Its contents and update cadence are defined in `workspace-layout` ("SUMMARY.md"). For an experiment, when it finishes, also write the findings into its log entry.

### Upkeep

- Commit often, as `git-workflow` requires: the entry when the experiment starts, `SUMMARY.md` as it changes, the findings when it ends. Don't hold the experiment back for one commit at the end.
- Keep an experiment's data in its own `outputs/<YYYYMMDD-slug>/` and don't move it, so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the experiment log holds history. Don't duplicate one into the other.

## Writing style

Prose should be clear and precise. Avoid:

- Claudisms: "certainly", "absolutely", "great question", "I'd be happy to", "it's worth noting", "it's important to note", "dive into", "delve into"
- Dramatic flourishes: superlatives, breathless enthusiasm, unnecessary hedging
- Padding: restatements, throat-clearing, meta-commentary about what you're about to say

Unless the user asks for a particular tone, write plainly and directly.

## README

Every session folder and tool repository of your own has a `README.md` at its root. If one is missing, create it. Repositories you don't own keep their existing conventions (see `workspace-layout`).

It covers two things, at a high level:

- **Purpose**: what the repository is for and what problem it solves, in a few sentences.
- **Usage**: how to use it — how to set it up, the main commands or entry points to run, and what goes in and comes out.

Keep it short. It is an orientation, not full documentation: link to deeper docs, `PLAN.md`, or the experiment log rather than repeating them. Update it in the same commit as any change to what the repo does or how it is used. Prose follows the `writing-style` rules.

## Claude model defaults

When writing code that calls Claude, default to `claude-opus-5-5` — the current high-capability, non-frontier model (powerful but not the most expensive tier). If a cheaper model is needed for cost reasons, use `claude-sonnet-5-5`. Only use `claude-fable-5-1` if explicitly asked for maximum capability.

## Python uv

- **Always use `uv`** for Python dependency management and script execution.
  - Install deps: `uv add <pkg>` (not `pip install`)
  - Run scripts: `uv run python ...` or `uv run <script>`
  - Create envs: `uv venv`
  - Sync: `uv sync`
  - Never reach for `pip`, `pip install`, `python -m pip`, or `poetry` unless a project explicitly requires it.
