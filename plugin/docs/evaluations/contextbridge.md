# Evaluation: contextbridge

**Repo:** [BoneD-Q/contextbridge](https://github.com/BoneD-Q/contextbridge)
**Stars:** 69 | **Last updated:** 2026-11-20 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-25
**Last triaged:** 2026-11-25  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context (cross-agent context handoff)
**Layer:** Process

---

## What it does

A skills-first AI context handoff tool (Apache-2.0) with structured evidence,
uncertainty tracking, validation, and cross-agent knowledge transfer.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this
eval offers none.

## Triage note

Newly discovered and catalogued today via the daily discovery pass. Overlaps with
`handoff-skill`, `sno-station`, and `portable-handoff` (all context-handoff tools),
but none of those is a STACK pick, so this does not band P2. Its claimed
differentiators — structured evidence and explicit uncertainty tracking on the
handoff, rather than a plain resumable doc — are worth a real comparison. Left at
`discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [contextbridge](https://github.com/BoneD-Q/contextbridge) | skill | Skills-first AI context handoff (Apache-2.0) with structured evidence, uncertainty tracking, and cross-agent knowledge transfer | Switching agents or sessions loses accumulated context, with no structured evidence trail for what the next agent should trust | handoff-skill, sno-station, portable-handoff |
