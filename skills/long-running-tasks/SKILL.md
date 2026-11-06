---
name: long-running-tasks
description: Duties for jobs that run more than a couple of minutes (training, sampling, bulk downloads, large scoring runs) — background execution, per-minute progress logs, proactive status reports, and end-of-job summaries. Use whenever launching, monitoring, or reporting on a long job.
---

# Long-running tasks

Anything that runs for more than a couple of minutes (training, sampling, bulk downloads, large scores) is a long
job, and both the job and the agent watching it have duties. Log lines follow the `logging` skill.

- **The job logs progress every 10–60 seconds.** Each line is timestamped and says where the job is
  in units the reader can convert into an ETA: `step 4500/8000`, `neurons 120/216`, bytes or rows done. Add the
  rate or the ETA itself when it is cheap to compute. A job that is silent for several minutes is indistinguishable
  from a hung one.
- **Run it in the background, logging to a file** in the run's `outputs/<YYYYMMDD-slug>/` folder, or in the experiment folder
  (`experiments/<YYYYMMDD-slug>/`) when the job is part of an experiment (timestamped lines, JSONL if
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
