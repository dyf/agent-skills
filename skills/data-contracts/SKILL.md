---
name: data-contracts
description: Versioning rules for data that code produces — model weights and checkpoints, result tables, processed outputs (not logs). Use whenever writing code that saves such data, changing its structure or meaning, or writing code that reads it back.
---

# Data contracts

Data that code produces for later use — model weights and checkpoints, result tables, processed outputs — must carry a version. Logs are exempt.

## The version

- Define the version once in code, next to the code that writes the data (e.g. `RESULTS_SCHEMA_VERSION = 3`). One constant per kind of output.
- Write it into the data itself, not only the filename: a key in the checkpoint dict, a field in the file's metadata or header, a column in the table.
- The version describes the data contract, not the code. It changes only when the answer to "will this break or mislead downstream users?" is yes:
  - **Structure**: fields, columns, or tensors added, removed, renamed, retyped, or reshaped; file layout changes.
  - **Semantic comparability**: the same field now means something different, so values from the old and new versions can't be compared directly — new units, normalization, coordinate frame, metric definition, preprocessing, or a model architecture whose weights don't load the old way.
- Refactors, speedups, and bug fixes that leave the output structure and meaning unchanged do not change the version.
- Use a single integer that only goes up. If you need to say what changed, keep a short changelog comment beside the constant (one line per version).

## Responsibilities

- Every developer who changes what gets written maintains the version. Bump it in the same commit as the change; a change to output structure or meaning without a bump is a bug.
- Code that reads the data checks the version and fails with a clear error on a version it doesn't support (e.g. "checkpoint is v2, this code needs v3 — retrain"). Never silently load or compare data across versions.
- When results from different versions end up side by side (tables, plots, experiment logs), record the version so the mismatch is visible.
