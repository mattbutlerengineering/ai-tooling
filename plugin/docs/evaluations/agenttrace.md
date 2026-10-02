# Evaluation: agenttrace

**Repo:** [tensorstax/agenttrace](https://github.com/tensorstax/agenttrace)
**Stars:** 84 | **Last updated:** not independently verified (GitHub API unavailable for this repo in this session) | **License:** MIT
**Last verified:** 2026-10-02
**Last triaged:** 2026-10-02  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

A lightweight observability library to trace and evaluate agentic systems — local tracing/eval
for debugging agent behavior without a hosted platform.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This session's GitHub API access is scoped to the
`ai-tooling` repo only, so repo facts came from the public repo page rather than `gh api`.
Source-grounded only: the repo's own README description plus the CATALOG "Overlaps with" cell.
Note: several unrelated repos share the "agenttrace"/"AgentTrace" name on GitHub; this evaluation
is specifically about `tensorstax/agenttrace`. Sufficient to place the lead, not to support any
verdict, and none is offered.

## Triage note

Left at `discovery-log`. No STACK pick is cited in its "Overlaps with" cell, so this bands P3 —
nothing structural forces a disposition. The Observability category already holds several local,
lightweight session-tracing tools (bar-observatory, tracecrate, peek), but this one is pitched at
general agentic-system tracing/eval rather than specifically Claude Code sessions, which is a
distinct enough angle to leave for a real look rather than dispose mechanically.

_Triaged 2026-10-02 by the P3 backlog band (daily discovery pass)._
