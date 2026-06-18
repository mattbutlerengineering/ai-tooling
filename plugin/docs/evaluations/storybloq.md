# Evaluation: Storybloq

**Repo:** [Storybloq/storybloq](https://github.com/Storybloq/storybloq)
**Stars:** 618 | **Last updated:** 2026-06-18 | **License:** PolyForm-Noncommercial-1.0.0
**Dev loop stage:** Implement / Reflect
**Layer:** Tooling

---

## What it does

Cross-session context persistence for AI coding agents. Ships as a CLI, an MCP server (53 tools), a Claude Code `/story` skill, and a native Mac app. Every project gets a `.story/` directory with JSON and markdown files: tickets, issues, roadmap phases, session handovers, and lessons learned — all git-tracked and agent-readable.

The mechanism is structured project state: instead of agents loading context by reading files ad-hoc, storybloq pre-computes summaries via MCP calls (`storybloq_status`, `storybloq_recap`, `storybloq_handover_latest`). Their own benchmark shows 34x faster context loading (3s vs 101s) and 30% fewer tokens vs manual file reading.

Key differentiators vs simpler memory tools: ticket/issue lifecycle management with blocking/dependency graphs, multi-repo federation via orchestrator nodes, autonomous mode (`/story auto T-001 T-002`) that drives tickets through plan → implement → test → review → commit, and a multi-lens code review system (8 lenses: security, performance, accessibility, etc.).

## How we tested it

Architecture review of the full repo (403 files, 298 TypeScript files, v1.4.4), the 504-line SKILL.md orchestrator, the README, and the self-published session priming comparison document.

```bash
gh api repos/Storybloq/storybloq --jq '.stargazers_count, .license.spdx_id'
gh api repos/Storybloq/storybloq/contents/src/skill/SKILL.md --jq '.content' | base64 -d | wc -l
gh api repos/Storybloq/storybloq/contents/SESSION_PRIMING_COMPARISON.md --jq '.content' | base64 -d
```

Not hands-on tested (no project bootstrap performed). Assessment is architecture-review based.

## What worked

- **Structured project state is the right abstraction.** Tickets, issues, roadmap phases, and handovers are first-class entities with JSON schemas, blocking graphs, and lifecycle states. This is more structured than any other memory tool in the catalog.
- **Federation is unique.** Multi-repo orchestration with `dependsOn`, `links`, and `crossNodeBlockedBy` relationships — no other memory tool addresses cross-repo agent coordination.
- **53 MCP tools give agents fine-grained access** — `storybloq_ticket_next`, `storybloq_lesson_digest`, `storybloq_recommend` are purpose-built for agent workflows, not generic CRUD.
- **Session priming comparison is honest.** The self-benchmark acknowledges weaknesses (MCP path misses RULES.md and commit history) alongside strengths, which builds trust.
- **Autonomous mode with review lenses.** The `/story auto` flow with 8 review lenses (security, performance, accessibility, etc.) is a complete development loop, not just memory.
- **Lean dependency surface.** Only 4 runtime dependencies for a 298-file TypeScript project — no database, no Docker, no cloud service required.

## What didn't work or surprised us

- **PolyForm-Noncommercial license** is a hard constraint. Cannot be used in commercial projects without a separate license. This is a dealbreaker for most professional dev teams.
- **Last commit was May 30, 2026** — 19 days without activity. The repo is young enough that this could be normal cadence or could signal abandonment.
- **504-line SKILL.md is heavily defensive.** The "active session guard" with whitelist semantics, re-trigger rules, and ToolSearch prelude workarounds suggests fragile MCP integration that needed extensive guardrails.
- **All-or-nothing adoption.** The `.story/` directory convention means the whole team needs to adopt storybloq — it's not a personal tool like claude-mem.
- **No hands-on validation.** The session priming benchmark is self-published; independent verification would strengthen the claims.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Structured ticket lifecycle prevents agents from losing track of what's done vs. pending |
| Speed | + | 34x faster context loading (3s vs 101s) per self-benchmark; 30% token reduction |
| Maintainability | + | Handovers and lessons learned create institutional memory |
| Safety | neutral | No security-specific features beyond path safety in review lenses |
| Cost Efficiency | + | Pre-computed MCP summaries reduce token waste on context loading |

## Verdict

**CONDITIONAL**

Use when: (1) your project is non-commercial or you have a commercial license, (2) the whole team can adopt the `.story/` convention, and (3) you need structured project management (tickets, roadmap, federation) integrated into agent sessions — not just memory. For solo Claude Code users who need cross-session memory, claude-mem (ADOPT) is simpler and permissively licensed. For multi-agent teams on commercial projects, engram (CONDITIONAL) is a better fit. Storybloq's federation and autonomous mode are genuinely unique, but the license narrows the audience significantly.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [storybloq](https://github.com/Storybloq/storybloq) | plugin | Cross-session context for Claude Code — CLI + MCP server + /story skill | Claude Code loses context across sessions; tracks tickets, issues, handovers in .story/ | claude-mem, OMEGA, engram |
