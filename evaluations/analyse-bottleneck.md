# Evaluation: analyse-bottleneck

**Repo:** [jindraregal/analyse-bottleneck](https://github.com/jindraregal/analyse-bottleneck)
**Stars:** 3 | **Last updated:** 2026-11-14 (pushed) | **License:** MIT
**Last verified:** 2026-11-14
**Last triaged:** 2026-11-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Reads local Claude Code transcripts to show where agent wall-clock time went — tests, builds, deploys, polling, model time, and waiting — in an HTML report, and suggests fixes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — catalogued today; no hands-on run yet.

## Triage note

Left at `discovery-log`, not SKIPped. It challenges `ccusage` (STACK, ADOPT) in "Overlaps with", but ccusage reports token/dollar cost from session logs, while analyse-bottleneck's specific claim is a *time* breakdown (tests/builds/deploys/polling/model/waiting) plus fix suggestions — a different measurement axis on the same local transcripts, not a clean substitute.

_Triaged 2026-11-14 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [analyse-bottleneck](https://github.com/jindraregal/analyse-bottleneck) | tool | Reads local Claude Code transcripts (MIT) to show where agent time went — tests, builds, deploys, polling, model time, waiting — and suggests fixes | Seeing where a Claude Code agent's wall-clock time actually went means reading raw transcripts by hand, with no breakdown or fix suggestions | ccusage, coding.sh, agenttrace |
