# Evaluation: agent-hud-open

**Repo:** [jazzenchen/agent-hud-open](https://github.com/jazzenchen/agent-hud-open)
**Stars:** 84 | **Last updated:** 2026-10-28 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A HUD (Rust/Tauri) for Claude Code, Codex, and 16 more coding agents — quotas, tokens, and session status at a glance, with the ability to answer a waiting agent and jump back in one click, from the desktop, phone, or watch.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (abtop, ccusage). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. It overlaps `abtop` (CONDITIONAL) and `ccusage` (ADOPT, already in STACK) on quota/token tracking, but its scope is broader — 18+ agents rather than a Claude-Code-centric terminal view — and it adds interactive, cross-device surfaces (phone, watch, "jump back in one click") that neither incumbent covers. That breadth is enough to leave it for a real hands-on look rather than dispose it as a mechanical redundancy.

## Triage note

P2 challenger — cites `abtop` and `ccusage` in "Overlaps with". Left at `discovery-log` rather than SKIPped: the multi-agent breadth and cross-device control surface are a meaningfully different value proposition from either incumbent's narrower scope, and that needs a hands-on comparison, not a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-hud-open](https://github.com/jazzenchen/agent-hud-open) | tool | HUD for Claude Code, Codex, and 16 more coding agents (Rust) — quotas, tokens, and sessions at a glance; answer requests and jump back in one click, on screen, phone, or watch | Running several coding-agent CLIs gives no at-a-glance view of quota, token usage, or session status across all of them | claude-monitor, ccusage, hotseat, abtop |
