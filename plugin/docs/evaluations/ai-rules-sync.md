# Evaluation: ai-rules-sync

**Repo:** [lbb00/ai-rules-sync](https://github.com/lbb00/ai-rules-sync)
**Stars:** 35 | **Last updated:** 2026-08-14 (pushed) | **License:** Unlicense
**Last verified:** 2026-08-14
**Last triaged:** 2026-08-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Synchronize AI rules, skills, commands, and subagents (Unlicense) across Cursor, Claude Code, Copilot, OpenCode, Trae, Codex, Gemini CLI, Warp." Keeps per-editor AI instruction/skill/command files in sync across eight+ editors from one source.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to catalog the lead, not to reach a verdict.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`: overlaps `capa` (capabilities.yaml wiring skills/tools/rules across 35+
editors) and `reporails/cli` (instruction diagnostics), but ai-rules-sync's stated scope is
narrower and more specific — *synchronizing* existing per-editor rule/skill/command files rather
than a unified config format or a diagnostics tool — so a mechanical "redundant with capa" SKIP
isn't clearly right without reading both more closely. Left for a closer look.

_Triaged 2026-08-14 by the P3 backlog band (daily discovery routine)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ai-rules-sync](https://github.com/lbb00/ai-rules-sync) | tool | Synchronize AI rules, skills, commands, and subagents (Unlicense) across Cursor, Claude Code, Copilot, OpenCode, Trae, Codex, Gemini CLI, Warp | Team/project AI instructions and skills drift out of sync when maintained separately per editor | capa, reporails/cli, openskills |
