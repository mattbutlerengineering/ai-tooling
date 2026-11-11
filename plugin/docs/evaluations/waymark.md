# Evaluation: waymark

**Repo:** [QiYueran-source/waymark](https://github.com/QiYueran-source/waymark)
**Stars:** 107 | **Last updated:** 2026-11-11 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-11
**Last triaged:** 2026-11-11  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A local-first, Git-friendly work tracker that keeps project work items in Markdown files,
with support for hierarchies, dependencies, and customizable fields, per the repo's own
description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-11) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not to
judge the tool's actual behavior — it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `GSD` (STACK, MEASURED) despite the P2
band pointing there. GSD is a full context-engineering Discuss→Plan→Execute→Verify→Ship loop
with restricted-tool subagents and durable state files — a whole orchestration framework.
waymark's stated scope is narrower and more specific: a markdown-native, git-friendly work-item
tracker with hierarchies, dependencies, and custom fields, closer in job to `planning-with-files`
than to GSD's full loop. Not a clean identical-job overlap; a real eval against the
narrower-scope peers would tell more than a mechanical SKIP against GSD.

_Triaged 2026-11-11 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [waymark](https://github.com/QiYueran-source/waymark) | tool | Local-first, Git-friendly work tracker (Apache-2.0) keeping project work items in Markdown files with hierarchies, dependencies, and custom fields | Tracking project work items means a separate PM tool disconnected from git, with no markdown-native hierarchy or dependency support | planning-with-files, GSD, vibe-coding-prompt-template |
