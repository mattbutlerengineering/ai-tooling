# Evaluation: agents-towards-production

**Repo:** [NirDiamant/agents-towards-production](https://github.com/NirDiamant/agents-towards-production)
**Stars:** 20,949 | **Last updated:** 2026-07-04 (pushed) | **License:** NOASSERTION
**Dev loop stage:** Reference
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

End-to-end, code-first tutorials for taking a GenAI agent from prototype to enterprise deployment —
observability, memory, orchestration, security, evals and deployment.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this — it is a tutorial collection. Source-grounded only: GitHub
metadata (fetched 2026-08-04) plus the CATALOG one-liner and "Overlaps with" cell (`genai-agents`,
`ai-engineering-from-scratch`, `12-factor-agents`). Enough to place it; not enough for any verdict,
and none is offered.

## Triage note

Left at `discovery-log`. ★21K, pushed 2026-07-04, and the same author as `genai-agents` — the two
are deliberately sequential rather than competing: one teaches building an agent, this one teaches
hardening it.

The production half is the part with the least coverage anywhere in the catalog. "Build an agent"
material is abundant; evals, observability and deployment for agents are exactly where the published
guidance thins out, which is the gap this fills and the reason it is not a disposable duplicate of
its sibling.

It is agent *building* rather than agent-assisted coding, the standing adjacency of this whole
teaching cluster. Licence resolves to `NOASSERTION` (unparsed, not absent).

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agents-towards-production](https://github.com/NirDiamant/agents-towards-production) | reference | End-to-end, code-first tutorials (★21K, by NirDiamant) for taking GenAI agents from prototype to enterprise deployment — observability, memory, orchestration, security, evals, deployment | Plenty of "build an agent" demos, few that cover the production hardening (eval, deploy, observe) needed to ship one | genai-agents, ai-engineering-from-scratch, 12-factor-agents |
