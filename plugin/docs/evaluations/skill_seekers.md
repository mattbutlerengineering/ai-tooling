# Evaluation: Skill_Seekers

**Repo:** [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)
**Stars:** 14,883 | **Last updated:** 2026-08-30 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A source-to-skill compiler: scrapes docs sites, GitHub repos, PDFs, and videos and
packages one knowledge asset for Claude, Gemini, OpenAI, LangChain, and vector DBs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata and the CATALOG "Overlaps with" cell.

## Triage note

Bands as a P2 challenger against `skill-creator` (score computed from the "Overlaps with"
cell), but per the triage-lead guidance not to SKIP a major tool as "redundant" —
Skill_Seekers is a substantial, actively-maintained project (14.9K★) whose own catalog row
already distinguishes its job from `skill-creator`'s ("authors/optimizes" vs. this tool's
"ingest once, export to every AI platform" compiler role). Left at `discovery-log` for a
real evaluation rather than a mechanical SKIP.

_Triaged 2026-09-02 by the P2 challenger band (daily discovery-and-triage routine, bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | tool | Source-to-skill compiler: scrapes docs sites / GitHub repos / PDFs / videos and packages one knowledge asset for Claude, Gemini, OpenAI, LangChain, and vector DBs | Hand-authoring a skill or RAG index from a library's docs is slow; ingest once, export to every AI platform | skill-creator (authors/optimizes), SkillOpt (trains), openskills (install), capa (wire) |
