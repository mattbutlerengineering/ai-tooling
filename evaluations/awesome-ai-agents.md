# Evaluation: awesome-ai-agents

**Repo:** [e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)
**Stars:** 28,393 | **Last commit:** 2025-02-26 | **License:** NOASSERTION
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

A curated landscape of ~215 AI agent products, split into two sections: open-source projects (the bulk, ~200 entries) and closed-source projects and companies. Each entry is a Markdown `<details>` block with a logo/screenshot, a category taxonomy (General purpose, Build your own, Multi-agent, Coding, Research, etc.), a bulleted feature/description list, and a link cluster (docs, GitHub, paper, Discord). It is maintained by the team behind E2B (the code-interpreting sandbox company), and a companion list — [awesome-sdks-for-ai-agents](https://github.com/e2b-dev/awesome-sdks-for-ai-agents) — splits off frameworks/SDKs, so this list is intended to be products and agents only.

The list also exists as a [filterable web UI](https://e2b.dev/ai-agents) and ships a landscape-chart image (`assets/landscape-latest.png`) at the top of the README.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — we did not install or run anything. We pulled metadata, README, last-commit recency, and entry counts via the GitHub API.

```
gh api repos/e2b-dev/awesome-ai-agents --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/e2b-dev/awesome-ai-agents/commits --jq '.[0].commit.committer.date'
gh api repos/e2b-dev/awesome-ai-agents/readme --jq '.content' | base64 -d | head -120
gh api repos/e2b-dev/awesome-ai-agents/readme --jq '.content' | base64 -d | grep -c '^## \['
```

## What worked

- **Breadth.** ~215 distinct agent products is one of the larger curated agent landscapes, spanning research agents, coding agents, autonomous task agents, and vertical/industry agents.
- **Per-entry structure is consistent.** Every entry has the same category/description/links shape, so it scans cleanly and the categories give a usable filtering axis (mirrored in the web UI).
- **Open vs. closed split is useful.** Separating open-source projects from commercial companies is a distinction most awesome-lists skip, and it matters when you're deciding what you can actually self-host.
- **Companion SDK list keeps scope clean.** Frameworks/SDKs are deliberately offloaded to a sibling repo, so this list stays about agents and products rather than turning into a generic LLM-tooling dump.

## What didn't work or surprised us

- **Stale — last commit Feb 26, 2025, ~16 months ago.** The agent landscape turned over heavily in that window (Claude Code, Codex CLI, the MCP ecosystem, the 2025-2026 coding-agent wave). A landscape list frozen in early 2025 is missing most of what matters now.
- **Vendor-anchored.** The README is heavily E2B promotional (Code Interpreter CTAs, "AWS for AI agents" framing). That's fine, but it signals the list is a marketing asset; once E2B's attention moved on, maintenance stopped.
- **README carries a visible TBD backlog.** The HTML comment at the top lists agents queued to be added (Devon, UFO, GPT Swarm, Eidolon, etc.) that were never integrated — a maintenance debt left in the open.
- **No activity/staleness flags.** Unlike awesome-claude-code's CSV, there is no per-entry Active/Stale tracking, so dead or pivoted products are indistinguishable from live ones — and after 16 months, many will be dead.
- **Near-zero Claude Code relevance.** This is an agent-*products* landscape, not a Claude Code resource list. Overlap with our catalog's Claude Code-centric focus is minimal.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference list — no direct effect on code quality |
| Speed | neutral | Breadth helps discovery, but staleness means time wasted on dead entries |
| Maintainability | neutral | No impact on code |
| Safety | − | No activity/license-health flags; stale entries risk pointing at abandoned/unmaintained projects |
| Cost Efficiency | neutral | Web UI filtering is convenient but the underlying data is 16 months old |

## Verdict

**SKIP**

It was a strong agent-landscape reference in 2024, but the last commit was February 2025 and the field has turned over since. With no staleness flags, a visible unmerged backlog, and a vendor-promotional framing that signals abandoned maintenance, it can't be trusted as a current discovery source — and its agent-products focus barely intersects our Claude Code-centric catalog. Prefer live, regularly-updated lists (awesome-claude-code) for discovery. Re-evaluate only if maintenance resumes.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | reference | E2B-curated landscape of ~215 open- and closed-source AI agent products (28.4K stars; stale since Feb 2025) | Hard to survey the AI agent product landscape in one place | awesome-llm-agents (kaushikb11), awesome-claude-code |
