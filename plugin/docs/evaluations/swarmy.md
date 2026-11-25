# Evaluation: swarmy

**Repo:** [koorchik/swarmy](https://github.com/koorchik/swarmy)
**Stars:** 48 | **Last updated:** 2026-11-25 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-25
**Last triaged:** 2026-11-25  <!-- triaged: bulk -->
**Dev loop stage:** Implement (multi-agent session dashboard)
**Layer:** Tooling

---

## What it does

A real-time terminal dashboard (Apache-2.0) for Claude Code, Codex, and Google
Antigravity sessions together — live agent/subagent status, history,
API-equivalent spend, weekly limits per project, worktrees, and a login vault.
Local only, read-only, ships as one static binary.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this
eval offers none.

## Triage note

Newly discovered and catalogued today via the daily discovery pass. Overlaps with
`claude-command-center`, `agent-standup`, and `agent-of-empires` (all multi-agent
session dashboards), but none of those is a STACK pick, so this does not band P2.
Its differentiator — cross-harness (Claude Code + Codex + Antigravity in one view)
plus spend/limit tracking — is a real one worth a hands-on comparison rather than a
first-day guess. Left at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [swarmy](https://github.com/koorchik/swarmy) | tool | Real-time terminal dashboard (Apache-2.0) for Claude Code, Codex, and Antigravity — live agent status, spend, limits, worktrees | Running several coding-agent CLIs in parallel gives no single local view of status, spend, or worktrees | claude-command-center, agent-standup, agent-of-empires |
