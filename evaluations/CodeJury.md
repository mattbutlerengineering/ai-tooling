# Evaluation: CodeJury

**Repo:** [krishagarwal314/CodeJury](https://github.com/krishagarwal314/CodeJury)
**Stars:** 136 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Terminal-first multi-agent SDLC pipeline that scopes requirements, implements, tests, and gates PRs with ensemble review.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (via `repo-metadata.json`, fetched 2026-08-04) plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — not previously examined; picked up as one of the oldest untriaged leads in the P3 backlog this pass.

## Triage note

P3 backlog (no STACK overlap flagged). Overlaps `BMAD-METHOD`/`ccpm`/`flow-next` (all discovery-log or non-STACK) rather than a STACK pick, so there is no redundancy call to make here. Small (136★) but not clearly dominated — left at discovery-log.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [CodeJury](https://github.com/krishagarwal314/CodeJury) | tool | Terminal-first multi-agent SDLC pipeline — scopes requirements, implements, tests, and gates PRs with ensemble review | Ad-hoc agent coding skips requirements/tests and ships PRs with no deterministic QA gate | BMAD-METHOD, ccpm, flow-next |  |
