# Evaluation: carrick

**Repo:** [carrick-tools/carrick](https://github.com/carrick-tools/carrick)
**Stars:** 2 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** Elastic License 2.0 (source-available, not OSI-approved)
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A type-aware, intent-aware cross-repo index of a codebase's TypeScript services, exposed to agents (Claude Code, Cursor, Windsurf, Codex) over MCP. Scans in CI and flags cross-repo API mismatches on PRs — e.g. finding functions by intent or validating cross-repo type compatibility.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Zero overlap pressure (P3 backlog). Conceptually adjacent to `sem`/`ts-morph`/`repowise` (structural/semantic code understanding for agents), differentiated by its cross-*repo* TypeScript-service focus and CI-integrated PR checks rather than single-repo entity diffing. Not a P4 mechanical-skip candidate — Elastic License 2.0 is non-permissive source-available, but P4 only applies to *vendored* Types (skill/plugin) copied into a consuming repo; this is an MCP server you run, not text you vendor, so the license doesn't propagate the way a skill's would. Worth noting for a future eval regardless: Elastic License 2.0 does restrict offering it as a competing hosted service.

_Triaged 2026-09-04 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [carrick](https://github.com/carrick-tools/carrick) | MCP server | Type-aware, intent-aware cross-repo index of TypeScript services (⚠️ Elastic License 2.0), exposed to agents over MCP — scans in CI and flags cross-repo API mismatches on PRs | Agents can't see type/intent compatibility across service boundaries in a multi-repo TypeScript codebase; want that indexed and checked in CI | sem, ts-morph, repowise |
