# Evaluation: Sourcebot

**Repo:** [sourcebot-dev/sourcebot](https://github.com/sourcebot-dev/sourcebot)
**Stars:** 3,524 | **Last updated:** 2026-06-20 (pushed) | **License:** see repo (no SPDX detected; self-hostable) | **Language:** TypeScript (self-hosted web app)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Code Understanding — search, navigation, NL Q&A across repos
**Layer:** Infrastructure (self-hosted server; humans + agents)

---

## What it does

Sourcebot is **a self-hosted tool that helps you understand your codebase** — for humans *and* agents. Three pillars: **Code Search** (blazing-fast search/navigation across all repos and branches on any host, with regex, repo/language filters, and boolean logic), **Code Navigation** (IDE-level goto-definition and find-references across all repos), and **Ask Sourcebot** (ask complex questions in natural language; a reasoning model uses Sourcebot's search + code-nav to answer with **inline citations** and navigable snippets). There's a public demo at app.sourcebot.dev; it's designed to be self-hosted across many repos/code hosts.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No instance deployed, no repos indexed.

```bash
gh api repos/sourcebot-dev/sourcebot --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 3524, NOASSERTION, pushed 2026-06-20
gh api repos/sourcebot-dev/sourcebot/readme --jq '.content' | base64 -d | head -30               # code search/nav, Ask Sourcebot w/ citations
```

## What worked

- **Search + nav + grounded Q&A in one self-hosted place.** Most tools do one; Sourcebot combines fast multi-repo search, IDE-grade navigation, and citation-grounded NL answers — useful for both humans browsing and agents retrieving.
- **Cited, navigable answers.** "Ask Sourcebot" answering with inline citations and goto-able snippets is the right shape for trustworthy code Q&A (no ungrounded hallucination).
- **Cross-repo, cross-host.** Search/nav across *all* repos and branches regardless of where they're hosted is a real org-scale strength that single-repo tools lack.
- **Self-hosted.** Keeps code on your infra; org-wide deployment model.
- **Active + try-before-deploy.** Daily pushes and a public demo lower evaluation friction.

## What didn't work or surprised us

- **License undeclared (NOASSERTION).** No standard SPDX detected — Sourcebot has historically used a non-OSI license for parts; confirm terms (and any feature gating) before relying on it commercially.
- **Server to run.** It's a self-hosted web app indexing many repos — real infra to deploy and maintain, vs. a single-binary CLI/MCP.
- **Agent integration depth.** "For agents" is in the framing, but the primary surface is a human web app + Ask; how cleanly agents consume it (MCP? API?) matters and isn't exercised here.
- **Crowded code-understanding niche.** Overlaps serena, claude-context, sem, code-context-engine; the wedge is org-scale multi-repo search + cited Q&A as a self-hosted product.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Citation-grounded answers + IDE-grade nav reduce wrong assumptions about code across many repos. |
| Speed | + | Fast multi-repo/branch search beats grepping each repo; NL Q&A shortcuts exploration. |
| Maintainability | neutral | Org-wide cited search aids onboarding/archaeology; a server to operate is overhead. |
| Safety | + | Self-hosted keeps code on your infra. |
| Cost Efficiency | neutral | Free to self-host (license caveat); running the indexing server is infra cost. |

## Verdict

**CONDITIONAL** — Sourcebot is a strong **self-hosted, org-scale code-understanding platform** that unifies fast multi-repo search, IDE-grade navigation, and **citation-grounded natural-language Q&A** ("Ask Sourcebot") for both humans and agents. Adopt it when your team has many repos across hosts and wants one self-hosted place for cross-repo search and trustworthy, cited code answers — onboarding, archaeology, and agent retrieval all benefit. It's CONDITIONAL because the license isn't a standard SPDX (verify terms/feature gating), it's a server to operate, and the agent-consumption path needs confirming for your stack. Against single-repo tools (serena, sem), Sourcebot's edge is org-wide reach + cited Q&A.

Compared to neighbors: **serena** does LSP symbol-level edit/find within a project; **claude-context** is embedding search via Milvus; **sem** is entity-level diffs; **code-context-engine** indexes one codebase. Sourcebot's distinguishing pitch is **self-hosted, cross-repo search + navigation + citation-grounded NL Q&A for humans and agents.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sourcebot](https://github.com/sourcebot-dev/sourcebot) | platform | Self-hosted code understanding for humans + agents — blazing code search/navigation (regex, repo/language filters, goto-def/find-refs) across all repos/branches/hosts, plus "Ask Sourcebot" natural-language Q&A grounded with inline citations | Teams and agents need fast, cited search and IDE-grade navigation across many repos, self-hosted | serena, claude-context, sem, code-context-engine |
