# Evaluation: agent-smith

**Repo:** [Chengjun023/agent-smith](https://github.com/Chengjun023/agent-smith)
**Stars:** 33 | **Last updated:** 2026-10-04 (pushed) | **License:** MIT
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A tool (Python, ★33, created 2026-09-30) implementing adaptive model routing — sends
routine work to cheaper models and reserves expensive ones for complex cases — plus a
glassy Codex usage monitor and reproducible cost benchmarks ("receipts").

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Overlaps `ccusage`/`claude-monitor` (usage/cost monitoring, one ADOPT one CONDITIONAL)
and `tokencost` (CONDITIONAL — per-call cost estimation); none of those is a plain model
router, which is agent-smith's distinguishing feature, so this does not mechanically
band as P2 against any single incumbent. No archived flag, no disqualifying license, no
`Ships inside` container. Left at `discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-smith](https://github.com/Chengjun023/agent-smith) | tool | Adaptive model routing (MIT) — routes routine LLM work to cheaper models, reserves expensive ones for complex cases, plus a usage monitor and reproducible benchmarks | Running every task on the expensive model wastes spend when a cheaper model would do, with no monitor showing the savings | ccusage, claude-monitor, tokencost |
