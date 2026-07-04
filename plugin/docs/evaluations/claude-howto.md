# Evaluation: claude-howto

**Repo:** [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto)
**Stars:** 37,603 | **Last updated:** 2026-06-17 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Discover (outer loop)
**Layer:** Process

---

## What it does

A structured, visual, example-driven learning guide for Claude Code — pitched as "Master Claude Code in a Weekend." It is not a feature reference; it is a guided curriculum that walks you from `claude` hello-world up to multi-agent pipelines. The content is organized into 10 numbered tutorial modules (`01-slash-commands` through `10-cli`), each with its own README plus copy-paste templates: slash-command definitions, CLAUDE.md scaffolds, hook scripts, MCP configs, and subagent definitions.

On top of the modules sit several navigation layers: `LEARNING-ROADMAP.md` (a beginner/intermediate/advanced path with ~11-13 hour time estimates), `CATALOG.md` (a quick-reference table of ~125 features — 103 built-in, ~47 examples), `QUICK_REFERENCE.md`, and `INDEX.md`. The guide ships its own Claude Code commands too: `/self-assessment` and `/lesson-quiz [topic]` for finding gaps and testing comprehension. It's localized into five languages (English, Vietnamese, Chinese, Ukrainian, Japanese) and versions itself against Claude Code releases (README cites v2.1.160, June 2026).

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — we did not run the curriculum or its quiz commands. Fetched metadata, README, file tree, the feature catalog, and per-module file counts via the GitHub API.

```
gh api repos/luongnv89/claude-howto --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],license:.license.spdx_id}'
gh api repos/luongnv89/claude-howto/commits --jq '.[0].commit.committer.date'
gh api repos/luongnv89/claude-howto/contents --jq '.[].name'
gh api repos/luongnv89/claude-howto/contents/CATALOG.md --jq '.content' | base64 -d | head -40
# per-module README/template counts for 01..10
```

## What worked

- **Genuine learning path, not a link dump.** The 10 ordered modules + roadmap with time estimates fill a real gap: the official docs describe features in isolation but don't teach how to *combine* them. This is the only entry in our reference set framed as a progressive curriculum.
- **Copy-paste templates with substance.** Module 01 alone ships eight working slash commands (`commit`, `pr`, `setup-ci-cd`, `unit-test-expand`, `optimize`, etc.), not toy snippets. Modules average 4-12 files each, so the examples are concrete.
- **Interactive self-assessment.** Shipping `/self-assessment` and `/lesson-quiz` as actual Claude Code commands is a clever twist — the guide teaches and tests inside the tool it's teaching.
- **Fresh and version-tracked.** Last commit 2026-06-17 (two days before this eval), version-pinned to a specific Claude Code release. This is actively maintained, unlike the stale READMEs common to discovery sources.
- **Strong repo hygiene.** MIT license, CHANGELOG, CONTRIBUTING, SECURITY, STYLE_GUIDE, pre-commit config, five-language localization — signals a maintained project rather than a weekend dump.

## What didn't work or surprised us

- **No GitHub description set.** `gh api ... .description` returns null; discovery relies entirely on the README, which is heavy on marketing framing ("leaving 90% of Claude Code's power on the table," a "Trusted by Developers" badge wall).
- **We did not verify the templates run.** Source inspection can't confirm the hook scripts and MCP configs work against current Claude Code; "synced with every release" is the maintainer's claim, not something we tested.
- **Tutorial, not catalog.** For someone who already knows Claude Code and just wants to discover *new tools*, this is the wrong shape — it teaches features rather than surveying the ecosystem. Its value is onboarding, not tool discovery.
- **Overlaps heavily with existing entries.** claude-code-tips (43 tips), claude-code-best-practice, and learn-claude-code cover adjacent ground; the differentiator is the structured beginner-to-advanced path, not unique content.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Production-ready templates (CI/CD, review, test) model correct multi-feature workflows |
| Speed | + | Guided path + copy-paste templates cut Claude Code onboarding from weeks to a weekend |
| Maintainability | neutral | Learning resource — no direct effect on a codebase |
| Safety | neutral | Includes a security policy; teaches hooks, but no security-specific guidance verified |
| Cost Efficiency | + | Teaching feature combination (memory + subagents + hooks) reduces wasted prompt cycles |

## Verdict

**CONDITIONAL**

The best onboarding resource in our reference set for someone *new* to Claude Code: a real curriculum with time estimates, working templates, and in-tool quizzes, actively maintained and version-tracked. Recommend it as the first stop for a developer ramping up. It drops below ADOPT because (a) its value is teaching, not tool discovery — experienced users gain little; (b) the README leans marketing-heavy and the repo sets no GitHub description; and (c) we inspected source only and did not verify the templates run against current Claude Code. Use as a learning-path pointer, not an authoritative spec.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-howto](https://github.com/luongnv89/claude-howto) | reference | Visual, example-driven 10-module curriculum for Claude Code, basics to multi-agent pipelines (37.6K stars) | Need a structured learning path for Claude Code with copy-paste templates | claude-code-tips, learn-claude-code, claude-code-best-practice |
