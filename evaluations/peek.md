# Evaluation: peek

**Repo:** [mstuart/peek](https://github.com/mstuart/peek)
**Stars:** 0 | **Last updated:** 2026-08-09 (pushed) | **License:** MIT
**Last verified:** 2026-08-09
**Last triaged:** 2026-08-09  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

DevTools for coding agents — session composition, cost attribution, compaction forensics, and config A/B benchmarking across Claude Code, Codex, and pi. Parses local session logs to show not just what a session cost but why (which config choices drove it) and what happened at compaction boundaries.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead and compare it against the existing observability incumbents, not to judge whether its cost-attribution or compaction-forensics claims hold up in practice.

## Verdict

**discovery-log — tentative read** — Distinct from ccusage/claude-monitor (cost totals) in scope: "compaction forensics" and "config A/B benchmarking" aren't offered by the existing cost/usage tools in the catalog. Zero stars, day-old repo — worth a real look once it has some track record, not a mechanical SKIP as redundant with ccusage.

_Triaged 2026-08-09 by the P2 challenger band._
