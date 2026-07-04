# Evaluation: awesome-llm-agents

**Repo:** [kaushikb11/awesome-llm-agents](https://github.com/kaushikb11/awesome-llm-agents)
**Stars:** 1,514 | **Last commit:** 2026-06-14 | **License:** none
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

A single-section curated list of ~27 LLM agent *frameworks* — CrewAI, LangChain, AutoGen, OpenManus, LlamaIndex, Semantic Kernel, Dify, Haystack, Embedchain, Google ADK, and similar. Each entry is a Markdown bullet with a one-line description, a stats line (stars · forks · contributors · open issues · primary language · license), and 3-5 bullet feature highlights. The README header carries a self-reported "Last updated" date, and the stats appear to be refreshed in bulk (the header date matches the last commit).

Scope is narrow and explicit: frameworks and agent-development tools, not agent products or end-user apps. It is the framework-shaped counterpart to e2b's product-shaped awesome-ai-agents.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — no install or run. We pulled metadata, README, last-commit recency, and entry counts via the GitHub API.

```
gh api repos/kaushikb11/awesome-llm-agents --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/kaushikb11/awesome-llm-agents/commits --jq '.[0].commit.committer.date'
gh api repos/kaushikb11/awesome-llm-agents/readme --jq '.content' | base64 -d | head -120
gh api repos/kaushikb11/awesome-llm-agents/readme --jq '.content' | base64 -d | grep -c '^- \['
```

## What worked

- **Fresh.** Last commit 2026-06-14 (five days before this eval), with a matching self-reported "Last updated" date. That makes it the rare actively-maintained agent list — a sharp contrast to awesome-ai-agents (stale since Feb 2025).
- **Per-entry stats are genuinely useful.** Star/fork/contributor/issue counts and license on each line let you gauge a framework's health and adoption at a glance, without clicking through.
- **Tight, decidable scope.** ~27 entries, all frameworks. It is short enough to read end-to-end and curated rather than exhaustive, which is the right shape for "which agent framework should I reach for."
- **Stats look auto-refreshed.** The counts read as machine-updated in bulk, which explains the freshness and is the right way to keep an awesome-list honest.

## What didn't work or surprised us

- **No license on the repo itself.** The `license` field is null — there is no LICENSE file. For a list others might fork or reuse, that's a gap (ironically, since each entry reports licenses).
- **Frameworks only, and broad ones.** Entries are large general-purpose frameworks (LangChain, CrewAI, AutoGen). Most are already in our catalog by name; the list adds little net-new discovery for a catalog that already tracks the major frameworks.
- **Near-zero Claude Code relevance.** Nothing here is Claude Code-specific — no skills, hooks, slash-commands, or CLAUDE.md patterns. It's a framework directory, orthogonal to our catalog's Claude Code focus.
- **No editorial voice.** Descriptions are functional taglines plus feature bullets, not the opinionated hand-written reviews that make awesome-claude-code valuable. You learn *what* a framework is, not *whether it's good*.
- **Small footprint (1.5K stars).** Modest reach for an awesome-list; coverage is a curated subset, not a comprehensive survey.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference list — no direct effect on code quality |
| Speed | + | Per-entry stats let you compare framework health/adoption fast, without clicking through |
| Maintainability | neutral | No impact on code |
| Safety | + | Reports each framework's license and issue count; freshness reduces dead-link risk |
| Cost Efficiency | neutral | Short and current, but narrow scope limits how often it's the source you reach for |

## Verdict

**CONDITIONAL**

Actively maintained (last update June 2026) and the per-entry health stats are a real, lightweight win when comparing agent frameworks. But scope is narrow — ~27 large frameworks most of which our catalog already tracks — there's no Claude Code relevance, no editorial signal, and no repo license. Use it as a quick "framework landscape with live stats" reference when sizing up agent frameworks; it is not a primary discovery source for our Claude Code-centric catalog. Worth a single catalog row, not adoption into the working stack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-llm-agents](https://github.com/kaushikb11/awesome-llm-agents) | reference | Actively-maintained list of ~27 LLM agent frameworks with live health stats per entry (1.5K stars) | Hard to compare agent-framework maturity/adoption at a glance | awesome-ai-agents (e2b-dev), awesome-claude-code |
