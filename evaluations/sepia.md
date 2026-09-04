# Evaluation: sepia

**Repo:** [Nanako0129/sepia](https://github.com/Nanako0129/sepia)
**Stars:** 1,445 | **Last updated:** 2026-09-02 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

A De-AI writing skill for any Agent Skills-compatible agent (77+ via the Skills CLI), with
native plugins for Claude Code, Codex, Grok Build, and Antigravity — narrative-architecture
repair for fiction and venue-matched rules for professional prose.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata and the CATALOG "Overlaps with" cell. That is sufficient for the verdict below,
because the verdict turns on redundancy with a catalogued incumbent for this catalog's own
scope (agent-output humanizing), not on the tool's behavior for its broader claimed use
case (fiction/professional prose). It would not support an ADOPT, and this eval offers
none.

## Verdict

**SKIP** — redundant with `caveman` (already ADOPT/MEASURED and in STACK) for this
catalog's scope. Sepia's broader claim — fiction narrative-architecture repair across 77+
harnesses — is outside AI-*dev*-tooling scope; the part of it that is in scope (making
agent-drafted text read less like an LLM wrote it) is the same job `caveman` already does,
measured, for this catalog's actual use case.

_Triaged 2026-09-02 by the P2 challenger band (daily discovery-and-triage routine, bulk,
eliminate-only)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sepia](https://github.com/Nanako0129/sepia) | skill | De-AI writing skill (MIT) for any Agent Skills-compatible agent (77+ via the Skills CLI) — narrative-architecture repair for fiction, venue-matched rules for professional prose | Agent-drafted prose and docs read as obviously AI-generated regardless of which harness wrote them | caveman, humanizer, stop-slop |
