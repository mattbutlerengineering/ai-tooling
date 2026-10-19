# Evaluation: tetriz-harness

**Repo:** [tetriz-ai/tetriz-harness](https://github.com/tetriz-ai/tetriz-harness)
**Stars:** 18 | **Last updated:** 2026-10-18 (pushed) | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Recommends changes to the harness that guides a team's AI coding agents — rules, skills,
hooks, agents, and MCP config — from the repository it works in and coding signals. A human
reviews the recommendations, then a control plane distributes selected changes to chosen
developers, teams, or a test group (audience-targeted rollout, manual test/control).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the README,
the CATALOG one-liner, and GitHub repo metadata (stars, license, topics). No hands-on run was
performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

New lead, cataloged today. P3 backlog — zero overlap pressure. Closest peer `model-citizen`
is itself a discovery-log lead, not a STACK pick, so not a P2 challenger despite the shared
"cross-harness rules/skills/hooks control plane" framing. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [tetriz-harness](https://github.com/tetriz-ai/tetriz-harness) | tool | Recommends harness changes (MIT) from a repo's own code and coding signals, then rolls approved rules/skills/hooks/agents out to chosen people or teams | Harness config (rules, skills, hooks, MCP) drifts per developer with no recommendation engine or controlled, audience-targeted rollout across a team | model-citizen, ai-rules-sync, capa |  |
