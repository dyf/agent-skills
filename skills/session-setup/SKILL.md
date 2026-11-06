---
name: session-setup
description: Where work lives — dated session folders for immediate, short-lived tasks, and the tool repository itself for long-lived tools and models — plus the shared folder layout (data/, outputs/, experiments/, tmp/) and PLAN.md. Use at the start of every new session or task, before writing any code, scripts, or data, and whenever deciding where a file should go or updating the session plan.
---

# Session setup

Decide first where the work belongs:

- **Session folder**: for an immediate, short-lived task — a one-off analysis, a data pull, a migration, a quick investigation. Create a new one as described below.
- **Tool repository**: for work on a long-lived tool or model that has its own repo (e.g. morphogen). Work in that repo, on a feature branch per `git-workflow`. Don't create a session folder for it.

## Session folders

1. Create a working folder under the workspace root (the directory that holds your projects, e.g. `~/projects/`) named `YYYYMMDD-<slug>`, where `<slug>` is 2–4 words (kebab-case) describing the task. Example: `20260820-aind-schema-migration`.
2. Initialize it as a git repo with `tmp/`, `data/`, and `outputs/` gitignored and a `README.md` (see `readme`) stating the task:
   ```
   git init
   mkdir tmp data outputs
   printf "tmp/\ndata/\noutputs/\n" > .gitignore
   printf "# <slug>\n\n<what this task is for>\n" > README.md
   git add .gitignore README.md && git commit -m "chore: init session folder"
   ```
3. Create a virtual environment: `uv venv .venv`

## Tool repositories

A tool repository is meant to be installed, imported, and maintained, so in addition to the folder layout below it follows the standard packaging and style conventions for its language. Use the ecosystem's usual project file, source layout, test location, and formatter/linter rather than inventing a structure. For Python:

- `pyproject.toml` as the single project file, managed with `uv` (see `python-uv`); package code under `src/<package>/`, tests under `tests/`.
- PEP 8 style, enforced with `ruff check` and `ruff format`; type hints on public functions.
- Entry points declared in `pyproject.toml` (`[project.scripts]`), not ad-hoc scripts at the top level.

For other languages, follow the equivalent standard (e.g. `Cargo.toml` and `rustfmt`/`clippy` for Rust, `go.mod` and `gofmt` for Go, `package.json` with ESLint and Prettier for TypeScript).

## Folder layout

Session folders and tool repositories use the same layout at their root, except that tool repositories have no `data/` or `outputs/`:

| Path | Contents |
|------|----------|
| top level | code — scripts, notebooks, anything meant to be run or reviewed |
| `PLAN.md` | the live plan (see below) |
| `data/` | non-transient input data (gitignored). Session folders only |
| `outputs/<YYYYMMDD-slug>/` | outputs and logs of a standard (non-experiment) run, staged and verified per `data-safety` (gitignored). Session folders only |
| `experiments/<YYYYMMDD-slug>/` | outputs, logs, and `STATUS.md` of one experiment, per `experiment-log` (tracked; large files gitignored) |
| `tmp/` | transient files — downloads, intermediate outputs, debug dumps (gitignored) |

Data and run outputs are not part of a tool repository. A tool reads its input from, and writes its outputs to, locations outside the repo (a session folder's `data/` and `outputs/`, shared storage, a database), passed in by path or config, never paths inside the repo.

## PLAN.md

Keep a `PLAN.md` at the root of every session folder and tool repository. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

- Update it whenever the plan changes, not after the fact.
- No changelog. History lives in git and the experiment log, not in the plan.
- The file is the live plan: goal, approach, open questions, next steps.
