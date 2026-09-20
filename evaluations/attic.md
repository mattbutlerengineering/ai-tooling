# Evaluation: Attic

**Repo:** [NishikantaRay/Attic](https://github.com/NishikantaRay/Attic)
**Stars:** 4 | **Last updated:** 2026-09-08 (pushed) | **License:** MIT
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Process

---

## What it does

Writes an agent's findings to a local `.attic/` directory as it works, so it stops
re-reading the same files after every `/compact`. A lightweight, skill-level cache of
what the agent already learned about the codebase this session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `headroom`. headroom compresses
verbose tool output/logs before they reach the model; Attic instead persists the agent's own
*findings* to disk so they survive a `/compact` without re-deriving them — a findings cache,
not an output compressor. Complementary mechanism, not a competing one. Very early (4★, first
push this week) — worth a real look once it has more usage signal.

_Triaged 2026-09-09 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Attic](https://github.com/NishikantaRay/Attic) | skill | Writes agent findings to a local `.attic/` directory (MIT) so it stops re-reading the same files after every `/compact` | Agents re-derive the same file context on every compaction, burning tokens and turns re-learning what they already found | lean-ctx, headroom, ctxwise |
