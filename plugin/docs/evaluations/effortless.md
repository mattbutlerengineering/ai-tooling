# Evaluation: effortless

**Repo:** [HeyCubit/effortless](https://github.com/HeyCubit/effortless)
**Stars:** 93 | **Last updated:** 2026-10-10 (pushed) | **License:** MIT
**Last verified:** 2026-10-10
**Last triaged:** 2026-10-10  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A Claude Code plugin (MIT) that picks a reasoning-effort level for each prompt
automatically instead of leaving it to the user, and adds a bar above the prompt
showing the chosen effort, prompt-cache/context fill, and how long the cache stays
warm. Offers one-click handoff or compaction when a session gets heavy. The repo's
own benchmark (four tasks) claims ~21% lower Opus cost vs. medium effort under its
default judge — a small, self-reported sample, not independently verified here.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only
(repo README plus metadata), consistent with an unattended discovery pass. The
repo's own cost-savings claim is noted above but not verified.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog — no overlap pressure (`Overlaps with`: cache-tax, ccstatusline,
claude-hud; none is a STACK pick). A Claude Code status-line/effort-selection mod in
a crowded but not identical space (cache-tax keeps the cache warm; ccstatusline/
claude-hud are display-only) — left at `discovery-log` rather than SKIPped as
redundant, since the effort-selection piece is not covered by either peer. Stamped
as examined.

_Triaged 2026-10-10 by the P3 backlog band._
