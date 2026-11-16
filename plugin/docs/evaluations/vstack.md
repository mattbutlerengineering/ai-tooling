# Evaluation: vstack

**Repo:** [hao-ai-lab/vstack](https://github.com/hao-ai-lab/vstack)
**Stars:** 62 | **Last updated:** 2026-11-16 (pushed) | **License:** MIT
**Last verified:** 2026-11-16
**Last triaged:** 2026-11-16  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A formal-verification workflow and skill stack for coding agents, wiring TLA+, Z3,
Apalache, and TLAPS into the agent's loop so it can check code against a formal spec
rather than relying on tests alone.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `stryker-js` (STACK pick,
overlap-cited). stryker-js is mutation testing — it checks whether existing tests catch
injected bugs; vstack is a formal-verification toolchain (TLA+/Z3/Apalache/TLAPS) that
checks code against a written specification, a fundamentally different verification
mechanism aimed at a different class of correctness bug (the tests may be fine and the
design may still violate an invariant mutation testing can't see). Not dominated by the
cited incumbent; a differentiated niche worth a real hands-on eval.

_Triaged 2026-11-16 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vstack](https://github.com/hao-ai-lab/vstack) | tool | Formal-verification workflow and skill stack (MIT) wiring TLA+, Z3, Apalache, and TLAPS into a coding agent's loop | Agent-written code can pass tests while violating the properties a spec actually requires, with no formal check catching it | gap-trap, stryker-js, verification-before-completion |
