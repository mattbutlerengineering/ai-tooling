# Evaluation: Jixu

**Repo:** [joe960913/Jixu](https://github.com/joe960913/Jixu)
**Stars:** 108 | **Last updated:** 2026-08-22 (pushed) | **License:** MIT
**Last verified:** 2026-08-23
**Last triaged:** 2026-08-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A durable single-agent harness for TypeScript with recoverable Threads, explicit side-effect boundaries, and a native terminal UI — built around crash-safe, resumable agent execution.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. Brand new (created 2026-08-18) and unproven, but the durable-execution/recoverable-Threads angle is a genuine differentiator from the incumbent lightweight harnesses (gptme, opendot) that don't survive a crash mid-run. Worth revisiting with more signal — adoption, a real run, or a comparison against letta-code's durability story — before any redundancy call.

_Triaged 2026-08-23 by the P3 backlog band (daily discovery routine)._
