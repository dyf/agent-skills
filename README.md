# agent-skills

Standing rules for coding agents, packaged as [Agent Skills](https://agentskills.io): one folder per rule set, each with a `SKILL.md` whose frontmatter tells the agent when to load it.

| Skill | Covers |
|-------|--------|
| [session-setup](skills/session-setup/SKILL.md) | dated working folder, git init, venv, `data/` vs `tmp/`, `PLAN.md` |
| [git-workflow](skills/git-workflow/SKILL.md) | feature branches, branch names, Conventional Commits, commit and push cadence |
| [data-safety](skills/data-safety/SKILL.md) | no in-place overwrites, `--dry-run` / `--test-run` for database writes |
| [data-contracts](skills/data-contracts/SKILL.md) | version every produced dataset, checkpoint, and result table; bump on breaking structure or meaning changes |
| [logging](skills/logging/SKILL.md) | ISO 8601 timestamps, JSONL logs, timestamped status reports |
| [long-running-tasks](skills/long-running-tasks/SKILL.md) | background jobs, per-minute progress, proactive monitoring and reporting |
| [experiment-log](skills/experiment-log/SKILL.md) | datestamped `EXPERIMENTS.md` log of model and algorithm experiments and results |
| [writing-style](skills/writing-style/SKILL.md) | plain prose, no Claudisms or padding |
| [python-uv](skills/python-uv/SKILL.md) | `uv` for all Python dependency and script work |
| [claude-model-defaults](skills/claude-model-defaults/SKILL.md) | default model IDs for code that calls Claude |

[AGENTS.md](AGENTS.md) contains the same rules in one file, for harnesses that read `AGENTS.md` but do not load skills.

## Install

**Claude Code** — as a plugin:

```
/plugin marketplace add dyf/agent-skills
/plugin install agent-skills@dyf
```

or as personal skills: `ln -s "$PWD"/skills/* ~/.claude/skills/`

**Other harnesses that support Agent Skills** — symlink or copy the folders in `skills/` into the harness's skills directory (check its docs for the path).

**Harnesses that read AGENTS.md** (Codex, Cursor, Gemini CLI, GitHub Copilot, and others) — copy or symlink `AGENTS.md` into the workspace root or the harness's global instructions location.

## Editing

The skills are the source of truth. After changing one, regenerate `AGENTS.md`:

```
uv run scripts/build_agents_md.py
```

CI fails if `AGENTS.md` is out of date.

## Layout

```
skills/<name>/SKILL.md        one skill per rule set (frontmatter: name, description)
AGENTS.md                     generated: all skills flattened into one file
CLAUDE.md                     points Claude Code at AGENTS.md
.claude-plugin/               Claude Code plugin + marketplace manifests
scripts/build_agents_md.py    regenerates AGENTS.md
```

## License

[MIT](LICENSE)
