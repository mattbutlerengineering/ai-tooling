# Evaluation: source-reading-methodology

**Repo:** [itshen/source-reading-methodology](https://github.com/itshen/source-reading-methodology)
**Stars:** 100 | **Last updated:** 2026-08-23 (pushed) | **License:** MIT
**Last verified:** 2026-08-24
**Last triaged:** 2026-08-24  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

A four-phase methodology plus reusable templates for AI-assisted deep reading of large
open source repositories, with a checklist of pitfalls; the stated goal is that every
technical claim an agent makes about the codebase traces back to a specific source line.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`. It cites no STACK pick in "Overlaps with"
(`PocketFlow-Tutorial-Codebase-Knowledge`, `project-mentor`, and `graphify` are all
`discovery-log`/unadopted leads), so it doesn't clear the P2 challenger bar. Not archived,
permissively licensed, not a vendored skill/plugin Type, no `Ships inside` declared. A
process methodology aimed specifically at making agent claims about unfamiliar code
verifiable (traceable to source lines) is a distinct angle on Code Understanding worth a
real look.

_Triaged 2026-08-24 by the P3 backlog band (daily discovery)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [source-reading-methodology](https://github.com/itshen/source-reading-methodology) | skill | Four-phase methodology + reusable templates for AI-assisted deep reading of large open source repos (MIT) | Agent summaries of unfamiliar codebases are unverifiable prose; want every technical claim traceable back to a specific source line | PocketFlow-Tutorial-Codebase-Knowledge, project-mentor, graphify |
