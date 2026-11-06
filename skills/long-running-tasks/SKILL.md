---
name: long-running-tasks
description: Duties for jobs that run more than a couple of minutes (training, sampling, bulk downloads, large scoring runs) — background execution, progress logs, proactive status reports, and end-of-job summaries. Use whenever launching, monitoring, or reporting on a long job.
---

# Long-running tasks

Anything that runs for more than a couple of minutes (training, sampling, bulk downloads, large scoring runs) is a long job, and both the job and the agent watching it have duties.

- **The job logs progress as `logging` requires** (cadence, timestamps, JSONL). For a long job, make the progress convertible into an ETA (`step 4500/8000`, `neurons 120/216`, bytes or rows done), and add the rate or the ETA itself when it is cheap to compute. A job that is silent for several minutes is indistinguishable from a hung one.
- **Run it in the background, logging to a file** next to the run's data in the session folder: `outputs/<YYYYMMDD-slug>/` for a standard run or an experiment on a tool, `experiments/<YYYYMMDD-slug>/` for an experiment in a session folder only. Never run it in a foreground call that blocks the session or is killed by a timeout.
- **The agent monitors the log and reports without being asked.** Post a short progress summary every few minutes — one or two lines: the time, where the job is, the rate, the ETA, anything unusual (a loss that stopped falling, a stage that is slower than expected, a warning). Do this on a schedule, not only when the job finishes, so the user never has to ask for a status update. Use a monitor on the log file when one is available rather than polling by hand.
- **If the log goes quiet**, say so and check whether the process is alive before assuming it is working.
- **When the job ends**, report the outcome in one message that stands on its own: whether it succeeded, how long it took, where the outputs are, the headline numbers, and what happens next. Chained stages (train → sample → score) are reported as they complete, not only at the end of the chain.
- **Set the next step up before waiting.** While a job runs, do the work that does not depend on its result (docs, tests, the analysis script that will read its output) so the result is used the moment it lands.
