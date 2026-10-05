# Evaluation: your-cto-jev

**Repo:** [rainday/your-cto-jev](https://github.com/rainday/your-cto-jev)
**Stars:** 0 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A git-hook guardrail that blocks leaked secrets and destructive commands from AI coding agents (Claude Code, Cursor, Gemini CLI, Codex) before they execute.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. Day-one repo (created 2026-10-01), 0
stars — too early to judge quality or differentiation hands-on.

## Triage note

Left at `discovery-log`, not SKIPped. This is a new day-one entrant in an already-dense
secrets/destructive-command-guard cluster (`cc-safety-net`, `secretguard-mcp`,
`toolpermit`). Multi-harness coverage (Claude Code, Cursor, Gemini CLI, Codex) in one
hook is a plausible differentiator from `cc-safety-net` (Claude-Code-only), but at 0
stars and days old there isn't enough signal for a defensible redundancy SKIP.
Revisit once it has real usage.

_Triaged 2026-10-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [your-cto-jev](https://github.com/rainday/your-cto-jev) | tool | Git-hook guardrail (MIT) blocking leaked secrets and destructive commands from Claude Code, Cursor, Gemini CLI, and Codex | Agents can commit leaked secrets or run destructive commands with no pre-execution check gating them | cc-safety-net, secretguard-mcp, toolpermit |
