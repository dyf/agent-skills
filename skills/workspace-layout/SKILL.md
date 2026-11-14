---
name: workspace-layout
description: Where work lives — dated session folders by default, plus a tool repository once session experiments grow into a tool, and when to make that transition — plus the complete folder layout of each and PLAN.md. Use at the start of every new session or task, before writing any code, scripts, or data, and whenever deciding where a file should go or updating the session plan.
---

# Workspace layout

Decide first where the work belongs:

- **Session folder only**: the default. For an immediate, short-lived task — a one-off analysis, a data pull, a migration, a quick investigation — and for early experiments that may later become a tool. Everything lives in the session folder: code, plan, job log, data.
- **Session folder plus tool repository**: for work on a tool or model of your own that has its own repo (e.g. morphogen). Each session of work on the tool still gets its own session folder. The tool's code, plan, and job log (`EXPERIMENTS.md`) live in the tool repo, on a feature branch per `git-workflow`; the data the session reads and writes lives in the session folder.
- **Any other repository** (one you don't own, such as a shared library you contribute to, or a config repo like `agent-skills`): follow that repo's existing conventions. Don't add a `PLAN.md` or the folder layouts below, or restructure it to match the tool-repository rules. Keep your plan in a session folder for the task if one is needed.

## From session to tool

Tools grow out of session experiments. Work starts in a session folder, and the job log (`outputs/OUTPUTS.md` and each job's `outputs/<YYYYMMDD-slug>/`) stays there until the code becomes a tool.

Make that transition deliberately, when the code needs to be reused, installed, or maintained beyond the session:

1. Create the tool repository with its language's packaging conventions (below), a `README.md`, and a `PLAN.md`, and move the code into it.
2. Start the tool repo's `experiments/EXPERIMENTS.md` with a note at the top, above the entries, linking back to the session folder's `outputs/OUTPUTS.md`, which stays where it is as history.
3. From then on, sessions interact with the tool: each tool job's record (`SUMMARY.md` and configs) goes in the tool repo, and its data goes in the session folder under `outputs/<YYYYMMDD-slug>/`.

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

Session folders never have an `experiments/` folder. Every job a session runs gets a run folder in `outputs/`, indexed by `outputs/OUTPUTS.md`. A **tool job** is one whose findings are about the tool (training, evaluation, ablations of it); its record lives in the tool repo instead, and only its data stays in the session folder.

Every run folder, in `outputs/` or a tool repo's `experiments/`, is named `YYYYMMDD-<slug>`: the date the job started plus a 2–4 word kebab-case slug (e.g. `20261106-lr-warmup`). A tool job uses the same name for its record in the tool repo and its data in the session folder. What goes in `OUTPUTS.md`, `EXPERIMENTS.md`, and each `SUMMARY.md` is defined in `job-logs`.

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
    OUTPUTS.md         the session's job log, indexing the run folders (tracked)
    20261106-<slug>/   one job: SUMMARY.md (tracked) plus its outputs and logs, staged and
                       verified per `data-safety`
  tmp/                 transient files: downloads, intermediate outputs, debug dumps (gitignored)
```

### Session folder working on a tool

The same, except that a tool job's record and `SUMMARY.md` live in the tool repo, and the session keeps only its data. Other jobs still have their `SUMMARY.md` here. `OUTPUTS.md` still indexes every run folder, and links each tool job to its record.

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
    OUTPUTS.md         the session's job log, indexing the run folders (tracked)
    20261106-<slug>/   one job's outputs and logs, with its SUMMARY.md (tracked), or a tool
                       job's data, named with the same slug as its record in the tool repo
                       (gitignored)
  tmp/                 transient files (gitignored)
```

### Tool repository

Code, plan, and job records only. Data, job outputs, and scratch files are never part of a tool repository, including the data of tool jobs: the tool reads and writes them at locations outside the repo (a session folder, shared storage, a database), passed in by path or config.

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
    EXPERIMENTS.md     the tool's job log, starting with a link back to the session OUTPUTS.md it grew from
    20261106-<slug>/   one tool job's record: SUMMARY.md and configs, with a link to its data
                       in the session folder's outputs/20261106-<slug>/
```

## PLAN.md

Keep a `PLAN.md` at the root of every session folder and every tool repository of your own. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

- The file is the live plan: goal, approach, open questions, next steps.
- Update it whenever the plan changes, not after the fact.
- No changelog. History lives in git and the job logs, not in the plan.

When a session works on a tool, the two plans have different scopes:

- The tool repo's `PLAN.md` is the tool's direction: goals, roadmap, open design questions. It outlives any one session.
- The session folder's `PLAN.md` is this session's task: what we are doing now, and how it moves the tool's plan forward.
