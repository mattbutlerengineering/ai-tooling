# Evaluation: headcount

**Repo:** [cbrock84/headcount](https://github.com/cbrock84/headcount)
**Stars:** 1,031 | **Last updated:** 2026-08-28 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Process

---

## What it does

An agent organization for Claude Code, structured as a company — 15+ departments, 125+
independently installable skills.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata and the CATALOG "Overlaps with" cell.

## Triage note

Bands as a P2 challenger against `mattpocock/skills` / `agent-skills` (score computed from
the "Overlaps with" cell), but per the triage-lead guidance not to SKIP a major tool as
"redundant" — headcount is a substantial pack (1,031★) organized around a distinct
department/role taxonomy rather than a flat skill list, which is a real structural
difference from the incumbents, not a copy. Left at `discovery-log` for a real evaluation
of whether that organization actually helps skill discovery, rather than disposed as a
mechanical SKIP.

_Triaged 2026-09-02 by the P2 challenger band (daily discovery-and-triage routine, bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [headcount](https://github.com/cbrock84/headcount) | plugin | Agent organization for Claude Code (MIT) — 15+ departments, 125+ independently installable skills structured like a company | Skill packs are unstructured piles; want skills organized by department/role so a specialist is easy to find and install alone | mattpocock/skills, agent-skills, orchestkit |
