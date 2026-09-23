# Evaluation: ming-qa

**Repo:** [mingdui/ming-qa](https://github.com/mingdui/ming-qa)
**Stars:** 28 | **Last updated:** 2026-09-21 (pushed) | **License:** MIT
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An end-to-end QA acceptance orchestrator (Python, MIT) for Claude Code/Codex/Cursor — chains
context, risk, cases, scripts, execution, review, and a report automatically, pausing only when a
generated test case needs human confirmation.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the context→risk→cases→scripts→execution→review→report pipeline. That is
sufficient to catalog it and place it relative to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog. Distinct from `gap-trap`/`i-dont-believe-you` (which gate agent-written code against
tampering/false-done claims) and `vet` — ming-qa is a QA *acceptance* pipeline generating and running
its own test cases from risk analysis, not a gate on the agent's own diff. No STACK incumbent covers
this specific shape. Left at `discovery-log`.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [ming-qa](https://github.com/mingdui/ming-qa) | skill | End-to-end QA acceptance orchestrator (MIT) for Claude Code/Codex/Cursor — context → risk → cases → scripts → execution → review → report, pausing only for case confirmation | Turning a feature into a reviewed, executed QA acceptance pass is manual at every step; want one pipeline that pauses only where judgment is needed | gap-trap, i-dont-believe-you, vet |  |
