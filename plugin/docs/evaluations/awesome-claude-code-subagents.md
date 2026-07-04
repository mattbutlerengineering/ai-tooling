# Evaluation: awesome-claude-code-subagents

**Repo:** [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
**Stars:** 22,115 | **Created:** 2025-07-30 | **Last commit:** 2026-06-16 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

A curated collection of 154+ Claude Code subagents organized into 10 categories: Core Development, Language Specialists, Infrastructure, Quality & Security, Data & AI, Developer Experience, Specialized Domains, Business & Product, Meta-Orchestration, and Research & Analysis. Unlike a typical link-list awesome repo, this one *ships the agents themselves* — every entry is a full `.md` agent file with `name`, `description`, `tools`, and `model` frontmatter plus a detailed system prompt, stored under `categories/NN-*/`. Language Specialists is the deepest category (31 agents); most others hold ~12.

It doubles as an installable artifact. There's a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) so you can `claude plugin marketplace add VoltAgent/awesome-claude-code-subagents` and install per-category plugins (`voltagent-lang`, `voltagent-infra`, etc.), plus four install paths: interactive `install-agents.sh`, a standalone curl-able installer, and an `agent-installer` meta-agent you drive from inside Claude Code. So it is simultaneously a reference list and a distribution mechanism.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — we did not install the agents. Counted entries per category, read a representative agent file for editorial quality, and checked freshness via the latest commit date.

```
gh api repos/VoltAgent/awesome-claude-code-subagents --jq '{desc,stars,pushed,created,license}'
gh api repos/.../commits --jq '.[0].commit.committer.date'           # 2026-06-16
gh api repos/.../contents/categories --jq '.[].name'                  # 10 categories
gh api repos/.../contents/categories/02-language-specialists --jq '[.[]|select(.name|endswith(".md"))]|length'   # 31
gh api repos/.../contents/categories/02-language-specialists/typescript-pro.md --jq '.content' | base64 -d | head -40
```

## What worked

- **It ships runnable agents, not links.** Each entry is a complete, copy-pasteable agent file with proper Claude Code frontmatter (`name`/`description`/`tools`/`model`). The `description` fields are written in the "Use when..." trigger style that actually drives subagent dispatch — better than most hand-rolled agents.
- **Coherent 10-category taxonomy.** Clean structure mapping to recognizable dev roles, with sensible model assignments (e.g. `typescript-pro` pinned to `sonnet`). Easy to browse and to pull just the slice you need.
- **Multiple low-friction install paths**, including a real plugin marketplace and an in-agent installer — it's a distribution channel, not just a catalog.
- **Fresh.** Last commit 2026-06-16 (three days before this eval), versus the stale-since-April competitor `awesome-claude-code`. Active maintenance.
- **Large mindshare.** 22K stars makes it the de facto reference for "where do I find a ready-made Claude Code subagent."

## What didn't work or surprised us

- **No editorial reviews.** This is the key contrast with `awesome-claude-code`: there are no opinionated, hand-written "why this is good" paragraphs. Each entry is just the agent file and a one-line tagline. You get quantity and structure, not curated judgment about which agents are actually good.
- **Generic, prompt-engineered agent bodies.** The sample (`typescript-pro`) reads as a long aspirational checklist ("100% type coverage", "Test coverage exceeding 90%") rather than battle-tested instructions. Quality is uneven and unverified — these look LLM-generated and aren't independently vetted.
- **Count drift / light marketing.** README headline says "154+" while the repo description says "100+"; the README also carries sponsor banners and "feature your product here" placements. It's a maintained project with a commercial layer (VoltAgent).
- **Scope overlap with our own agent tooling.** Many of these duplicate roles already covered by purpose-built agents in the catalog; value is breadth of starting points, not best-in-class implementations.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference/distribution list — agent quality is uneven and unvetted; doesn't directly guarantee better code |
| Speed | + | Ready-made agents save time vs. authoring subagents from scratch; install in one command |
| Maintainability | neutral | No impact on your codebase |
| Safety | ~ | Agent files declare scoped `tools`, but bodies are unvetted prompts; review before granting broad tool access |
| Cost Efficiency | + | Per-category plugins + sensible model pinning (haiku/sonnet) avoid over-spending; free to adopt |

## Verdict

**CONDITIONAL**

The best *quantity-and-distribution* reference for Claude Code subagents — and, unusually, it ships the agents as installable artifacts rather than just linking out, which neither `awesome-claude-code` nor the `awesome-claude-skills` lists do. Use it as a starting-point library when you need an agent for a role you haven't written yet: pull the relevant `.md`, then review and harden the prompt before trusting it. It lands at CONDITIONAL rather than ADOPT because it lacks the editorial curation that makes `awesome-claude-code` valuable — there's no signal about which of the 154 agents are actually good, the bodies look LLM-generated and unvetted, and there's a sponsor/marketing layer. It complements `awesome-claude-code` (curation-rich, agent-light) rather than replacing it: this one is the agent warehouse, that one is the reviewed catalog.

## Catalog entry

**Target category: Reference**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | reference | 154+ ready-to-install Claude Code subagents in 10 categories, shipped as agent files with frontmatter (22K stars) | Need a ready-made subagent for a dev role without authoring one from scratch | awesome-claude-code, awesome-agent-skills, buildwithclaude |
