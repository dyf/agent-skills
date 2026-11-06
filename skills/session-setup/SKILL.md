---
name: session-setup
description: Sets up a dated working folder, git repo, venv, scratch layout, and PLAN.md at the start of a new work session. Use at the start of every new session or task, before writing any code, scripts, or data, and whenever deciding where a file should go (code vs data/ vs tmp/) or updating the session plan.
---

# Session setup

At the start of each new session:

1. Create a working folder under the workspace root (the directory that holds your projects, e.g. `~/projects/`) named `YYYYMMDD-<slug>`, where `<slug>` is 2–4 words (kebab-case) describing what the session is about. Example: `20260820-aind-schema-migration`.
2. Initialize it as a git repo with `tmp/` and `data/` gitignored and a `README.md` (see the `readme` skill) stating the session's purpose:
   ```
   git init
   mkdir tmp data
   printf "tmp/\ndata/\n" > .gitignore
   printf "# <slug>\n\n<what this session is for>\n" > README.md
   git add .gitignore README.md && git commit -m "chore: init session folder"
   ```
3. Create a virtual environment: `uv venv .venv`

## Scratch storage layout

| Path | Contents |
|------|----------|
| top level | code — scripts, notebooks, anything meant to be run or reviewed |
| `data/` | non-transient data (gitignored — survives the session but not tracked) |
| `outputs/<YYYYMMDD-slug>/` | outputs and logs of a standard (non-experiment) run, staged and verified per `data-safety` |
| `experiments/<YYYYMMDD-slug>/` | outputs, logs, and `STATUS.md` of one experiment (see `experiment-log`) |
| `tmp/` | transient files — downloads, intermediate outputs, debug dumps (gitignored) |

## PLAN.md

Keep a `PLAN.md` at the top level of the session working folder. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

- Update it whenever the plan changes, not after the fact.
- No changelog. History lives in git and the experiment log, not in the plan.
- The file is the live plan: goal, approach, open questions, next steps.
