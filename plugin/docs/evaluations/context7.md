# Evaluation: Context7

**Repo:** [upstash/context7](https://github.com/upstash/context7)
**Stars:** 57,752 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Implement (also Plan — checking current APIs before writing code)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Live documentation lookup — current APIs, not stale training data." Context7 is an MCP server that fetches up-to-date, version-specific documentation and code snippets for a library on demand, so an agent writes against the library's *current* API instead of whatever was in its training cutoff. It exposes two tools: `resolve-library-id` (fuzzy library name → a canonical `/org/project` ID, with ranking signals) and `query-docs` (pull doc chunks + code examples for a resolved ID, scoped to a natural-language question).

## How we tested it

**Evidence:** RUN

Ran it **live** from inside an agent session against a concrete coding question — "how to apply rate limiting to a specific Express route" — to see both the resolution ranking and the doc payload.

```
resolve-library-id { libraryName: "Express", query: "rate limiting specific routes in Express.js" }
query-docs { libraryId: "/express-rate-limit/express-rate-limit", query: "apply a rate limiter to a specific route only" }
```

`resolve-library-id` returned **5 ranked candidates**, each with a Context7 ID, description, **code-snippet count**, **source reputation** (High/Medium), **benchmark score**, and **version list**. The top result was not the literal name match — it surfaced `/express-rate-limit/express-rate-limit` (94 snippets, benchmark 84.43) above the generic `/expressjs/express` (815 snippets) because it was more relevant to the *rate-limiting* intent in the query.

`query-docs` then returned **4 documentation chunks, each with its source GitHub URL**, and they directly contained the answer:

```typescript
// per-path
app.use('/auth', limiter)
// per-endpoint
app.post('/reset_password', limiter, (req, res) => { ... })
```

plus a dynamic per-role-limit example. The snippets used the **current** API (`limit:`, `standardHeaders: 'draft-8'`) rather than the older `max:` option — exactly the "not stale" value proposition.

## What worked

- **Resolution ranks by relevance, not just name match.** For a rate-limiting question it elevated the dedicated `express-rate-limit` middleware over the generic Express framework — the ranking signals (snippet count, source reputation, benchmark score) are exposed so the agent can pick deliberately.
- **Answers are source-cited and current.** Every `query-docs` chunk carried a GitHub source URL, and the code used the library's present-day API/options, which is the whole point versus relying on training-cutoff memory.
- **Version-aware.** `resolve-library-id` returned available versions (`v5.1.0`, `4_21_2`, `v5.2.0`), and `query-docs` accepts a `/org/project/version` ID — so you can pin docs to the version you actually depend on.
- **Two-call ergonomics are tight.** Resolve → query is a fast, low-token loop; the resolve step's guidance caps itself at 3 calls to avoid thrashing.

## What didn't work or surprised us

- **Resolution can be ambiguous and needs judgment.** "Express" returned five entries including three near-duplicate `/websites/expressjs*` mirrors with low benchmark scores (9–46). An agent that blindly takes the first or a high-snippet generic entry could query the wrong source; you have to read the ranking signals.
- **Quality varies by library/source.** Benchmark scores ranged 10–84 across the candidates for one library — coverage and snippet quality are not uniform, so the value depends on whether the specific library is well-indexed.
- **It's a lookup, not a guarantee.** It returns relevant doc chunks for a query, not a single authoritative answer; the agent still has to synthesize the right snippet (here, picking the per-endpoint form over the global `app.use`).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Returned current, source-cited API usage (`limit`/`draft-8`), avoiding stale-training-data mistakes — verified on a live query. |
| Speed | + | Two-call resolve→query loop answered a real API question without leaving the session to browse docs. |
| Maintainability | neutral | Affects how code is written, not the codebase structure. |
| Safety | neutral | Read-only documentation fetch. |
| Cost Efficiency | + | Pulls a few targeted doc chunks instead of an agent guessing then debugging wrong-API output. |

## Verdict

**ADOPT**

Verified hands-on: a live resolve→query loop ranked the correct library for the intent and returned the exact, current, source-cited answer. For any task that touches a third-party library — especially fast-moving ones where training data drifts — this directly moves Correctness by grounding the agent in present-day APIs. The one discipline it demands is reading the resolution ranking signals rather than taking the first hit blindly. Install: `claude mcp add --transport sse context7 https://mcp.context7.com/sse`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [context7](https://github.com/upstash/context7) | MCP server | Live, version-specific library docs + code snippets fetched on demand for the agent | Agents write against stale, training-cutoff APIs and hallucinate options that no longer exist | ref-tools-mcp, mdn-mcp, git-mcp (docs retrieval) |
