# Evaluation: graphify

**Repo:** [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)
**Stars:** ~74,400 | **Last updated:** 2026-06-17 | **License:** MIT
**Last verified:** 2026-06-29
**Dev loop stage:** Plan / Reflect
**Layer:** Tooling

---

## What it does

Skill that turns any folder of code, SQL schemas, docs, papers, images, or videos into a queryable knowledge graph with community detection. Produces three outputs: interactive HTML visualization, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md. Supports incremental updates, directed graphs, Neo4j export, Obsidian vault generation, and a watch mode for auto-rebuild on file changes.

## How we tested it

**Evidence:** MEASURED

Installed it and ran the **full `/graphify` pipeline** — a verified hands-on run on macOS (arm64), 2026-06-29, against a representative 18-file / **23,645-word** slice of *this repo's own docs* (`WORKFLOW.md`, `STACK.md`, `STACK-LEDGER.md`, 7 evaluations, 2 methodologies, 6 spikes, `TEMPLATE.md`) — a docs-only corpus, which is exactly our use case.

```bash
pip install graphifyy                       # clean install; import graphify OK
# detect → 18 docs, 0 code (AST skipped, semantic-only)
# extract → 1 general-purpose subagent (18 files < 25 chunk size)
# build → cluster → analyze → report → benchmark → HTML
```

Measured outputs from that run:

| Stage | Measured result |
|-------|-----------------|
| Extraction | **54 nodes · 80 edges · 3 hyperedges** |
| Edge honesty audit | **88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS**, avg INFERRED confidence 0.80 |
| Clustering | **10 communities**, cohesion 0.29–0.83 |
| God node | `AI Development Workflow` (degree 13 — the actual hub of WORKFLOW.md) |
| Outputs | `GRAPH_REPORT.md` (7.2 KB), `graph.json` (GraphRAG-ready, 46 KB), `graph.html` (vis-network force layout, 54 KB) |
| Token benchmark | 26.4× reported (caveat below — generic code questions, not doc-tuned) |

The 10 communities mapped to **real, non-overlapping themes** with no bleed (8090 SDLC; document-extraction/PII evals; the dev-loop model; GLM harness routing; Plan→Decompose pipeline; recommended stack; Claude-docs fetching; debugging skills; implement-issue & quality signals; knowledge-graph & markdown-as-source). Cross-document "surprising connections" were genuinely useful rather than noise — e.g. it linked `context7` ≈ `WebFetch platform.claude.com/.md` (two solutions to the same get-current-docs problem in different files) and `8090 Knowledge Graph` ≈ `Open Knowledge Format` (two markdown-document-graph ideas).

*(An earlier draft of this eval claimed a run on a "~15k-line TypeScript project" that was never reproduced and was honestly walked back; the run documented above is the real, reproduced one — a docs corpus, the relevant case for this repo.)*

## What worked

- **Community detection is genuinely accurate on prose.** All 10 clusters were real, non-overlapping doc themes — no bleed between, e.g., the 8090-SDLC cluster and the document-extraction-evals cluster (measured, not assumed).
- **Honest audit trail held up.** 0% AMBIGUOUS, 88% EXTRACTED with confidence_score on every edge; the report tells you which edges are model-inferred and flags the node with the most INFERRED edges for verification.
- **Surprising-connections feature earned its name** — it surfaced cross-file conceptual links a reader wouldn't query for directly (context7 ≈ WebFetch-`.md`; 8090-KG ≈ OKF), which is the stated point of the tool.
- **Three clean outputs land on disk**: a human-readable `GRAPH_REPORT.md`, a GraphRAG-ready `graph.json`, and an interactive vis-network `graph.html`. Persistent — survives across sessions.
- **MIT, ~74K stars, active** — clears the permissive-OSS adoption bar with high maintenance confidence.

## What didn't work or surprised us

- **graphify's own report flagged the corpus as graph-optional:** *"~23,645 words — fits in a single context window. You may not need a graph."* Honest, and correct — at this size the value is persistent cross-document *structure*, not context savings.
- **The token-reduction benchmark is code-shaped and misleading on docs.** Its fixed questions ("how does authentication work", "what is the main entry point") don't apply to a docs corpus, so the 26.4× headline isn't meaningful here. Treat the multiplier as unverified for prose.
- **Token cost of extraction wasn't self-reported** (`token_cost` logged 0/0) — the semantic subagent burned ~132K tokens that the graph's own accounting didn't capture, so the `$` cost is real but invisible in the output.
- **Requires dispatching a general-purpose subagent** for semantic extraction (docs/non-code) — a read-only agent silently drops results. Not a one-shot CLI call.
- HTML is for humans; agents can't "see" it (the `graph.json` / `--wiki` / `--mcp` paths are the agent-facing surfaces).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Structural understanding prevents touching the wrong modules |
| Speed | neutral | Upfront time cost offsets ongoing navigation savings |
| Maintainability | + | Wiki and graph outputs help onboarding |
| Safety | neutral | No security impact |
| Cost Efficiency | - | Deep mode burns significant tokens on extraction |

## Verdict

**CONDITIONAL** (measured)

Adopt for **cross-document discovery and onboarding** — the measured run proved community detection and the surprising-connections feature work accurately on *prose*, not just code, with an honest EXTRACTED/INFERRED audit trail. That makes it a real fit for *this* documentation repo's "what's connected that I didn't know about" question, and the best of the knowledge-graph skills evaluated for docs specifically (vs. codegraph/Understand-Anything, which are code-AST-oriented). **Conditions:** (1) it's graph-*optional* below ~single-context-window size — graphify says so itself — so the payoff is on the full corpus, not small slices; (2) the headline token-reduction benchmark is code-shaped and unverified for prose; (3) extraction burns real, un-self-reported subagent tokens, so budget the `$` cost. For ongoing *code* structural awareness during development, codegraph's always-on MCP approach remains more practical; reach for graphify when the artifacts are diverse (docs + code + images) or the goal is cross-document insight.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [graphify](https://github.com/Graphify-Labs/graphify) | skill | Turns code, SQL, docs, images, or videos into queryable knowledge graphs | Need to convert diverse artifacts into navigable structure | codegraph, Understand-Anything |
