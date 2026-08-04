# Evaluation: Ref MCP (ref-tools-mcp)

**Repo:** [ref-tools/ref-tools-mcp](https://github.com/ref-tools/ref-tools-mcp)
**Stars:** 1,132 | **Last updated:** 2026-05-06 (pushed) | **License:** MIT | **Language:** TypeScript (npm: `ref-tools-mcp`)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers (documentation retrieval) — Implement/Verify
**Layer:** Tooling (MCP server; streamable-HTTP recommended, stdio legacy)

---

## What it does

Ref MCP is an MCP server that gives a coding agent **token-efficient access to documentation** for APIs, services, and libraries. Its tools are "designed to match how models search while using as little context as possible to reduce context rot." Two efficiency mechanisms stand out: (1) **session-aware search** — within an MCP session it never returns repeated results, so the agent can page *and* refine its prompt at once; and (2) **fetch-the-part-that-matters** — when reading a doc page it uses the session's search history to drop irrelevant sections and return only the most relevant ~5k tokens, instead of the 20k+ a naive `fetch()` would pull in. Setup is via streamable-HTTP (`https://api.ref.tools/mcp?apiKey=...`, recommended) or a legacy local stdio server (`npx ref-tools-mcp`); both need a Ref API key.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No MCP server connected, no searches issued, token-savings claims not measured.

```bash
gh api repos/ref-tools/ref-tools-mcp --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 1132, MIT, pushed 2026-05-06
gh api repos/ref-tools/ref-tools-mcp/readme --jq '.content' | base64 -d | sed -n '185,275p'        # session filtering, 5k-token fetch, setup
```

## What worked

- **Targets the right cost.** The README quantifies the problem well: 6k tokens of irrelevant doc context can cost ~$0.09/step on Opus, and "more context makes models dumber" (cites the Chroma context-rot research). Returning ~5k relevant tokens instead of 20k+ is a concrete win.
- **Session-aware dedup is a genuinely good idea.** Never repeating results within a session lets the agent page and re-prompt simultaneously — better than blind pagination.
- **Low-friction install.** Streamable-HTTP one-liner, Cursor deeplinks, Smithery badge; works with Claude Code and other MCP clients.
- **Scoped and honest.** It does one thing (docs retrieval, efficiently) and explains the trade-offs rather than overclaiming.

## What didn't work or surprised us

- **API key + hosted backend.** Both transports require a Ref API key against ref.tools; the relevance/dedup logic runs server-side, so this is a paid/managed service, not a self-contained local index.
- **Overlaps context7 head-on.** context7 is the incumbent live-docs MCP; the wedge here is the token-efficiency mechanics (session dedup, 5k-token fetch), not coverage.
- **Effectiveness depends on their search/index quality.** "Most relevant 5k tokens" is only as good as their ranking; unverified here.
- **Slightly staler than the batch.** Pushed 2026-05-06 (vs. same-week pushes for the others) — active but not as hot.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Current, on-target docs reduce API hallucination; grounded snippets beat training-data guesses. |
| Speed | + | Fewer, more-relevant tokens per read; session dedup cuts wasted search round-trips. |
| Maintainability | neutral | One scoped MCP server; no repo state to maintain. |
| Safety | neutral | Sends queries to a hosted API with a key; no special risk but it is an external dependency. |
| Cost Efficiency | + | Core pitch: ~5k vs 20k+ tokens per doc read directly cuts per-step API cost. |

## Verdict

**SKIP** — redundant with [`context7`](https://github.com/upstash/context7), the installed STACK pick for the same job. Both are MCP servers that put current library documentation into an agent's context behind a hosted API key; they occupy one slot, and context7 already holds it (STACK, Tier 1, `KEEP`/`RUN`).

Ref's whole claim to that slot is *efficiency mechanics* — session-aware result dedup and a ~5k-token cap per page — and this evaluation measured none of it (`Evidence: REVIEW`, no server connected, no searches issued). A challenger that ties the incumbent on capability and leads only on an unverified number does not earn a second documentation MCP.

Re-open if context7's page sizes become a measured bottleneck: Ref's per-read cap is the specific fix for that specific problem, and the comparison is then a with/without token delta on a disclosed task set (`evaluations/measurement-protocols.md`) in the P0 measure band — not a bulk pass.

Neighbor placement, unchanged by the skip: **git-mcp** serves live repo source, **pg-aiguide** is a Postgres-specific knowledge layer, **mdn/mcp** covers browser-platform docs. Only context7 competes for the same slot.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ref-tools-mcp](https://github.com/ref-tools/ref-tools-mcp) | MCP server | Token-efficient documentation search for coding agents (MIT) — session-aware search that never repeats results within a session and returns only the most relevant ~5k tokens of a page to fight context rot; streamable-HTTP or stdio | Agents pull 20k+ tokens of mostly-irrelevant docs and get dumber/pricier; want minimal, on-target documentation retrieval | context7, git-mcp, pg-aiguide, mdn/mcp |
