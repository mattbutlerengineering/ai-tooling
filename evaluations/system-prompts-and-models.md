# Evaluation: system-prompts-and-models

**Repo:** [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)
**Stars:** 140,892 | **Last updated:** 2026-06-12 | **License:** GPL-3.0
**Dev loop stage:** Discover
**Layer:** Infrastructure

---

## What it does

The single largest and most popular collection of leaked/extracted system prompts and tool definitions from commercial AI coding and assistant products. The repo is a flat set of 34 top-level directories — one per product — each holding the extracted system prompt(s) and, where captured, the tool-call schemas and internal model instructions. Coverage spans the field: Cursor, Devin AI, Windsurf, Replit, v0, Lovable, Manus, Perplexity, Warp.dev, VSCode Agent, Xcode, Google, and an Anthropic directory containing Claude Code 2.0, Claude Sonnet 4.6, and Claude for Chrome prompts, plus an "Open Source prompts" folder. There is no tooling, no spec, no install — it is a reference corpus you read to see how shipping agents are actually prompted: their role framing, tool descriptions, safety rails, formatting conventions, and reasoning scaffolds.

The learning value is comparative: by reading many products' prompts side by side you can see which patterns are convergent (explicit tool-call schemas, anti-laziness instructions, planning preambles) versus product-specific, and lift battle-tested prompt phrasing into your own agents and skills.

## How we tested it

Method: inspected the GitHub repo metadata, README, and file tree only via `gh api`. Did NOT clone the repo or read individual prompt files in full. No hands-on usage is reported — all observations are repo/README-sourced and noted as such.

```bash
gh api repos/x1xhlol/system-prompts-and-models-of-ai-tools \
  --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/x1xhlol/system-prompts-and-models-of-ai-tools/git/trees/main --jq '.tree[].path'
gh api repos/x1xhlol/system-prompts-and-models-of-ai-tools/contents/Anthropic --jq '.[].name'
gh api repos/x1xhlol/system-prompts-and-models-of-ai-tools/commits --jq '.[0].commit.committer.date'
```

Reviewed: top-level directory list (34 product folders), the Anthropic folder contents (Claude Code 2.0, Sonnet 4.6, Claude for Chrome), the README (sponsor/support/security-notice framing, "Latest Update: 10/05/2026"), license, and freshness.

## What worked

- **Breadth is unmatched** — 34 products in one place, far wider than any single-product prompt dump. For comparative study of how agents are prompted, this is the canonical starting corpus.
- **Genuinely fresh** — last commit 2026-06-12 and a self-reported recent update; prompts track current shipping versions (Claude Code 2.0, Sonnet 4.6), not stale 2024 snapshots.
- **High learning value** — reading real production prompts surfaces concrete, copyable patterns (tool-call schema phrasing, planning preambles, refusal framing) that improve your own skills and agent prompts.
- **Enormous social proof** — 140K stars and Trendshift-ranked; it is the de facto reference the ecosystem points at, including tools and wikis that link to it.

## What didn't work or surprised us

- **Not read in depth** — only metadata, README, and the tree were inspected; individual prompt accuracy/completeness was not verified file-by-file.
- **Leaked, not authorized** — these are extracted prompts, not vendor-published. Accuracy, version-pinning, and completeness vary by product and capture date; treat each file as an unverified snapshot, not ground truth.
- **GPL-3.0 on a prompt corpus** — a copyleft license over leaked third-party text is legally murky. Copying prompt text wholesale into your own product carries both IP and license-propagation questions; use it to learn patterns, not to lift verbatim.
- **README is heavily monetized** — crypto donation addresses, Patreon/Ko-fi, paid sponsorship slots, and a "secure your prompts" upsell (ZeroLeaks). The framing is promotional, not scholarly; nothing wrong with it, but set expectations accordingly.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Learning resource; doesn't touch your code. Prompt patterns may improve your own agents indirectly |
| Speed | neutral | A reference corpus; no effect on dev loop speed |
| Maintainability | neutral | Helps you write better prompts; no direct codebase impact |
| Safety | - | Leaked content under copyleft license; lifting prompt text verbatim raises IP/license risk |
| Cost Efficiency | neutral | Free to read; no direct token or cost effect |

## Verdict

**CONDITIONAL**

The most comprehensive, most current, and most-starred leaked-prompt corpus available — high learning value for anyone designing agent prompts, skills, or tool schemas, and worth keeping as a Discover-stage reference. Use it conditionally: as a comparative study aid to learn prompt-engineering patterns across 34 products, not as authoritative documentation (the prompts are unverified leaks) and not as a source to copy text from verbatim (GPL-3.0 over leaked third-party content is legally murky). Within the leaked-prompt cluster it is the widest net: prefer it over [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) (Claude-Code-only, deeper single-product detail) when you want cross-product breadth, and it overlaps closely with [system-prompts-leaks](https://github.com/asgeirtj/system_prompts_leaks) (also broad and regularly updated, spanning more non-coding assistants) — keep both as complementary corpora rather than picking one.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [system-prompts-and-models](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | reference | Largest collection of leaked system prompts and tool defs from 34 AI products (Cursor, Devin, Claude Code, v0, etc.) | Want to learn how shipping AI agents are actually prompted, by comparing real production prompts | claude-code-system-prompts, system-prompts-leaks, learn-claude-code |
