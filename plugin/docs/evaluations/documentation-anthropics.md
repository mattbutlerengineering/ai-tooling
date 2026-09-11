# Evaluation: documentation (anthropics)

**Repo:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
**Stars:** 23,967 | **Last updated:** 2026-09-11 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-11
**Last triaged:** 2026-09-11  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A lightweight documentation skill from Anthropic's Claude-Cowork-oriented
knowledge-work plugin repo, covering READMEs, API docs, runbooks, and onboarding
guides without the multi-step overhead of a full documentation workflow.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log` rather than SKIPped: this was queued for triage with no eval
file at all. It overlaps `documentation-and-adrs`, a STACK pick — but that STACK pick
is scoped specifically to **ADRs and inline-comment philosophy**, while this skill is
general-purpose low-ceremony documentation (READMEs, runbooks, onboarding). The two
jobs are adjacent, not identical, so this isn't a clean P2 redundancy call. Not
significant enough on its own to prioritize, but not confidently dominated either.

_Triaged 2026-09-11 — daily discovery pass, oldest-untriaged sweep._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [documentation (anthropics)](https://github.com/anthropics/knowledge-work-plugins) | skill | Lightweight documentation skill covering READMEs, API docs, runbooks, and onboarding guides | Agent needs quick, low-ceremony documentation generation without multi-step workflow overhead | documentation-writer, documentation-and-adrs |
