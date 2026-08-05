# Evaluation: Plandex

**Repo:** [plandex-ai/plandex](https://github.com/plandex-ai/plandex)
**Stars:** 15,458 | **Last updated:** 2025-10-03 (pushed) | **License:** MIT | **Language:** Go (terminal agent; self-hostable)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Agent Orchestration / Implement — autonomous terminal coding agent
**Layer:** Tooling/Platform (CLI + self-hostable server)

---

## What it does

Plandex is **an open-source terminal AI coding agent "designed for large projects and real tasks."** Its distinguishing features are aimed at big, multi-file work: a large effective context (it advertises ~2M tokens via smart context management), **multi-file planning**, configurable autonomy levels, and — notably — a **diff-review sandbox**: changes are accumulated in a protected sandbox/branch and you review/apply them rather than the agent editing your files directly. It supports multiple model providers, runs from the terminal, and offers a **local self-hosted mode** plus a hosted option.

## How we tested it

**Evidence:** REVIEW

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

**SKIP** — dormant. Not archived, so this is not a P1 successor-check; the ground is that the eval's
own gating condition has now been checked and comes back negative.

That eval held Plandex at a tentative read with one explicit reservation: "the last push is ~8 months
old (not archived, but lagging the fast-moving field), so **confirm current-model support before
committing**." Confirmed on 2026-08-04:

| Signal | Value |
|--------|-------|
| Last push (any branch) | **2025-10-03** — 10 months |
| Last commit to `main` | **2025-10-03** |
| Last release (`server/v2.2.1`, `cli/v2.2.1`) | **2025-07-16** — 13 months |
| Open issues | 61 |
| Archived | no |

Thirteen months without a release in a category where every other row in this slice was pushed within
the last week (and where model APIs, tool-calling formats and context limits all turned over in that
window) means the reservation is no longer a risk to price — it is a resolved fact. A coding agent
that has not shipped since 2025-07 does not support the models people would run it on.

This is *not* a redundancy SKIP, and that distinction matters: Plandex's differentiator — large
multi-file planning with a **sandboxed diff-review apply model** — is genuinely good and is one of the
better answers in the catalog to "how do I let an agent work autonomously without letting it write
blindly to my tree". Nothing here disputes the design. The row is being retired on maintenance, and if
maintenance resumes the design argument is untouched.

Re-open on any of: a new release, a commit series indicating resumed maintenance, or a maintained fork
carrying the sandboxed-review model forward — the last of which would be worth catalogueing on its own.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [plandex](https://github.com/plandex-ai/plandex) | platform | Open-source terminal AI coding agent (MIT) built for large projects and real tasks — diff-review sandbox (changes staged in a protected branch before applying), multi-file planning, configurable autonomy, 2M-token effective context, and self-hostable; ⚠️ less actively pushed (mid-2025) | Want an autonomous coding agent that plans and executes large multi-file changes with review gates, not just chat-style edits | opencode, goose, OpenHands, aider-style, ralph-claude-code |
