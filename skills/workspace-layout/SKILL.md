---
name: workspace-layout
description: Where work lives — dated session folders by default, plus a tool repository once session experiments grow into a tool, and when to make that transition — plus the complete folder layout of each and PLAN.md. Use at the start of every new session or task, before writing any code, scripts, or data, and whenever deciding where a file should go or updating the session plan.
---

# Workspace layout

Decide first where the work belongs:

- **Session folder only**: the default. For an immediate, short-lived task — a one-off analysis, a data pull, a migration, a quick investigation — and for early experiments that may later become a tool. Everything lives in the session folder: code, plan, experiment log, data.
- **Session folder plus tool repository**: for work on a tool or model of your own that has its own repo (e.g. morphogen). Each session of work on the tool still gets its own session folder. The tool's code, plan, and experiment log live in the tool repo, on a feature branch per `git-workflow`; the data the session reads and writes lives in the session folder.
- **Any other repository** (one you don't own, such as a shared library you contribute to, or a config repo like `agent-skills`): follow that repo's existing conventions. Don't add a `PLAN.md` or the folder layouts below, or restructure it to match the tool-repository rules. Keep your plan in a session folder for the task if one is needed.

## From session to tool

Tools grow out of session experiments. Work starts in a session folder, and the experiment log (`outputs/OUTPUTS.md` and each experiment's `outputs/<YYYYMMDD-slug>/`) stays there until the code becomes a tool.

Make that transition deliberately, when the code needs to be reused, installed, or maintained beyond the session:

1. Create the tool repository with its language's packaging conventions (below), a `README.md`, and a `PLAN.md`, and move the code into it.
2. Start the tool repo's `experiments/EXPERIMENTS.md` with a note at the top, above the entries, linking back to the session folder's `outputs/OUTPUTS.md`, which stays where it is as history.
3. From then on, sessions interact with the tool: new experiment records and `SUMMARY.md` go in the tool repo, and their data goes in the session folder under `outputs/<YYYYMMDD-slug>/`.

Until that transition happens, there is no tool repository, and nothing goes anywhere but the session folder.

## Session folders

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
3. Create the Python project and environment, so `uv add` works (see `python-uv`): `uv init --bare && uv venv`. Commit `pyproject.toml`, and `uv.lock` once it exists.

## Tool repositories

A tool repository is meant to be installed, imported, and maintained, so it follows the standard packaging and style conventions for its language. Use the ecosystem's usual project file, source layout, test location, and formatter/linter rather than inventing a structure. For Python:

- `pyproject.toml` as the single project file, managed with `uv` (see `python-uv`); package code under `src/<package>/`, tests under `tests/`.
- PEP 8 style, enforced with `ruff check` and `ruff format`; type hints on public functions.
- Entry points declared in `pyproject.toml` (`[project.scripts]`), not ad-hoc scripts at the top level.

For other languages, follow the equivalent standard (e.g. `Cargo.toml` and `rustfmt`/`clippy` for Rust, `go.mod` and `gofmt` for Go, `package.json` with ESLint and Prettier for TypeScript).

## Folder layouts

These are the complete layouts. Beyond them, add only what the language or tooling expects (e.g. `uv.lock`, `docs/`, `.github/`).

Session folders never have an `experiments/` folder. All of a session's runs, experiments included, go in `outputs/`, one folder per run, indexed by `outputs/OUTPUTS.md`.

Every run folder, in `outputs/` or a tool repo's `experiments/`, is named `YYYYMMDD-<slug>`: the date the run started plus a 2–4 word kebab-case slug (e.g. `20261106-lr-warmup`). A tool experiment uses the same name for its record in the tool repo and its data in the session folder.

### Session folder, on its own

```
20261106-<slug>/
  README.md            purpose and usage (see `readme`)
  PLAN.md              this session's plan
  .gitignore           tmp/, data/, .venv/, and outputs/ except OUTPUTS.md and SUMMARY.md files
  pyproject.toml       dependencies (from `uv init --bare`)
  uv.lock              locked dependencies
  .venv/               uv environment (gitignored)
  *.py, *.ipynb        scripts and notebooks
  data/                input data (gitignored)
  outputs/
    OUTPUTS.md         index of the run folders, and the session's experiment log (tracked)
    20261106-<slug>/   one run: SUMMARY.md (tracked) plus its outputs and logs. A standard run,
                       staged and verified per `data-safety`, or an experiment
  tmp/                 transient files: downloads, intermediate outputs, debug dumps (gitignored)
```

### Session folder working on a tool

The same, except that a tool experiment's record and `SUMMARY.md` live in the tool repo, and the session keeps only its data. Standard runs still have their `SUMMARY.md` here. `OUTPUTS.md` still indexes every run folder, and links each tool experiment to its record.

```
20261106-<slug>/
  README.md            purpose and usage, naming the tool and its version or commit
  PLAN.md              this session's task
  .gitignore           same as above
  pyproject.toml       dependencies, including the tool
  uv.lock              locked dependencies
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

### Tool repository

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
    20261106-<slug>/   one experiment's record: SUMMARY.md and configs, with a link to its data
                       in the session folder's outputs/20261106-<slug>/
```

## EXPERIMENTS.md and OUTPUTS.md

Each is a log: one brief entry per run folder, so a reader can scan what was done and what came of it without opening every folder.

- `OUTPUTS.md`, in a session folder's `outputs/`, logs every run in that session: standard runs and experiments. In a session folder only, it is also the session's experiment log.
- `EXPERIMENTS.md`, in a tool repo's `experiments/`, logs every experiment on the tool. After the session-to-tool transition, it starts with a note linking back to the session `OUTPUTS.md` it grew from.

Each entry, newest last:

- **Heading**: `## YYYYMMDD-<slug>`, the run folder's name, so headings and anchors are unique.
- **Title and link**: a one-line title and a link to the run's folder. For a tool experiment, the session's `OUTPUTS.md` entry links to the record in the tool repo, and the tool's `EXPERIMENTS.md` entry links to both the record and the data in the session folder.
- **Purpose**: a sentence or two on what the run is for, or the question an experiment answers.
- **Results**: a brief summary of what came of it and what it means, including negative and inconclusive results, and for an experiment, what to try next. While the run is going, write "running" and see `SUMMARY.md`.

Keep entries brief. Inputs, parameters, code, timing, and status belong in the run's `SUMMARY.md`, not here. Write the entry when the run starts and fill in the results when it ends, not after the fact.

## SUMMARY.md

Every run has exactly one `SUMMARY.md`. For a standard run or a session-only experiment, it is in the run's `outputs/<YYYYMMDD-slug>/`. For a tool experiment, it is with the record in the tool repo's `experiments/<YYYYMMDD-slug>/`, not with the data. It is the one file a reader opens to understand a run, while it runs and after. It contains:

- **Last updated**: ISO 8601 timestamp at the top, so a reader can tell how stale it is.
- **Index entry**: a link to the run's entry in its index file, using the heading anchor (`../OUTPUTS.md#20261106-lr-warmup` in a session folder, `../EXPERIMENTS.md#20261106-lr-warmup` in a tool repo).
- **Purpose**: what the run is for, and for an experiment, the question it answers.
- **Inputs, parameters, and code**: input data paths, parameters and config, the code version (commit hash, or tool name and version), and the exact command.
- **Time**: start time, end time (or "running"), and duration so far or in total.
- **Status**: what has completed, what is still running or queued (with progress, e.g. `step 4500/8000`), and anything that failed. When the run ends, mark it finished or failed.
- **Preliminary interpretation**: what the results so far suggest, and how confident that is.

`SUMMARY.md`, `OUTPUTS.md`, and `EXPERIMENTS.md` are records, not data: the no-overwrite rule in `data-safety` and the versioning in `data-contracts` don't apply to them. Overwrite `SUMMARY.md` in place, as a current snapshot, not an append-only history. Update it at a cadence that matches how fast the run produces new information, every ~10 minutes by default, and once more when it ends. Commit it at milestones (start, stage done, end), not on every refresh.

## PLAN.md

Keep a `PLAN.md` at the root of every session folder and every tool repository of your own. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

- The file is the live plan: goal, approach, open questions, next steps.
- Update it whenever the plan changes, not after the fact.
- No changelog. History lives in git and the experiment log, not in the plan.

When a session works on a tool, the two plans have different scopes:

- The tool repo's `PLAN.md` is the tool's direction: goals, roadmap, open design questions. It outlives any one session.
- The session folder's `PLAN.md` is this session's task: what we are doing now, and how it moves the tool's plan forward.
