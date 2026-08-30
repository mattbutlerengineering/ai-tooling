# Evaluation: forward-implementation-first

**Repo:** [Vuk97/forward-implementation-first](https://github.com/Vuk97/forward-implementation-first)
**Stars:** 27 | **Last updated:** 2026-08-29 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

An agent skill (MIT) that stops coding agents from blocking real work on their own bookkeeping — hashes, locks, receipts, certification markers, and progress metadata a task didn't ask for.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`HERO-Anti-OverDefense`, `stop-that-shit`, `ratchet`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. `HERO-Anti-OverDefense` and `stop-that-shit` target over-defense and unrequested scaffolding broadly; this one names a narrower failure mode (self-imposed bookkeeping specifically) that neither calls out explicitly. Whether that narrower framing earns its own seat, or is fully covered by the broader skills, needs a real comparison.

_Triaged 2026-08-30 by the P3 backlog band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [forward-implementation-first](https://github.com/Vuk97/forward-implementation-first) | skill | Agent skill (MIT) stopping coding agents from blocking real work on their own bookkeeping — hashes, locks, receipts, certification markers | Agents self-impose unrequested bookkeeping scaffolding that blocks the actual task | HERO-Anti-OverDefense, stop-that-shit, ratchet |
