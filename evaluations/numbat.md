# Evaluation: numbat

**Repo:** [perplexityai/numbat](https://github.com/perplexityai/numbat)
**Stars:** 256 | **Last updated:** 2026-07-29 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-07-30
**Last triaged:** 2026-07-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

Endpoint visibility into AI agent activity, from Perplexity — on-device detection, optional
pre-action blocking, and forensic reconstruction of what an agent did on a machine.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (agentlint, hol-guard, code-on-incus). Sufficient to place
the lead in Security & Safety and note it addresses runtime endpoint monitoring rather than
static skill scanning, not to support an ADOPT.

## Triage note

Left at `discovery-log` rather than SKIPped: `SkillSpector`/`skill-scanner` scan skill packages
statically before use; `agentlint`/`hol-guard`/`code-on-incus` are runtime guardrails scoped to
the agent process or its sandbox. numbat's endpoint-level, on-device detection + forensic
reconstruction is a distinct vantage point (the host, not the agent runtime), and it comes from a
major AI lab (Perplexity) rather than an unknown author. Significant enough to deserve a real
eval, not a mechanical SKIP.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._
