# Evaluation: buried-injections

**Repo:** [rudratoshs/buried-injections](https://github.com/rudratoshs/buried-injections)
**Stars:** 18 | **Last updated:** 2026-09-26 (pushed) | **License:** MIT
**Last verified:** 2026-09-26
**Last triaged:** 2026-09-26  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A reproducible benchmark (MIT) showing that a plain regex filter catches 0% and Meta's Prompt
Guard 2 catches ~1% of 629 realistic AgentDojo injection attacks when the injection is buried
inside tool output rather than the user's own prompt.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this benchmark. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (agent-scan, agentshield, trustmcp). That is
sufficient to note it as a reference data point about existing defenses' miss rate, not to
independently verify the 0%/1% figures against our own corpus — it would not support an ADOPT,
and this eval offers none.

## Triage note

Left at `discovery-log`: this is a benchmark/reference quantifying a real gap in existing
prompt-injection defenses (regex filters, Prompt Guard 2), not a competing scanner — it doesn't
overlap a STACK pick and there is nothing here to call redundant. Worth a closer read when
evaluating any of the MCP/agent security scanners already in the catalog, to see whether their
own claims hold up against this benchmark's methodology.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [buried-injections](https://github.com/rudratoshs/buried-injections) | tool | Reproducible benchmark (MIT) showing regex and Meta's Prompt Guard 2 catch 0-1% of prompt-injection attacks buried in tool output | Teams assume a regex filter or Prompt Guard catches prompt injection in tool output; want quantified evidence of the actual miss rate | agent-scan, agentshield, trustmcp |
