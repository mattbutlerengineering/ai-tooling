# Evaluation: agent-eval-loop

**Repo:** [relai-ai/agent-eval-loop](https://github.com/relai-ai/agent-eval-loop)
**Stars:** 27 | **Last updated:** 2026-11-14 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-14
**Last triaged:** 2026-11-14  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Builds evals from traces, code, and coding sessions to measure and improve AI agent behavior, including coding agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — catalogued today; no hands-on run yet.

## Triage note

Left at `discovery-log`, not SKIPped. Zero overlap pressure (brand new). The "builds evals from your own real traces" framing is a different starting point than `assay`/`agentagon`'s audit-the-artifact approach, worth a first-time read rather than a mechanical redundancy call.

_Triaged 2026-11-14 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-eval-loop](https://github.com/relai-ai/agent-eval-loop) | tool | Builds evals from traces, code, and coding sessions (Apache-2.0) to measure and improve coding-agent behavior | Judging whether a coding agent's behavior actually improved is guesswork without evals built from its own real traces and sessions | assay, agentagon, vet |
