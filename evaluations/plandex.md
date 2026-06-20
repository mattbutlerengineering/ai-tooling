# Evaluation: Plandex

**Repo:** [plandex-ai/plandex](https://github.com/plandex-ai/plandex)
**Stars:** 15,458 | **Last updated:** 2025-10-03 (pushed) | **License:** MIT | **Language:** Go (terminal agent; self-hostable)
**Dev loop stage:** Agent Orchestration / Implement — autonomous terminal coding agent
**Layer:** Tooling/Platform (CLI + self-hostable server)

---

## What it does

Plandex is **an open-source terminal AI coding agent "designed for large projects and real tasks."** Its distinguishing features are aimed at big, multi-file work: a large effective context (it advertises ~2M tokens via smart context management), **multi-file planning**, configurable autonomy levels, and — notably — a **diff-review sandbox**: changes are accumulated in a protected sandbox/branch and you review/apply them rather than the agent editing your files directly. It supports multiple model providers, runs from the terminal, and offers a **local self-hosted mode** plus a hosted option.

## How we tested it

**Source-grounded inspection — not installed, not run.** No project built, no plan executed.

```bash
gh api repos/plandex-ai/plandex --jq '{stars,license:.license.spdx_id,archived,pushed:.pushed_at}'   # 15458, MIT, archived=false, pushed 2025-10-03
gh api repos/plandex-ai/plandex/readme --jq '.content' | base64 -d | head -45                        # large projects, 30s install, self-host
```

## What worked

- **Built for scale, with review gates.** The sandbox/diff-review model (changes staged before they touch your files) is a sane answer to "autonomous agent on a large codebase" — you get autonomy without blind writes. That's a genuine design strength.
- **Large-context, multi-file planning.** Targeting big tasks (not single-file edits) with managed context and explicit plans fits real refactors/features better than chat-edit loops.
- **Self-hostable + model-agnostic.** MIT, local mode, multiple providers — no lock-in.
- **Established and popular.** 15K stars, a recognizable name in the open coding-agent space.

## What didn't work or surprised us

- **Maintenance cadence is the main caveat.** Last push **2025-10** (~8 months before this writing). Not archived and still widely used, but it's not keeping pace with the daily-churn agents (opencode, goose, gemini-cli) — verify it supports current models/features before standardizing.
- **Crowded category.** Open terminal coding agents are plentiful (opencode, goose, OpenHands, aider, grok-cli); Plandex's wedge is large-project handling + the sandbox review model, not novelty.
- **Its own workflow.** The plan/sandbox model is opinionated; teams already on Claude Code/Codex may not switch wholesale.
- **Go server to run for self-host.** Local mode is available but the full experience is a service.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Multi-file planning + sandboxed diff review catch bad changes before they land. |
| Speed | + | Autonomous multi-file execution on large tasks is faster than guiding edit-by-edit. |
| Maintainability | + / neutral | Review-before-apply keeps changes inspectable; the tool's own recent cadence is a watch-item. |
| Safety | + | Changes staged in a protected sandbox/branch — no blind writes to your working tree. |
| Cost Efficiency | neutral | MIT/self-hostable; large-context multi-file runs consume tokens; provider choice controls cost. |

## Verdict

**CONDITIONAL** — Plandex is a well-regarded, MIT **open-source terminal coding agent built for large, multi-file tasks**, and its standout is the **sandboxed diff-review model** that gives you autonomy without letting the agent write blindly to your tree. Adopt it when you want an autonomous agent for big refactors/features with review gates and self-hosting, and you're comfortable with its opinionated plan/sandbox workflow. The real caveat keeping it CONDITIONAL is **maintenance cadence** — the last push is ~8 months old (not archived, but lagging the fast-moving field), so confirm current-model support before committing. In a crowded category (opencode/goose/OpenHands), Plandex's edge is large-project handling + sandbox review.

Compared to neighbors: **opencode**/**goose** are model-agnostic open agents; **OpenHands** is a full AI dev platform; **ralph-claude-code** is an autonomous loop. Plandex's distinguishing pitch is **large-project, multi-file planning with a sandboxed diff-review apply model.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [plandex](https://github.com/plandex-ai/plandex) | platform | Open-source terminal AI coding agent (MIT) built for large projects and real tasks — diff-review sandbox (changes staged in a protected branch before applying), multi-file planning, configurable autonomy, 2M-token effective context, and self-hostable; ⚠️ less actively pushed (mid-2025) | Want an autonomous coding agent that plans and executes large multi-file changes with review gates, not just chat-style edits | opencode, goose, OpenHands, aider-style, ralph-claude-code |
