# Evaluation: skill_manager

**Repo:** [ssssssanjiu/skill_manager](https://github.com/ssssssanjiu/skill_manager)
**Stars:** 11 | **Last updated:** 2026-09-13 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Plan (skill management)
**Layer:** Tooling

---

## What it does

Local, zero-dependency web panel for managing Claude Code skills — paste a GitHub URL to install, symlink-hosted with zero copies, plus a daily feed of newly published skills.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — new (created 2026-09-09), catalogued from today's discovery scan.

## Triage note

P3 backlog. Overlaps `skills-hub` (a cross-platform desktop app doing similar install/organize/sync work) and `openskills`/`vercel-labs/skills` (cross-tool installer CLIs), but skill_manager is specifically a Claude-Code-scoped local web panel with a discovery feed — narrower scope, different surface. Left at discovery-log rather than SKIPped given the differentiated surface (browser panel vs. desktop app vs. CLI).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [skill_manager](https://github.com/ssssssanjiu/skill_manager) | tool | Local, zero-dependency web panel (MIT) for managing Claude Code skills — paste a GitHub URL to install, symlink-hosted with zero copies, plus a daily feed of newly published skills | Installing and tracking Claude Code skills means manually cloning/symlinking each one with no single view of what's installed | skills-hub, skill-view, openskills |  |
