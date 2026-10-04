# Evaluation: codex-kit

**Repo:** [zhaoFenG8917/codex-kit](https://github.com/zhaoFenG8917/codex-kit)
**Stars:** 3 | **Last updated:** 2026-10-01 (pushed) | **License:** MIT
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A single-binary, zero-dependency CLI toolkit (Rust, ★3, created 2026-09-29) bundling
system utilities for AI coding agents — `ls`, `tree`, `info`, `stat`, `replace`, `head`,
`tail`, `wc`, `diff` — with JSON-native output and automatic GBK/UTF-8 encoding
handling across platforms.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Low signal (★3, 3 days old) but a genuine, narrow niche: a cross-platform utility belt
specifically built for agent consumption (JSON output, encoding handling) rather than
reused human-facing coreutils. Overlaps `usagetrim` (discovery-log — folds verbose
dev-tool output) and `jevgrep` (discovery-log — finds files by what code does); neither
is a STACK pick, and codex-kit's job (basic file/text ops with structured output) is
distinct from both. No archived flag, no disqualifying license, no `Ships inside`
container. Left at `discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codex-kit](https://github.com/zhaoFenG8917/codex-kit) | tool | Single-binary, zero-dependency CLI toolkit (MIT, Rust) for AI coding agents — ls, tree, info, stat, replace, head, tail, wc, diff with JSON-native output | Agents shell out to a different system utility per task, each with inconsistent output and encoding handling across platforms | usagetrim, jevgrep |
