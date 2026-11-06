# AGENTS.md

<!-- Generated from skills/*/SKILL.md by scripts/build_agents_md.py. Edit the skills, not this file. -->

Workspace-level guidance for all agents. These are standing rules — follow them without being asked.

## Session setup

Decide first where the work belongs:

- **Session folder only**: the default. For an immediate, short-lived task — a one-off analysis, a data pull, a migration, a quick investigation — and for early experiments that may later become a tool. Everything lives in the session folder: code, plan, experiments, data.
- **Session folder plus tool repository**: once a tool or model of your own has its own repo (e.g. morphogen), a session works with it. The tool's code, plan, and experiment log live in the tool repo, on a feature branch per `git-workflow`. The data it reads and writes lives in the session folder.
- **Any other repository** (one you don't own, such as a shared library you contribute to, or a config repo like `agent-skills`): follow that repo's existing conventions. Don't add a `PLAN.md`, the folder layout below, or restructure it to match the tool-repository rules. Keep your plan in a session folder for the task if one is needed.

### From session to tool

Tools grow out of session experiments. Work starts in a session folder, and the experiment structure (`experiments/`, `EXPERIMENTS.md`, `STATUS.md`, data) stays there until the code becomes a tool.

Make that transition deliberately, when the code needs to be reused, installed, or maintained beyond the session:

1. Create the tool repository with its language's packaging conventions (below), a `README.md`, and a `PLAN.md`, and move the code into it.
2. Start the tool repo's `experiments/EXPERIMENTS.md`. Its first entry links back to the session folder's experiment log, which stays where it is as history.
3. From then on, sessions interact with the tool: new experiment records and `STATUS.md` go in the tool repo, and their data goes in the session folder under `outputs/<YYYYMMDD-slug>/`.

Until that transition happens, there is no tool repository, and nothing goes anywhere but the session folder.

### Session folders

1. Create a folder under the workspace root (the directory that holds your projects, e.g. `~/projects/`) named `YYYYMMDD-<slug>`, where `<slug>` is 2–4 words (kebab-case) describing the task. Example: `20260820-aind-schema-migration`.
2. Initialize it as a git repo with `tmp/`, `data/`, and `outputs/` gitignored, plus a `README.md` (see `readme`) and a `PLAN.md`:
   ```
   git init
   mkdir tmp data outputs
   printf "tmp/\ndata/\noutputs/\n" > .gitignore
   printf "# <slug>\n\n<what this task is for>\n" > README.md
   printf "# Plan\n\n<goal, approach, open questions, next steps>\n" > PLAN.md
   git add .gitignore README.md PLAN.md && git commit -m "chore: init session folder"
   ```
3. Create a virtual environment: `uv venv .venv`

### Tool repositories

A tool repository is meant to be installed, imported, and maintained, so in addition to the folder layout below it follows the standard packaging and style conventions for its language. Use the ecosystem's usual project file, source layout, test location, and formatter/linter rather than inventing a structure. For Python:

- `pyproject.toml` as the single project file, managed with `uv` (see `python-uv`); package code under `src/<package>/`, tests under `tests/`.
- PEP 8 style, enforced with `ruff check` and `ruff format`; type hints on public functions.
- Entry points declared in `pyproject.toml` (`[project.scripts]`), not ad-hoc scripts at the top level.

For other languages, follow the equivalent standard (e.g. `Cargo.toml` and `rustfmt`/`clippy` for Rust, `go.mod` and `gofmt` for Go, `package.json` with ESLint and Prettier for TypeScript).

### Folder layout

Session folders and tool repositories use the same layout at their root, except that tool repositories have no `data/` or `outputs/`:

| Path | Contents |
|------|----------|
| top level | code. In session folders: scripts and notebooks. In tool repositories: the language's standard layout (above) |
| `PLAN.md` | the live plan (see below) |
| `data/` | non-transient input data (gitignored). Session folders only |
| `outputs/<YYYYMMDD-slug>/` | outputs and logs of a standard (non-experiment) run, staged and verified per `data-safety` (gitignored). Session folders only |
| `experiments/<YYYYMMDD-slug>/` | one experiment's record and `STATUS.md`, per `experiment-log`. In session folders it also holds the experiment's data (tracked; large files gitignored) |
| `tmp/` | transient files — downloads, intermediate outputs, debug dumps (gitignored) |

Data and run outputs are not part of a tool repository, including experiment data. A tool reads its input from, and writes its outputs to, locations outside the repo (a session folder's `data/` and `outputs/`, shared storage, a database), passed in by path or config, never paths inside the repo.

### PLAN.md

Keep a `PLAN.md` at the root of every session folder and every tool repository of your own. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

- Update it whenever the plan changes, not after the fact.
- No changelog. History lives in git and the experiment log, not in the plan.
- The file is the live plan: goal, approach, open questions, next steps.

## Git workflow

All work on remote repositories happens on feature branches, never directly on `main` or `master`.

- **Branch names**: follow conventional format — `<type>/<short-description>` (e.g. `feat/add-subject-validator`, `fix/missing-modality-field`, `chore/update-deps`)
- **Commit messages**: use [Conventional Commits](https://www.conventionalcommits.org/) — `<type>(<scope>): <description>` (e.g. `feat(schema): add optional funder field`)

Common types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `ci`

- **Commit often**: commit after every major step (e.g. a working script, a completed transformation, a plan change), in both remote repositories and session folders. Don't let significant work accumulate uncommitted.
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

- Write code so it always emits useful log messages that convey meaningful progress: what stage it is in and how
  far through it (`rows 12000/50000`, `file 3/8`), not just "working..." or nothing at all. Log at whatever cadence
  makes sense for the work, but prefer every 10–60 seconds — often enough to show the process is alive and moving,
  rarely enough that the log stays readable.
- Timestamp every log message (ISO 8601 wall-clock, not only elapsed seconds). Long runs are read back hours later;
  "step 4500, t=2415" says nothing about when it happened or whether the process is still alive.
- Prefer JSONL for logs that will be read by code: one JSON object per line, with `ts`, and the quantities as fields
  rather than formatted into a string. Keep human-readable progress lines separate if they are needed at all.
- Agents should timestamp their messages back to the user when reporting on running or completed work (e.g.
  "09:12 — training at step 4500/8000"), so the user can tell how stale a status is and how long things took.

## Long-running tasks

Anything that runs for more than a couple of minutes (training, sampling, bulk downloads, large scoring runs) is a
long job, and both the job and the agent watching it have duties.

- **The job logs progress as `logging` requires** (cadence, timestamps, JSONL). For a long job, make the progress
  convertible into an ETA (`step 4500/8000`, `neurons 120/216`, bytes or rows done), and add the rate or the ETA
  itself when it is cheap to compute. A job that is silent for several minutes is indistinguishable from a hung one.
- **Run it in the background, logging to a file** next to the run's outputs: in a session folder's
  `outputs/<YYYYMMDD-slug>/`, or its `experiments/<YYYYMMDD-slug>/` for an experiment run from a session folder. A
  tool-repository experiment logs with its data in the session folder, not in the tool repo. Never run it in a foreground call that blocks the session or is killed by a timeout.
- **The agent monitors the log and reports without being asked.** Post a short progress summary every few minutes —
  one or two lines: the time, where the job is, the rate, the ETA, anything unusual (a loss that stopped falling, a
  stage that is slower than expected, a warning). Do this on a schedule, not only when the job finishes, so the user
  never has to ask for a status update. Use a monitor on the log file when one is available rather than polling by
  hand.
- **If the log goes quiet**, say so and check whether the process is alive before assuming it is working.
- **When the job ends**, report the outcome in one message that stands on its own: whether it succeeded, how long it
  took, where the outputs are, the headline numbers, and what happens next. Chained stages (train → sample → score)
  are reported as they complete, not only at the end of the chain.
- **Set the next step up before waiting.** While a job runs, do the work that does not depend on its result (docs,
  tests, the analysis script that will read its output) so the result is used the moment it lands.

## Experiment log

When experimenting on a model or an algorithm, keep all experiments under one top-level `experiments/` folder at the root of the session folder or tool repository:

```
experiments/
  EXPERIMENTS.md
  20261106-lr-warmup/
    STATUS.md
  20261107-wider-decoder/
```

### EXPERIMENTS.md

The index of every experiment, one entry each, newest last, headed `## YYYYMMDD-<slug>` (the folder name, so headings and anchors are unique), followed by a one-line title and a link to the experiment's folder. Each entry has:

- **Question / hypothesis**: what the experiment is meant to show.
- **Setup**: code version (commit hash), config and changed parameters, data, seed, command run.
- **Findings**: a short summary of the results and what they mean, including negative and inconclusive results, and what to try next.

Write the entry when the experiment starts and add the findings when it finishes, not after the fact.

### Experiment folders

One subfolder per experiment, named `YYYYMMDD-<slug>` (the date it started plus a 2–4 word kebab-case slug), matching its entry. `EXPERIMENTS.md` summarizes; the folder holds the evidence. What goes in it depends on whether the work has become a tool yet (see "From session to tool" in `session-setup`):

- **Session folder only**: everything the experiment produced — results tables, plots, logs, checkpoints, configs, and the exact command or script that ran it.
- **Session folder plus tool repository**: the tool repo's folder holds only the record — `STATUS.md`, configs, the exact command, and a link to where the data is. The experiment's input and output data (results, logs, checkpoints, plots) live in a session folder, under `outputs/<YYYYMMDD-slug>/` with the same slug, because data is not part of a tool repository.

### STATUS.md

Each experiment folder has one `STATUS.md` that says where the experiment stands while it runs:

- **Last updated**: ISO 8601 timestamp at the top, so a reader can tell how stale it is.
- **Log entry**: a link to this experiment's entry in `EXPERIMENTS.md`, using the heading anchor (e.g. `../EXPERIMENTS.md#20261106-lr-warmup`).
- **Done**: which runs, seeds, or stages have completed.
- **Not done**: what is still running or queued, with progress where known (e.g. `step 4500/8000`), and anything that failed.
- **Preliminary interpretation**: what the results so far suggest, and how confident that is.

`STATUS.md` is a status report, not data: the no-overwrite rule in `data-safety` and the versioning in `data-contracts` don't apply. Overwrite it in place, as a current snapshot, not an append-only history. Update it at a cadence that matches how fast the experiment produces new information, every ~10 minutes by default. When the experiment finishes, mark it finished in `STATUS.md` and write the findings into `EXPERIMENTS.md`.

### Upkeep

- Commit often, as `git-workflow` requires: the entry when the experiment starts, results and `STATUS.md` as they land, the findings when it ends. Don't hold the experiment back for one commit at the end.
- In a session folder, large files (checkpoints, big arrays) can be gitignored, but keep them in the experiment folder so the paths in the log stay valid.
- `PLAN.md` holds current thinking; the experiment log holds history. Don't duplicate one into the other.

## Writing style

Prose should be clear and precise. Avoid:

- Claudisms: "certainly", "absolutely", "great question", "I'd be happy to", "it's worth noting", "it's important to note", "dive into", "delve into"
- Dramatic flourishes: superlatives, breathless enthusiasm, unnecessary hedging
- Padding: restatements, throat-clearing, meta-commentary about what you're about to say

Unless the user asks for a particular tone, write plainly and directly.

## README

Every repository has a `README.md` at its root. If one is missing, create it.

It covers two things, at a high level:

- **Purpose**: what the repository is for and what problem it solves, in a few sentences.
- **Usage**: how to use it — how to set it up, the main commands or entry points to run, and what goes in and comes out.

Keep it short. It is an orientation, not full documentation: link to deeper docs, `PLAN.md`, or `experiments/EXPERIMENTS.md` rather than repeating them. Update it in the same commit as any change to what the repo does or how it is used. Prose follows the `writing-style` rules.

## Claude model defaults

When writing code that calls Claude, default to `claude-opus-5-5` — the current high-capability, non-frontier model (powerful but not the most expensive tier). If a cheaper model is needed for cost reasons, use `claude-sonnet-5-5`. Only use `claude-fable-5-1` if explicitly asked for maximum capability.

## Python uv

- **Always use `uv`** for Python dependency management and script execution.
  - Install deps: `uv add <pkg>` (not `pip install`)
  - Run scripts: `uv run python ...` or `uv run <script>`
  - Create envs: `uv venv`
  - Sync: `uv sync`
  - Never reach for `pip`, `pip install`, `python -m pip`, or `poetry` unless a project explicitly requires it.
