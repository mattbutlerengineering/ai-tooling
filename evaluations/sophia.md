# Evaluation: sophia

**Repo:** [zhengjiaqiao/sophia](https://github.com/zhengjiaqiao/sophia)
**Stars:** 0 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** Plan (skill/MCP management)
**Layer:** Tooling

---

## What it does

A desktop app (Rust/Tauri) linking skills, MCP servers, and models into Claude Code,
Codex, Cursor, and 37+ other agents with one click.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. Day-one repo, 0 stars.

## Triage note

Left at `discovery-log`, stamped only (P3 backlog — no STACK pick cited). Overlaps
`skills-hub` (also a cross-platform desktop app syncing skills) and `capa`/
`harness-ai-kit` (config-portability tools) closely enough that it may turn out
redundant, but at 0 stars and days old there's no way to tell whether its "37+ agents,
one click" claim holds up any better than the incumbents' narrower claims.

_Triaged 2026-10-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sophia](https://github.com/zhengjiaqiao/sophia) | tool | Desktop app (MIT, Rust/Tauri) linking skills, MCP servers, and models into Claude Code, Codex, Cursor, and 37+ other agents with one click | Skill/MCP/model config must be re-wired by hand per coding-agent harness; want one desktop app to link them everywhere | skills-hub, capa, harness-ai-kit |
