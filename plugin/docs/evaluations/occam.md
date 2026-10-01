# Evaluation: occam

**Repo:** [quisbaum-prog/occam](https://github.com/quisbaum-prog/occam)
**Stars:** 13 | **Last updated:** 2026-10-01 (pushed) | **License:** MIT
**Last verified:** 2026-10-01
**Last triaged:** 2026-10-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A 30-line rule set for Claude Code and Codex: prefer existing code and standard tools, read only
what matters, and keep output concise. Self-reported benchmarks claim 51-55% lower estimated task
cost on higher-tier models (plus 8.3% fewer tokens on visual-rendering tasks) while holding or
improving test pass rates.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on redundancy with
a catalogued incumbent, not on the tool's behavior — a question the overlap answers directly. It
would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `caveman` (STACK, MEASURED, 49-59% output-token reduction via a
lightweight rule-based skill). `occam` targets the same job — cut token/cost waste through a
minimal, rule-based discipline pack rather than a heavyweight framework — and its own stated
mechanism ("read only what matters, keep output concise") overlaps `caveman`'s scope directly. At
13 stars and brand new, it offers a self-reported benchmark but no measured, independent evidence
distinguishing it from an already-ADOPTED, measured incumbent doing the same job. A second tool
for this earns nothing until it demonstrates something `caveman` doesn't.

_Triaged 2026-10-01 by the P2 challenger band (today's new lead)._
