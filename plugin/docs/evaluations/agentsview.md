# Evaluation: agentsview

**Repo:** [kenn-io/agentsview](https://github.com/kenn-io/agentsview)
**Stars:** 2,946 | **Last updated:** 2026-06-20 (pushed) | **License:** MIT | **Distribution:** install script, Homebrew cask, desktop app, Docker
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Observability (Reflect / outer loop — see what your agents did and what they cost)
**Layer:** Tooling (single local binary + local SQLite + web UI)

---

## What it does

agentsview is a **local-first browser, search, and cost tracker for AI coding-agent sessions** — "one binary, no accounts, everything local." On first run it discovers sessions from every supported agent on the machine (Claude Code via `~/.claude/projects`, Codex, Forge, and 20+ others), syncs them into a local SQLite database, and serves a web UI at `127.0.0.1:8080`. There's also a desktop app (macOS/Windows) and a published Docker image.

It runs as a managed local server:

```bash
agentsview serve --background   # dashboard keeps running after the prompt returns
agentsview serve status         # is a server running?
agentsview usage daily          # daily cost summary
```

The pitch is unified cross-agent history + analytics + spend in one place, without sending anything to a cloud service.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No binary installed, no sessions synced, no dashboard opened. Behavior and the "20+ agents" / cost-tracking claims come from the repository README and metadata, not observed usage.

```bash
gh api repos/kenn-io/agentsview --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 2.9K, MIT
gh api repos/kenn-io/agentsview/readme --jq '.content' | base64 -d | head -55   # serve/usage commands, SQLite sync, multi-agent discovery
```

## What worked

- **Cross-agent unification.** Most session tools are single-agent (claude-fleet, abtop lean Claude/Codex). agentsview's pitch is one local dashboard across 20+ agents — the breadth is its main differentiator.
- **Genuinely local-first.** SQLite on disk, binds to `127.0.0.1`, no account — the right privacy posture for parsing your own transcripts; mirrors the catalog's other local-first session tools (codeburn, claude-fleet).
- **Low-friction distribution.** Install script, Homebrew cask, desktop app, and Docker image cover most setups; managed `serve` lifecycle (background/status/stop) is convenient.
- **Browse + search + cost in one surface.** Combines history search with token/cost analytics rather than forcing two tools.

## What didn't work or surprised us

- **Crowded local-observability niche in this catalog.** It overlaps codeburn (local cost attribution + waste fixes), claude-fleet (live multi-window triage + ripgrep transcript search), and abtop (real-time TUI monitor). Differentiation is breadth of agent support + a polished web/desktop browse UI, not a unique capability.
- **It's a retrospective browser, not a live orchestrator.** Unlike claude-fleet's working/waiting/stalled triage, agentsview is oriented to searching and analyzing past sessions — complementary to, not a replacement for, live multi-agent monitoring.
- **An always-on local server** (even bound to localhost) is one more daemon to run and update.
- **Cost accuracy is parser-dependent.** Like all log-parsing cost tools, numbers are only as good as its per-agent pricing model; unverified here.
- **Young project (~2.9K stars).** Promising and active (pushed today) but less battle-tested than langfuse-class tooling.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Observability tool — informs, doesn't change agent output. |
| Speed | + | Fast local search/browse over synced SQLite; one place instead of per-agent digging. |
| Maintainability | neutral / + | Surfaces which projects/agents consume effort; adds one local daemon to run. |
| Safety | + | Fully local, no accounts, localhost-bound — transcript data stays on the machine. |
| Cost Efficiency | + | Daily cost summaries and cross-agent spend visibility help catch waste (parser-dependent accuracy). |

## Verdict

**CONDITIONAL** — agentsview is a clean, local-first way to **browse, search, and cost-track sessions across 20+ coding agents from one dashboard**, MIT-licensed with easy install (Homebrew/desktop/Docker). Adopt it if you run many *different* agents (not just Claude Code) and want unified retrospective history + spend without a cloud service. If you're Claude/Codex-only, it overlaps heavily with codeburn (cost + waste fixes) and claude-fleet (live triage + transcript search) — pick by whether you need cross-agent breadth + browse UI (agentsview) vs. waste-finding cost analysis (codeburn) vs. live multi-window orchestration (claude-fleet). Verify its cost numbers against a provider bill before trusting them.

Compared to neighbors: **codeburn** attributes spend and emits ranked waste fixes; **claude-fleet** is a live working/waiting/stalled dashboard with ripgrep transcript search; **abtop** is a real-time TUI monitor. agentsview's distinguishing pitch is **broadest agent coverage (20+) with a search-first web/desktop browse UI plus cost**, oriented to retrospective analysis rather than live monitoring.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentsview](https://github.com/kenn-io/agentsview) | tool | Local-first browse/search + analytics + cost tracking across 20+ coding agents (Claude Code, Codex, …) — one binary, local SQLite, web UI + desktop app | Can't search past sessions or see token spend across many different coding agents in one place | codeburn, claude-fleet, abtop |
