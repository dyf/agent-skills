---
name: logging
description: Logging rules — code always emits meaningful progress messages every 10–60 seconds, ISO 8601 timestamps on every line, JSONL for machine-read logs, and timestamped status reports to the user. Use whenever adding logging or progress output to code, or reporting on running or completed work.
---

# Logging

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
