# Evaluation: claude-rein

**Repo:** [shasyasan/claude-rein](https://github.com/shasyasan/claude-rein)
**Stars:** 2 | **Last updated:** 2026-09-06 (pushed) | **License:** MIT
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A plugin that automatically hands a Claude Code session over to a fresh one before a long task exhausts the context window, with no manual restart or handoff note required.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `headroom` despite the overlap citation. headroom compresses tool output/logs *before* they reach the model to slow context growth; claude-rein instead triggers a full session handover once the budget nears exhaustion — a different point in the same problem (reduce consumption vs. transfer state), not the same job duplicated. 2★, one day old.

_Triaged 2026-09-07 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-rein](https://github.com/shasyasan/claude-rein) | plugin | Automatic session handover for Claude Code (MIT) before a long task exhausts the context window | A long task wearing out context mid-way forces a manual restart and a rewritten handoff note | Continuous-Claude-v3, headroom, dot-reflex |
