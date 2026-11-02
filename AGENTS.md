# AGENTS.md

<!-- Generated from skills/*/SKILL.md by scripts/build_agents_md.py. Edit the skills, not this file. -->

Workspace-level guidance for all agents. These are standing rules — follow them without being asked.

## Session setup

At the start of each new session:

1. Create a working folder under the workspace root (the directory that holds your projects, e.g. `~/projects/`) named `YYYYMMDD-<slug>`, where `<slug>` is 2–4 words (kebab-case) describing what the session is about. Example: `20260820-aind-schema-migration`.
2. Initialize it as a git repo with `tmp/` and `data/` gitignored:
   ```
   git init
   mkdir tmp data
   printf "tmp/\ndata/\n" > .gitignore
   git add .gitignore && git commit -m "init"
   ```
3. Create a virtual environment: `uv venv .venv`

### Scratch storage layout

| Path | Contents |
|------|----------|
| top level | code — scripts, notebooks, anything meant to be run or reviewed |
| `data/` | non-transient data (gitignored — survives the session but not tracked) |
| `tmp/` | transient files — downloads, intermediate outputs, debug dumps (gitignored) |

### PLAN.md

Keep a `PLAN.md` at the top level of the session working folder. It should always reflect the current thinking — not history, not what we tried, but what we are doing and why.

- Update it whenever the plan changes, not after the fact.
- Keep a pithy changelog at the top (one line per change, newest first) so it's easy to see how thinking evolved.
- The rest of the file is the live plan: goal, approach, open questions, next steps.

## Git workflow

All work on remote repositories happens on feature branches, never directly on `main` or `master`.

- **Branch names**: follow conventional format — `<type>/<short-description>` (e.g. `feat/add-subject-validator`, `fix/missing-modality-field`, `chore/update-deps`)
- **Commit messages**: use [Conventional Commits](https://www.conventionalcommits.org/) — `<type>(<scope>): <description>` (e.g. `feat(schema): add optional funder field`)

Common types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `ci`

- **Commit often**: commit after every major step (e.g. a working script, a completed transformation, a plan change), in both remote repositories and session working folders. Don't let significant work accumulate uncommitted.
- **Keep the remote branch current**: push feature-branch commits to the remote as you make them, not in one batch at the end. The remote should never lag far behind local work, so progress is visible and nothing is lost if the local copy goes away.

## Data safety

Never overwrite data in place. Always write to a new file or location, verify the output, then replace or rename. If a transformation goes wrong, the original must still exist.

### Dry runs and test runs

Scripts that write to or modify a database must always support two safety modes:

- **Dry run** — log every intended write action without executing it. Default to dry run on unless explicitly disabled.
- **Test run** — process one record (or a small fixed number) instead of the full set, with real writes enabled. Good for verifying the logic end-to-end before committing to a full run.

Implement these as CLI flags (`--dry-run`, `--test-run`) or environment variables. Make it impossible to accidentally run the full destructive path without explicitly opting out of dry run.

When space permits, stage outputs to a `./results/` folder and verify them before committing destructive changes.

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

Anything that runs for more than a couple of minutes (training, sampling, bulk downloads, large scores) is a long
job, and both the job and the agent watching it have duties. Log lines follow the `logging` skill.

- **The job logs progress every 10–60 seconds.** Each line is timestamped and says where the job is
  in units the reader can convert into an ETA: `step 4500/8000`, `neurons 120/216`, bytes or rows done. Add the
  rate or the ETA itself when it is cheap to compute. A job that is silent for several minutes is indistinguishable
  from a hung one.
- **Run it in the background, logging to a file** under the run directory or `tmp/` (timestamped lines, JSONL if
  code will read it), never in a foreground call that blocks the session or is killed by a timeout.
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

## Writing documents

Prose should be clear and precise. Avoid:

- Claudisms: "certainly", "absolutely", "great question", "I'd be happy to", "it's worth noting", "it's important to note", "dive into", "delve into"
- Dramatic flourishes: superlatives, breathless enthusiasm, unnecessary hedging
- Padding: restatements, throat-clearing, meta-commentary about what you're about to say

Unless the user asks for a particular tone, write plainly and directly.

## Claude model defaults

When writing code that calls Claude, default to `claude-opus-5-5` — the current high-capability, non-frontier model (powerful but not the most expensive tier). If a cheaper model is needed for cost reasons, use `claude-sonnet-5-5`. Only use `claude-fable-5-1` if explicitly asked for maximum capability.

## Package management

- **Always use `uv`** for Python dependency management and script execution.
  - Install deps: `uv add <pkg>` (not `pip install`)
  - Run scripts: `uv run python ...` or `uv run <script>`
  - Create envs: `uv venv`
  - Sync: `uv sync`
  - Never reach for `pip`, `pip install`, `python -m pip`, or `poetry` unless a project explicitly requires it.
