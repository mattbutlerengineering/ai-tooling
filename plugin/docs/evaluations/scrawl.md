# Evaluation: scrawl

**Repo:** [kitlangton/scrawl](https://github.com/kitlangton/scrawl)
**Stars:** 707 | **Last updated:** 2026-10-23 (pushed) | **License:** MIT
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A macOS screen recorder (Rust, GPUI) that lets you mark up a recording — annotate,
highlight, point — and send it straight to a coding agent (Claude Code, opencode) instead
of describing the problem in words.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-14) but already well-starred (★707 in ~9 days) — real
traction. Its "Overlaps with" cell names `Remarc`, `sim-agentation`, and `ilse`, none of
which is a STACK pick, so this does not band as a P2 challenger. No archived flag, no
disqualifying license, no `Ships inside` container. Differentiator over the existing
point-and-annotate peers is the screen-*recording* format (a video with markup) rather
than a static screenshot or live simulator overlay. Left at `discovery-log`; its star
trajectory makes it a reasonable near-term hands-on-eval candidate.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [scrawl](https://github.com/kitlangton/scrawl) | tool | macOS screen recorder (MIT, Rust/GPUI) that lets you mark up a recording and send it straight to a coding agent | Reporting a UI or behavior problem to a coding agent means describing it in words; want to mark up a screen recording and hand it over directly | Remarc, sim-agentation, ilse |
