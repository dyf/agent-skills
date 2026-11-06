"""Build AGENTS.md from skills/*/SKILL.md.

The skills are the source of truth. AGENTS.md is the same rules flattened into one
file for harnesses that read AGENTS.md but do not load skills.

    uv run scripts/build_agents_md.py          # write AGENTS.md
    uv run scripts/build_agents_md.py --check  # exit 1 if AGENTS.md is stale
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "AGENTS.md"

# Section order in AGENTS.md. Skills not listed here are appended alphabetically.
ORDER = [
    "session-setup",
    "git-workflow",
    "data-safety",
    "data-contracts",
    "logging",
    "long-running-tasks",
    "experiment-log",
    "writing-style",
    "readme",
    "claude-model-defaults",
    "python-uv",
]

HEADER = """\
# AGENTS.md

<!-- Generated from skills/*/SKILL.md by scripts/build_agents_md.py. Edit the skills, not this file. -->

Workspace-level guidance for all agents. These are standing rules — follow them without being asked.
"""


def body(skill_md: Path) -> str:
    text = skill_md.read_text()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S).strip()
    # Demote headings one level so each skill becomes a section, skipping fenced code.
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        out.append("#" + line if not fenced and line.startswith("#") else line)
    return "\n".join(out)


def build() -> str:
    names = sorted(p.parent.name for p in ROOT.glob("skills/*/SKILL.md"))
    ordered = [n for n in ORDER if n in names] + [n for n in names if n not in ORDER]
    sections = [body(ROOT / "skills" / n / "SKILL.md") for n in ordered]
    return HEADER + "\n" + "\n\n".join(sections) + "\n"


def main() -> int:
    content = build()
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text() != content:
            print("AGENTS.md is out of date; run: uv run scripts/build_agents_md.py", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(content)
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
