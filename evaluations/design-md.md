# Evaluation: design.md

**Repo:** [google-labs-code/design.md](https://github.com/google-labs-code/design.md)
**Stars:** 25,534 | **Last updated:** 2026-07-01 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

A format specification for a `DESIGN.md` file that gives coding agents a persistent, structured
understanding of a project's design system — visual identity, tokens, component conventions —
read the way an agent reads `CONTEXT.md`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** apply this format to a project. This evaluation is source-grounded only: repo
metadata plus the CATALOG one-liner and "Overlaps with" cell (`documentation-and-adrs`,
`agent-rules-books`). Sufficient to place the lead against the STACK incumbent it names; not
sufficient for a positive verdict, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. Its STACK overlap is
[`documentation-and-adrs`](https://github.com/addyosmani/agent-skills), but the two produce
different artifacts: that skill records *decisions and their rationale* (ADRs), while design.md
specifies a durable schema for *design-system facts* an agent needs on every UI task. One is a
decision log, the other a reference sheet; adopting either does not answer the other's need.

It is also Type `reference` — a format to follow, not software to install — so "redundant with an
incumbent" is a weaker frame here than for a tool competing for the same slot. First-party Google
Labs, Apache-2.0, 25K stars. The real question for a real evaluation is whether a `DESIGN.md`
actually changes agent output on frontend work, which is a with/without measurement
(`evaluations/measurement-protocols.md`), not a triage call.

_Triaged 2026-08-04 by the P2 challenger band ([#265](https://github.com/mattbutlerengineering/ai-tooling/issues/265))._
