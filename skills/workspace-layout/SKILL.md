---
name: workspace-layout
description: Where work lives — dated session folders by default, plus a tool repository once session experiments grow into a tool, and when to make that transition — plus the shared folder layout (data/, outputs/, experiments/, tmp/) and PLAN.md. Use at the start of every new session or task, before writing any code, scripts, or data, and whenever deciding where a file should go or updating the session plan.
---

# Workspace layout

Decide first where the work belongs:

- **Session folder only**: the default. For an immediate, short-lived task — a one-off analysis, a data pull, a migration, a quick investigation — and for early experiments that may later become a tool. Everything lives in the session folder: code, plan, experiments, data.
- **Session folder plus tool repository**: for work on a tool or model of your own that has its own repo (e.g. morphogen). Each session of work on the tool still gets its own session folder. The tool's code, plan, and experiment log live in the tool repo, on a feature branch per `git-workflow`; the data the session reads and writes lives in the session folder.
- **Any other repository** (one you don't own, such as a shared library you contribute to, or a config repo like `agent-skills`): follow that repo's existing conventions. Don't add a `PLAN.md`, the folder layout below, or restructure it to match the tool-repository rules. Keep your plan in a session folder for the task if one is needed.

## From session to tool

Tools grow out of session experiments. Work starts in a session folder, and the experiment structure (`experiments/`, `EXPERIMENTS.md`, `STATUS.md`, data) stays there until the code becomes a tool.

Make that transition deliberately, when the code needs to be reused, installed, or maintained beyond the session:

1. Create the tool repository with its language's packaging conventions (below), a `README.md`, and a `PLAN.md`, and move the code into it.
2. Start the tool repo's `experiments/EXPERIMENTS.md` with a note at the top, above the entries, linking back to the session folder's experiment log, which stays where it is as history.
3. From then on, sessions interact with the tool: new experiment records and `STATUS.md` go in the tool repo, and their data goes in the session folder under `outputs/<YYYYMMDD-slug>/`.

Until that transition happens, there is no tool repository, and nothing goes anywhere but the session folder.

## Session folders

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

## Tool repositories

A tool repository is meant to be installed, imported, and maintained, so in addition to the folder layout below it follows the standard packaging and style conventions for its language. Use the ecosystem's usual project file, source layout, test location, and formatter/linter rather than inventing a structure. For Python:

- `pyproject.toml` as the single project file, managed with `uv` (see `python-uv`); package code under `src/<package>/`, tests under `tests/`.
- PEP 8 style, enforced with `ruff check` and `ruff format`; type hints on public functions.
- Entry points declared in `pyproject.toml` (`[project.scripts]`), not ad-hoc scripts at the top level.

For other languages, follow the equivalent standard (e.g. `Cargo.toml` and `rustfmt`/`clippy` for Rust, `go.mod` and `gofmt` for Go, `package.json` with ESLint and Prettier for TypeScript).

## Folder layout

Session folders and tool repositories use the same layout at their root, except that tool repositories have no `data/`, `outputs/`, or `tmp/`:

| Path | Contents |
|------|----------|
| top level | code. In session folders: scripts and notebooks. In tool repositories: the language's standard layout (above) |
| `PLAN.md` | the live plan (see below) |
| `data/` | non-transient input data (gitignored). Session folders only |
| `outputs/<YYYYMMDD-slug>/` | outputs and logs of one run: a standard run, staged and verified per `data-safety`, or an experiment on a tool, whose record lives in the tool repo (gitignored). Session folders only |
| `experiments/<YYYYMMDD-slug>/` | one experiment's record and `STATUS.md`, per `experiment-log`. In session folders it also holds the experiment's data (tracked; large files gitignored) |
| `tmp/` | transient files — downloads, intermediate outputs, debug dumps (gitignored). Session folders only |

Data, run outputs, and scratch files are not part of a tool repository, including experiment data. A tool reads its input from, and writes its outputs to, locations outside the repo (a session folder's `data/`, `outputs/`, and `tmp/`, shared storage, a database), passed in by path or config, never paths inside the repo.

## PLAN.md

Keep a `PLAN.md` at the root of every session folder and every tool repository of your own. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

When a session works on a tool, the two plans have different scopes:

- The tool repo's `PLAN.md` is the tool's direction: goals, roadmap, open design questions. It outlives any one session.
- The session folder's `PLAN.md` is this session's task: what we are doing now, and how it moves the tool's plan forward.

- Update it whenever the plan changes, not after the fact.
- No changelog. History lives in git and the experiment log, not in the plan.
- The file is the live plan: goal, approach, open questions, next steps.
