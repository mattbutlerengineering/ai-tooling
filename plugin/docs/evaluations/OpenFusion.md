# Evaluation: OpenFusion

**Repo:** [calesthio/OpenFusion](https://github.com/calesthio/OpenFusion)
**Stars:** 11 | **Last updated:** 2026-10-29 (pushed) | **License:** MIT
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Multi-model router for coding agents: inspects each task and sends it to the cheapest
model capable of doing it well, rather than running every task through one fixed
priced model. Advertises support across Claude Code, Codex, Cursor, GitHub Copilot,
Gemini CLI, Antigravity, and OpenCode.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. At 11 stars and a few days old, the routing
quality (does the "cheapest capable" heuristic actually hold up) is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today, no STACK-pick overlap.
Not examined further in this pass.

_Triaged 2026-11-03 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [OpenFusion](https://github.com/calesthio/OpenFusion) | tool | Multi-model router (MIT) sending each coding-agent task to the cheapest model that can do it well | Every task gets routed through one priced model with no per-task cheapest-capable routing across harnesses | cheap-ag, frugent, litellm |
