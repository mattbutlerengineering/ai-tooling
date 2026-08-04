# Evaluation: vibe-log-cli

**Repo:** [vibe-log/vibe-log-cli](https://github.com/vibe-log/vibe-log-cli)
**Stars:** 338 | **Last updated:** 2026-04-19 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (session analytics)
**Layer:** Tooling

---

## What it does

A CLI that reads local Claude Code and Cursor session logs and turns them into activity analytics —
a productivity dashboard over coding sessions rather than a one-shot table.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`ccusage`, `langfuse`). Sufficient for a SKIP that
turns on *redundancy with a catalogued incumbent*; not sufficient for a positive verdict, and none
is offered.

## Verdict

**SKIP** — redundant with [`ccusage`](https://github.com/ccusage/ccusage) (STACK, `MEASURED`). Both
tools do the same mechanical thing: parse the local coding-agent session logs already on disk and
report over them. ccusage produces daily/monthly/session/model token and cost reports and has been
run; vibe-log wraps the same source data in a productivity dashboard.

The differentiator it claims is Cursor coverage alongside Claude Code. That is real breadth, but it
is breadth into a harness this stack does not use — the second supported harness here is opencode
(ADR-0002), which vibe-log does not read. Paying a second log parser for a tool nobody runs is not
a trade worth making.

Staleness settles what the overlap leaves open: last pushed 2026-04-19, three and a half months, in
a category where the session-log format is set by harnesses that ship weekly. A log parser that
stops tracking its format quietly starts reporting nothing.

Re-open if it resumes releases *and* adds opencode, or if session *activity* analytics (as distinct
from token/cost accounting) turns out to be a question ccusage cannot answer.

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vibe-log-cli](https://github.com/vibe-log/vibe-log-cli) | tool | CLI that logs and analyzes Claude Code and Cursor coding-session activity into a dashboard | Want cross-tool (Claude Code + Cursor) session analytics rather than a one-shot table | ccusage, langfuse |
