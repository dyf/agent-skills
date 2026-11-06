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

## Folder layout

Session folders and tool repositories use the same layout at their root:

| Path | Contents |
|------|----------|
| top level | code — scripts, notebooks, anything meant to be run or reviewed |
| `data/` | non-transient input data (gitignored) |
| `outputs/<YYYYMMDD-slug>/` | outputs and logs of a standard (non-experiment) run, staged and verified per `data-safety` (gitignored) |
| `experiments/<YYYYMMDD-slug>/` | outputs, logs, and `STATUS.md` of one experiment, per `experiment-log` (tracked; large files gitignored) |
| `tmp/` | transient files — downloads, intermediate outputs, debug dumps (gitignored) |

## PLAN.md

Keep a `PLAN.md` at the top level of the session folder. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

- Update it whenever the plan changes, not after the fact.
- No changelog. History lives in git and the experiment log, not in the plan.
- The file is the live plan: goal, approach, open questions, next steps.
