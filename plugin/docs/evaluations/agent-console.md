# Evaluation: agent-console

**Repo:** [LockedinLabs-AI/agent-console](https://github.com/LockedinLabs-AI/agent-console)
**Stars:** 287 | **Last updated:** 2026-09-27 (pushed) | **License:** MIT
**Last verified:** 2026-09-27
**Last triaged:** 2026-09-27  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A local observability console for Claude Code and Codex — sessions, subagents,
tokens, and estimated model costs, aggregated across multiple machines into one
console. Privacy-first by the README's own framing: only metadata (token counts,
hashed identifiers) is shared between machines, never prompt or file content.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the README's description of scope and privacy model. That is
sufficient for a discovery-log entry, not for an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`. It cites `ccusage` in Overlaps with, but ccusage is a
single-machine CLI that parses local session logs into cost reports; agent-console's
distinguishing claim is cross-machine aggregation plus subagent-level tracking, which
ccusage does not do. Not clearly dominated — differentiated enough to deserve a real
look rather than a mechanical "redundant with ccusage" SKIP.

_Triaged 2026-09-27 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-console](https://github.com/LockedinLabs-AI/agent-console) | tool | Local observability console (MIT) for Claude Code and Codex — sessions, subagents, tokens, and model costs across machines, privacy-first | Can't see session/subagent/token/cost activity across multiple coding-agent machines in one place without parsing logs by hand | ccusage, agentacct, tokentab |
