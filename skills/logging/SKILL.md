---
name: logging
description: Log format rules — ISO 8601 timestamps on every line, JSONL for machine-read logs, and timestamped status reports to the user. Use whenever adding logging or progress output to code, or reporting on running or completed work.
---

# Logging

- Timestamp every log message (ISO 8601 wall-clock, not only elapsed seconds). Long runs are read back hours later;
  "step 4500, t=2415" says nothing about when it happened or whether the process is still alive.
- Prefer JSONL for logs that will be read by code: one JSON object per line, with `ts`, and the quantities as fields
  rather than formatted into a string. Keep human-readable progress lines separate if they are needed at all.
- Agents should timestamp their messages back to the user when reporting on running or completed work (e.g.
  "09:12 — training at step 4500/8000"), so the user can tell how stale a status is and how long things took.
