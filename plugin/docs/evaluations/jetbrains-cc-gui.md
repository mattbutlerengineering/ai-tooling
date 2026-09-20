# Evaluation: jetbrains-cc-gui

**Repo:** [zhukunpenglinyutong/jetbrains-cc-gui](https://github.com/zhukunpenglinyutong/jetbrains-cc-gui)
**Stars:** 6,120 | **Last updated:** 2026-09-10 (pushed) | **License:** MIT
**Last verified:** 2026-09-11
**Last triaged:** 2026-09-11  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An IntelliJ/JetBrains plugin (formerly "Claude Code GUI") giving Claude Code and OpenAI
Codex a native visual panel inside the IDE — `@file` context, image input, conversation
rewind, skills slash-commands, and MCP support.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log` rather than SKIPped: this was queued for triage with no eval
file at all — the oldest kind of untouched lead. Its named overlaps (`kilocode`,
`cc-switch`, `claudian`) are none of them a STACK pick, so there's no confident
redundancy call to make. 6.1K stars and real JetBrains-marketplace distribution;
deserves a real hands-on eval rather than a mechanical SKIP.

_Triaged 2026-09-11 — daily discovery pass, oldest-untriaged sweep._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jetbrains-cc-gui](https://github.com/zhukunpenglinyutong/jetbrains-cc-gui) | plugin | IntelliJ/JetBrains plugin giving Claude Code and OpenAI Codex a native visual panel — `@file` context, image input, conversation rewind, skills slash-commands, MCP (formerly "Claude Code GUI") | Claude Code/Codex are terminal-first; want them as a native GUI inside a JetBrains IDE with editor-aware context | kilocode, cc-switch, claudian |
