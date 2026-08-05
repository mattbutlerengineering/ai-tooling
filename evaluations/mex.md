# Evaluation: mex

**Repo:** [mex-memory/mex](https://github.com/mex-memory/mex)
**Stars:** 1,149 | **Last updated:** 2026-07-08 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Persistent project memory for coding agents: a structured scaffold plus a CLI that detects when the
recorded memory has **drifted** from what the codebase actually is.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus
the CATALOG one-liner and "Overlaps with" cell (`claude-mem`, `cognee`, `mem0`). Sufficient to place
it against the STACK incumbent it names; not sufficient for a positive verdict, and this eval offers
none.

## Triage note

Left at `discovery-log`, not SKIPped. It overlaps
[`claude-mem`](https://github.com/thedotmack/claude-mem) (STACK, `ADOPT`/`MEASURED`) on persistent
project memory, but it claims an axis nothing else in this 21-lead band does: **drift detection** —
noticing that stored memory no longer matches reality.

That failure mode is the one this repo's own doctrine treats most seriously. Stale recorded facts
are worse than absent ones because they read as current; it is the same reasoning behind
`**Last verified:**` staleness sweeps and detector R's metadata ageing. A memory tool that says
"this belief is now wrong" rather than confidently reciting it is attacking a real problem, and
nothing in STACK does.

Small (1.1K stars) and unverified, so the claim needs exercising before it counts — P0 work, not a
bulk SKIP.

_Triaged 2026-08-04 by the P2 challenger band ([#264](https://github.com/mattbutlerengineering/ai-tooling/issues/264))._
