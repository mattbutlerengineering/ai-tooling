# Evaluation: claude-context-optimizer

**Repo:** [egorfedorov/claude-context-optimizer](https://github.com/egorfedorov/claude-context-optimizer)
**Stars:** 71 | **Last updated:** 2026-07-06 (pushed) | **License:** MIT
**Last verified:** 2026-07-10
**Last triaged:** 2026-07-10  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling (Claude Code plugin)

---

## What it does

A local Claude Code plugin that flags unused high-token files in context and prescribes
concrete Grep/compact fixes with an estimated token saving — closing the gap between
"spend is high" telemetry and "which context is wasted, and what do I do about it."

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: it
rests on GitHub repo metadata (MIT, 71 stars, pushed 2026-07-06) and the `CATALOG.md`
"Overlaps with" cell. That is sufficient for the verdict below, because the verdict
turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a
question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with [`headroom`](https://github.com/headroomlabs-ai/headroom).
Headroom is the STACK incumbent for the context/token-optimization job (MEASURED, and
installed), compressing tool output before it reaches the context window. claude-context-optimizer
addresses the same signal — high-token context waste — from the narrower angle of
flagging unused files, and it overlaps headroom directly per its own CATALOG row
(`headroom, claw-compactor, lean-ctx`). A second, less-proven tool for a job STACK
already covers earns nothing; nothing here is differentiated enough to warrant a
first-time hands-on eval.

_Triaged 2026-07-10 by the P2 challenger band. Eliminate-only: this lane may SKIP a
redundant lead or leave it at discovery-log, never adopt one. Headroom was named as the
incumbent it duplicates; a false SKIP here is cheap and reversible._
