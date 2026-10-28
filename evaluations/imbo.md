# Evaluation: imbo

**Repo:** [Bearisbug/imbo](https://github.com/Bearisbug/imbo)
**Stars:** 16 | **Last updated:** 2026-10-28 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Instant messaging between coding-agent sessions (Rust) — Claude Code, Codex, opencode, Cursor CLI, MiniMax Code, and ZCode — across tools and to other people's agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and the CATALOG one-liner/overlaps (agent-link, succubus, reason-network, multiplayer-ai). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. None of its overlapping neighbors is a STACK pick today, so it doesn't land in P2 challenger, and no license/archival signal disposes it mechanically.

## Triage note

P3 backlog. Left at `discovery-log`; its cross-tool and cross-person messaging (not just cross-machine, same-harness like `succubus`/`fleetpost`) is a real differentiator worth a hands-on look in a future pass.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [imbo](https://github.com/Bearisbug/imbo) | tool | Instant messaging between coding-agent sessions (Apache-2.0, Rust) — Claude Code, Codex, opencode, Cursor CLI, and others, across tools and to other people's agents | Coding-agent sessions running in parallel, even across different tools or people, have no direct way to message each other | agent-link, succubus, reason-network, multiplayer-ai |
