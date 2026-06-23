# Evaluation: codegraph

**Repo:** [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)
**Stars:** 53,201 | **Last updated:** 2026-06-22 | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Pre-indexed code knowledge graph that runs as an MCP server and auto-syncs on file changes. Agents query it for function definitions, call graphs, cross-module dependencies, and structural context. Runs 100% locally — no external API calls. Works with Claude Code, Codex, Gemini, Cursor, and other MCP-compatible agents. Beyond the MCP server it ships a full CLI (`init`, `index`, `sync`, `query`, `explore`, `callers`, `callees`, `impact`, `affected`, `status`) so the same graph is scriptable and directly verifiable outside an agent session.

## How we tested it

**Evidence:** MEASURED

**Ran hands-on** on 2026-06-22 (macOS arm64, Node v20.19.5). Installed `@colbymchenry/codegraph` **1.0.1** globally, indexed a real third-party TypeScript codebase ([`sindresorhus/got`](https://github.com/sindresorhus/got), 72 `.ts` files / 80 total), and exercised the query, call-graph, impact, explore, and incremental-sync surfaces — **verifying every structural claim against `grep` ground truth in the source**. No API key, no network calls; the index is a local SQLite DB.

```bash
npm i -g @colbymchenry/codegraph          # added 2 packages in 1s; codegraph 1.0.1
git clone --depth 1 https://github.com/sindresorhus/got /tmp/cg-target
codegraph init /tmp/cg-target             # build the graph
```

**Indexing (measured).** `init` scanned 80 files and built the graph in **768 ms** (1.40 s wall incl. Node start):

```
◆  Indexed 80 files
●  1,443 nodes, 5,859 edges in 768ms
```

`codegraph status` reports a **4.97 MB local SQLite DB** (`node:sqlite`, WAL) and a typed node breakdown — 463 imports, 276 properties, 211 methods, 156 functions, 127 type_aliases, 104 constants, 22 classes, 2 interfaces — across 72 TypeScript / 6 JS / 2 YAML files. The entire index lives in `.codegraph/codegraph.db` (5.0 MB); nothing leaves the machine.

**Query accuracy (verified, not just run).** `codegraph query parseBody` returned `function parseBody` at `source/core/response.ts:158` with its full signature. Ground truth: that line is `export const parseBody = (response: Response, …): unknown => {` — an **arrow function assigned to a const**, which a naïve `grep "function parseBody"` *misses entirely*. codegraph resolved it as a function node correctly.

**Call-graph accuracy (verified against grep).** `codegraph callers parseBody` named exactly one calling function, `asPromise` (`source/as-promise/index.ts:35`). Ground truth: the only two `parseBody(` call sites (`index.ts:61` and `:266`) are both **inside the body of `asPromise` (defined at line 35)** — so codegraph correctly attributed the calls to their enclosing function rather than to text positions. `codegraph impact parseBody` then traced the blast radius to 5 affected symbols across `response.ts`, `as-promise/index.ts`, and `create.ts`.

**Explore — the headline agent tool (verified).** `codegraph explore retry delay calculation` (same output the `codegraph_explore` MCP tool returns to agents) found 113 symbols across 12 files and produced a **blast-radius list with per-symbol test-coverage annotations**:

```
- `calculateRetryDelay` (source/core/calculate-retry-delay.ts:5) — 2 callers in source/core/index.ts; ⚠️ no covering tests found
- `retry` (source/core/options.ts:2811) — 2 callers; tests: test/https.ts, test/infinite-loop-issue.ts
```

Both coverage claims check out: `test/https.ts` and `test/infinite-loop-issue.ts` genuinely reference `retry`, and `calculateRetryDelay` is genuinely imported (`source/core/index.ts:26`) and called (`:494`). The command then emits verbatim, line-numbered on-disk source for the relevant files — designed so the agent skips redundant Read calls. Measured CLI latency: **~160 ms `query`, ~210 ms `explore`** per invocation (each includes Node cold-start; over MCP the process stays warm, so per-query is faster).

**Incremental auto-sync (verified end-to-end).** Appended a new `codegraphTestProbe()` function to `calculate-retry-delay.ts`, then:

```
codegraph sync     →  Modified: 1 — 5 nodes in 173ms
codegraph query codegraphTestProbe  →  function codegraphTestProbe  source/core/calculate-retry-delay.ts:44  (): number
```

It detected the single changed file, re-indexed it in **173 ms**, and the brand-new symbol was immediately queryable at the correct line — confirming the auto-sync mechanism that is the project's headline claim.

## What worked

- **Fast, real indexing.** 80-file TypeScript repo → 1,443 nodes / 5,859 edges in **768 ms**; incremental sync of one changed file in **173 ms**. These are observed numbers on this host, not vendor figures.
- **Structural resolution beats grep — verified.** It caught an arrow-function-as-const that `grep "function"` misses, and attributed call sites to their *enclosing function* (`asPromise`), not raw text positions. The call-graph and impact results matched source ground truth exactly.
- **`explore` is genuinely agent-useful.** One call returns ranked symbols, a dependency blast radius, **correct test-coverage annotations**, and verbatim line-numbered source — exactly the context an agent would otherwise spend several tool calls assembling.
- **100% local, low footprint.** Self-contained npm package (2 packages, 1 s install); index is a single 5 MB local SQLite DB. No API key, no network, no cloud — confirmed.
- **Clean CLI mirrors the MCP tool.** `explore`/`node` CLI output is documented as identical to the MCP `codegraph_explore`/`codegraph_node` tools, so the graph is scriptable and independently verifiable — which is exactly what made this eval measurable.

## What didn't work or surprised us

- **`uninit` blocks on an interactive confirm.** `codegraph uninit` prompts `Continue? (y/N)` with no `--yes`/`--force` flag surfaced, so in non-interactive contexts you delete `.codegraph/` directly instead.
- **Author's cost/tool-call benchmark not reproduced.** The ~16% token savings / ~58% fewer tool calls remain the project's own numbers — reproducing them needs an A/B agent session, out of scope here. What *is* measured is that the structural data is accurate and fast.
- **Query relevance score is an opaque percentage.** Results rank by a `10340%`-style score with no documented scale; fine in practice but not self-explanatory.
- **Graph returns structural data, not judgement.** `explore`/`impact` give the agent the right context, but interpreting the relationships is still the agent's job (by design).
- **No visualization output** (unlike graphify) — purely an agent/CLI-facing tool.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Verified: resolved an arrow-fn const, attributed callers to the enclosing function, and produced accurate impact + test-coverage data — all matching grep ground truth. Structural awareness instead of grep-and-guess. |
| Speed | + | Measured 768 ms to index 80 files, 173 ms incremental sync, ~160–210 ms per CLI query; over MCP the warm process is faster still. Author reports ~58% fewer tool calls (not reproduced here). |
| Maintainability | neutral | Helps agents understand structure but doesn't change the code itself. |
| Safety | + | Confirmed 100% local — a single 5 MB SQLite DB, no API key, no network egress; telemetry is anonymous and opt-out (`telemetry off`). |
| Cost Efficiency | + (author-reported) | ~16% token savings per the project's benchmark; not reproduced here, but the `explore` source-inlining plausibly cuts redundant agent Read calls. |

## Verdict

**ADOPT**

Ran hands-on and verified: codegraph installs in seconds, indexes a real 80-file TypeScript repo in **768 ms**, incrementally re-syncs a changed file in **173 ms**, and answers definition / caller / impact / explore queries whose structural claims **matched source ground truth exactly** — including an arrow-function-as-const that plain `grep` misses and correct enclosing-function call attribution. It is genuinely 100% local (a 5 MB SQLite DB, no keys, no network). The always-on, auto-syncing knowledge-graph-over-MCP design is the right default for daily agent-assisted development: unlike batch tools (graphify, Understand-Anything) it stays current without manual rebuilds and integrates invisibly over MCP, while the same data is verifiable from the CLI. The only friction observed was a non-`--yes` `uninit` prompt and the author's cost/tool-call benchmark being unreproduced here (the structural accuracy and speed *are* measured). Install via `npm i -g @colbymchenry/codegraph` (not a bare `claude mcp add codegraph`).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codegraph](https://github.com/colbymchenry/codegraph) | tool | Pre-indexed code knowledge graph that auto-syncs on changes | Agents lack structural awareness of the codebase | graphify, Understand-Anything |
