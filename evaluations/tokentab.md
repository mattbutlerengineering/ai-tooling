# Evaluation: tokentab

**Repo:** [wzchav/tokentab](https://github.com/wzchav/tokentab)
**Stars:** 111 | **Last updated:** 2026-08-12 (pushed) | **License:** MIT
**Last verified:** 2026-08-13
**Last triaged:** 2026-08-13  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

A CLI that reads local Claude Code, Codex, and Gemini CLI session logs and works out what they
cost, broken down by model, project, and day.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell.

## Triage note

Overlaps `ccusage` (already ADOPT/MEASURED, in STACK) on the core job — parsing local
coding-agent session logs into cost reports — and the overlap-pressure signal challenges it. But
`ccusage`'s own catalog one-liner claims general "coding-agent" log parsing without naming which
CLIs beyond Claude Code it actually covers, while tokentab explicitly supports three (Claude
Code, Codex, and Gemini CLI) as a stated feature. Whether that is a real differentiator or
ccusage already covers the same ground needs a hands-on comparison, not a mechanical guess — a
major-tool SKIP-as-redundant call this band is not authorized to make on source-reading alone.
Left for the P0/eval-runner lane.

_Triaged 2026-08-13 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tokentab](https://github.com/wzchav/tokentab) | tool | CLI turning Claude Code, Codex, and Gemini CLI session logs into cost reports by model/project/day | Multi-CLI coding-agent spend isn't visible without parsing each tool's session logs by hand | ccusage, claude-monitor, codeburn |
