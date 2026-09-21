# Evaluation: pactflow-agent-skills

**Repo:** [pactflow/pactflow-agent-skills](https://github.com/pactflow/pactflow-agent-skills)
**Stars:** 6 | **Last updated:** 2026-09-21 (pushed) | **License:** MIT
**Last verified:** 2026-09-21
**Last triaged:** 2026-09-21  <!-- triaged: bulk -->
**Dev loop stage:** Implement (contract-testing skills/agents invoked while writing and verifying tests)
**Layer:** Tooling

---

## What it does

Official SmartBear/PactFlow plugin (MIT, Python) bundling agent skills, subagents, and an MCP
server that teach Claude Code, GitHub Copilot, Cursor, Windsurf, and other coding assistants to
work with Pact, PactFlow, and Drift contract testing. Skills cover Drift authoring, OpenAPI
parsing, and PactFlow workspace management; the bundled agents generate and review Pact tests and
run a full BDCT (bi-directional contract testing) flow end-to-end.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: a shallow clone
of the repo (README, LICENSE, plugin manifests) confirming it is real, MIT-licensed, published by
SmartBear/PactFlow, and matches its stated description.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog (pressure 0, brand new). No STACK incumbent covers contract testing for
Pact/PactFlow/Drift, so this is not a redundancy case; it is a narrow, official, domain-specific
skill pack similar in shape to `azure-skills` and `scientific-agent-skills`. Left at
`discovery-log`; too new (6 stars, same-day activity) to prioritize for a hands-on eval yet.

_Triaged 2026-09-21 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [pactflow-agent-skills](https://github.com/pactflow/pactflow-agent-skills) | plugin | Official PactFlow plugin (MIT) — skills, subagents, and an MCP server for Pact/PactFlow/Drift contract testing | Coding agents have no persistent knowledge of contract-testing workflows and need concepts re-explained every session | azure-skills, scientific-agent-skills, mcp-atlassian |  |
