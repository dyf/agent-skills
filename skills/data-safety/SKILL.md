---
name: data-safety
description: Rules for transforming data without losing originals, and the mandatory --dry-run / --test-run modes for scripts that write to databases. Use whenever writing a script or command that modifies, overwrites, migrates, or deletes files or database records.
---

# Data safety

Never overwrite data in place. Always write to a new file or location, verify the output, then replace or rename. If a transformation goes wrong, the original must still exist.

## Dry runs and test runs

Scripts that write to or modify a database must always support two safety modes:

- **Dry run** — log every intended write action without executing it. Dry run is the default; real writes require an explicit flag.
- **Test run** — process one record (or a small fixed number) instead of the full set, with real writes enabled. Good for verifying the logic end-to-end before committing to a full run.

Implement these as CLI flags (`--dry-run`, `--test-run`) or environment variables. Make it impossible to accidentally run the full destructive path without explicitly opting out of dry run.

When space permits, stage outputs (in a session folder, `outputs/<YYYYMMDD-slug>/`; for a tool, the output location it was given) and verify them before committing destructive changes.
