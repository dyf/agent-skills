---
name: python-uv
description: Use uv for all Python dependency management, environments, and script execution — never pip or poetry. Use whenever installing Python packages, creating a virtual environment, or running a Python script.
---

# Python uv

- **Always use `uv`** for Python dependency management and script execution.
  - Install deps: `uv add <pkg>` (not `pip install`)
  - Run scripts: `uv run python ...` or `uv run <script>`
  - Create envs: `uv venv`
  - Sync: `uv sync`
  - Never reach for `pip`, `pip install`, `python -m pip`, or `poetry` unless a project explicitly requires it.
