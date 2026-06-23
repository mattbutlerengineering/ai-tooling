# Evaluation: repowise

**Repo:** [repowise-dev/repowise](https://github.com/repowise-dev/repowise)
**Stars:** ~2,460 | **Last updated:** 2026-06-20 | **License:** source-available (repo SPDX returns NOASSERTION)
**Dev loop stage:** Plan (codebase intelligence)
**Layer:** Tooling

---

## What it does

A codebase-intelligence layer "for AI and humans" — it produces both context an AI agent can use and health/risk/ownership signals a team can trust, exposed via MCP.

Per the README it's **five intelligence layers** and **nine MCP tools** covering: code **health scores**, **auto-generated docs**, **git analytics**, **dead-code detection**, ownership, and architectural-decision (ADR) signals — across 15 languages and multi-repo workspaces, installed with one `pip install`. The dual framing is the differentiator: the same analysis that grounds an agent (so it reads what matters) also gives a team trustworthy maintainability/risk metrics. A hosted team tier exists alongside the OSS install.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented layers/tools (health scores, auto-docs, git analytics, dead-code, ownership, ADRs; nine MCP tools; 15 languages; multi-repo). Confirmed the MCP delivery and the AI-context + team-signals dual purpose. License resolves to NOASSERTION via the API — pin terms before commercial reliance. Not run on a live repo, so condition-gated.

```bash
gh api repos/repowise-dev/repowise --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/repowise-dev/repowise/readme --jq '.content' | base64 -d
```

## What worked

- **AI context + human metrics from one layer.** Most tools do agent context (sourcebot/semble) or code health (separate analytics); repowise unifies them via MCP — agents get grounding, teams get health/risk/ownership.
- **Broad, MCP-native.** Nine MCP tools across 15 languages and multi-repo workspaces make it usable by any MCP client with one install.
- **Decision signals (ADRs, ownership).** Surfacing architectural decisions and ownership is unusually high-level for a code-intelligence tool — useful for planning.

## What didn't work or surprised us

- **License unresolved + hosted tier.** NOASSERTION via API and a paid team tier — confirm what the OSS install includes and the license terms.
- **Overlaps sourcebot/codebase-memory-mcp/repomix.** Several tools give agents codebase context; repowise's edge is the health/risk/ownership/ADR signals layered on top.
- **Signal quality unverified.** Health scores and dead-code detection are heuristic; validate accuracy on your repo before trusting the metrics.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Grounds agents in real structure; flags dead code/risk |
| Speed | + | MCP tools give targeted context vs. file-by-file reading |
| Maintainability | + | Health scores, ownership, ADRs surface maintainability signals |
| Safety | neutral | Read/analysis layer; no direct safety effect |
| Cost Efficiency | ✓/$ | OSS install; hosted team tier and large-repo analysis cost |

## Verdict

**CONDITIONAL**

Adopt when you want one MCP layer that both grounds AI agents in your codebase and gives the team trustworthy health/risk/ownership/ADR signals — its dual purpose is the differentiator over context-only tools. Confirm the license and OSS-vs-hosted boundary, and validate the heuristic signals on your repo. Overlaps sourcebot/codebase-memory-mcp for the agent-context half.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [repowise](https://github.com/repowise-dev/repowise) | tool | Codebase-intelligence layer for AI agents and teams (★2.5K; SPDX unverified) — five intelligence layers + nine MCP tools delivering code health scores, auto-docs, git analytics, dead-code detection, ownership, and ADR signals across 15 languages and multi-repo workspaces | Agents lack trustworthy codebase context and teams lack health/risk/ownership signals; want one MCP layer providing both | sourcebot, codebase-memory-mcp, repomix, serena |
