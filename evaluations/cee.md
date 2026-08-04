# Evaluation: cee

**Repo:** [p0nymc1/cee](https://github.com/p0nymc1/cee)
**Stars:** 66 | **License:** Apache-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A deterministic-first execution engine for agent workflows, written in Go: the LLM extracts
at the edge, a deterministic state machine decides. Zero dependencies, no-code JSON plugins,
replayable runs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (conductor, deer-workflow, inngest). That is
sufficient to place the lead and note none of its named overlaps is a STACK incumbent, not
to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: conductor and inngest are durable workflow engines but don't
foreground "LLM-extracts, state-machine-decides" as an explicit architectural constraint;
deer-workflow is TypeScript-only. cee's Go, zero-dependency, replayable-run design is a real
differentiator worth a hands-on eval rather than a redundancy SKIP.

_Triaged 2026-08-04 by the daily discovery routine (today's new lead)._
