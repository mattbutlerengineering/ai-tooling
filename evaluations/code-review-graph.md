# Evaluation: code-review-graph

**Repo:** [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph)
**Stars:** 18,696 | **Last updated:** 2026-06-14 | **License:** MIT
**Dev loop stage:** Review (primary); Plan (codebase navigation)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Local-first code intelligence graph with blast-radius analysis."

code-review-graph (`crg`) is a Python 3.10+ tool (PyPI `code-review-graph`, currently **v2.3.6**) that parses a repository into an AST with Tree-sitter, stores it as a SQLite graph of nodes (functions, classes, imports) and edges (calls, inheritance, test coverage), and exposes that graph to AI coding agents over **MCP** (30 tools + 5 prompt templates) and a CLI. Its signature capability is **blast-radius analysis**: when a file changes, the graph traces every caller, dependent, and test that the change could affect, so the agent reads only that minimal "review set" instead of re-scanning the whole project.

The mechanism end-to-end: `code-review-graph install` auto-detects installed AI tools (Claude Code, Codex, Cursor, Windsurf, Zed, Continue, OpenCode, Gemini CLI, Qwen, Kiro, Copilot, and more), writes each one's MCP config, and injects graph-aware rules into the platform's instruction files; `build` parses the codebase (~10s for 500 files); then watch mode, editor hooks, or a standalone multi-repo daemon (`crg-daemon`) keep the graph fresh via SHA-256 diffing and incremental re-parse (a 2,900-file repo re-indexes in under 2s). At review time the agent calls tools like `get_impact_radius_tool`, `get_review_context_tool`, `detect_changes_tool` (risk-scored diff → affected functions/flows/test gaps), and `query_graph_tool` (callers/callees/tests/imports/inheritance). The same analysis ships as a composite **GitHub Action** that posts a sticky risk-scored PR comment, with an optional `fail-on-risk` merge gate — built and queried entirely on the CI runner, no source sent externally.

Beyond review it includes a large surplus of analysis features: Leiden community detection, hub/bridge detection via betweenness centrality, surprise scoring (unexpected coupling), knowledge-gap analysis, execution-flow tracing, refactoring tools (rename preview, dead-code detection), wiki generation, a D3.js interactive visualization, exports to GraphML/Neo4j Cypher/Obsidian/SVG, and a multi-repo registry with cross-repo search. Semantic search via vector embeddings is **optional** (sentence-transformers locally, or Gemini/MiniMax/any OpenAI-compatible endpoint) — the core graph is purely structural and needs no external service.

## How we tested it

**Method: inspected the repo, full README, release history, and repo tree via the GitHub API. Not installed or run hands-on.** No `code-review-graph build` was executed and no MCP session was driven. Every metric below (82x median / 528x max token reduction, 0.71 impact F1, build/latency numbers) is the **author's published benchmark**, not a number we reproduced. Per the catalog integrity rule, this is an architecture/maturity review calibrated against the existing codegraph (ADOPT) and code-context-engine (CONDITIONAL) evaluations.

What was actually inspected:

```
gh api repos/tirth8205/code-review-graph --jq '{stars,forks,license,description,pushed_at,created_at,open_issues,language,archived}'
# {stars:18696, forks:2004, license:MIT, lang:Python, created:2026-02-26, pushed:2026-06-14, archived:false, open_issues:143}

gh api repos/tirth8205/code-review-graph/readme --jq '.content' | base64 -d   # full README (650 lines)
gh api repos/tirth8205/code-review-graph/git/trees/main --jq '.tree[].path'   # tests/ hooks/ skills/ docs/ action.yml .mcp.json vscode ext
gh api repos/tirth8205/code-review-graph/releases --jq '.[].tag_name'         # v2.3.6 ... v1.1.0 (28 releases, semver past 1.0)
```

Repo structure confirms maturity: `tests/` directory, CI badge + `.github/workflows/` (ci, eval, pr-review dogfood), a VS Code extension (`code-review-graph-vscode`), a composite GitHub Action (`action.yml`), bundled Claude Code skills (`skills/`) and hooks (`hooks/`), a `docs/` tree with USAGE/COMMANDS/FAQ/REPRODUCING/ROADMAP, 5 translated READMEs, SECURITY.md, CODE_OF_CONDUCT.md, and CONTRIBUTING.md. Findings cross-referenced against `evaluations/codegraph.md` (the catalog's ADOPT structural code-intelligence tool) and `evaluations/code-context-engine.md` (CONDITIONAL semantic peer).

## What worked

- **Mature and active.** 18.7K stars, 2K forks, **28 releases to v2.3.6** (semver well past 1.0), CI, a test suite, a VS Code extension, and a self-dogfooding PR-review workflow. This is the second-most-mature code-intelligence tool in the catalog after codegraph, and far above the typical <500-star entry.
- **Unusually honest benchmarking.** The README leads with caveats most projects bury: the headline "528x" is explicitly labelled the *maximum* (best-case fastapi), the true median is **~82x**; "recall 1.0" is flagged as a **circular, graph-derived upper bound**, not real-world recall, with an honest co-change mode measured alongside. A dedicated "Limitations and known weaknesses" section documents weak search ranking (MRR 0.35), 33% flow-detection recall (Python-only), and the small-single-file-edit case where graph context *exceeds* a naive file read. Deterministic, reproducible benchmarks (pinned SHAs, fixed seeds) with a full recipe in `docs/REPRODUCING.md`.
- **Review-focused, not just navigation.** Unlike codegraph (general structural Q&A) and CCE (semantic retrieval), this tool is purpose-built for the Review stage: blast-radius impact sets, risk-scored `detect_changes`, test-gap detection, affected-flow tracing, and a CI PR-review gate. It targets a dev-loop stage the catalog's other code-graph tools don't directly serve.
- **Local-first and private by default.** Core graph is SQLite in `.code-review-graph/`; zero telemetry, no cloud, no API keys for the structural graph. Cloud embeddings are strictly opt-in with an egress warning (`CRG_ACCEPT_CLOUD_EMBEDDINGS`). The GitHub Action keeps everything on the runner.
- **Broad reach.** ~30+ languages plus Jupyter/Databricks notebooks, custom-language support via a no-fork `languages.toml`, one-command install across 14+ agent platforms, a multi-repo daemon with health checks, and tool-filtering (`--tools` / `CRG_TOOLS`) to trim the 30-tool surface in token-constrained setups.
- **Token-savings transparency.** `context_savings` metadata attaches to review MCP responses and a CLI `--brief` panel, with `--verify` to cross-check estimates against tiktoken (within ~1% of GPT-4 tokens per author calibration).

## What didn't work or surprised us

- **30 MCP tools is a heavy context surface.** Exposing 30 tools (plus 5 prompts) by default consumes meaningful tool-schema tokens in every session and can crowd an agent that already runs several MCP servers. The tool ships `--tools` filtering precisely because of this — but the burden is on the user to configure it, and the default is "all on."
- **Feature sprawl.** Beyond blast-radius review it bundles refactoring, wiki generation, visualization, multi-repo registry, exports, hub/bridge/surprise analysis. Powerful, but the surface area is large for a v2.x single-maintainer project and raises the learning/maintenance cost versus codegraph's tighter scope.
- **Impact "recall 1.0" is circular by the author's own admission** — graded against ground truth derived from the same graph the predictor walks. Real predictive recall (co-change mode) is acknowledged to be "substantially lower" and not yet quoted. The genuinely measured number is the **0.71 average impact F1** with **0.58 precision** (deliberately over-flags to avoid missing a broken dependency).
- **Weak spots are real, not cosmetic:** search ranking is mediocre (MRR 0.35, express queries return 0 hits on module-pattern naming); flow detection is reliable only for Python frameworks (33% recall overall); and for trivial single-file diffs the graph response can be larger than just reading the file.
- **Not installed here**, so MCP wiring with Claude Code, real query latency under a live agent, and the install auto-detection all remain author-claimed rather than verified.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Blast-radius surfaces affected callers/dependents/tests an agent would otherwise miss on grep-and-read; 0.71 impact F1 (over-flags rather than misses) |
| Speed | + | Agent reads the minimal review set instead of re-scanning the repo; sub-2s incremental re-index, sub-ms search latency (author benchmarks) |
| Maintainability | + | Hub/bridge/knowledge-gap/dead-code analysis and risk-scored CI reviews help keep structure and test coverage healthy — more code-health reach than codegraph |
| Safety | + | Local-first, zero telemetry, opt-in cloud embeddings with egress warning; CI Action keeps source on the runner |
| Cost Efficiency | + | Targets review-task input tokens; ~82x median per-question reduction vs whole-corpus baseline (best case 528x); `context_savings` metadata makes savings visible |

## Verdict

**CONDITIONAL**

code-review-graph is a mature (18.7K stars, v2.3.6), local-first, honestly-benchmarked structural code graph with a clear and differentiated specialty — **blast-radius/risk-scored code review** — that the catalog's other code-intelligence tools don't directly target. Its maturity clears the bar that earned codegraph an ADOPT, and its self-aware limitations documentation is a strong trust signal. It falls short of an outright ADOPT on two counts: the 30-tool-by-default MCP surface plus broad feature sprawl make it a heavier, higher-configuration commitment than codegraph's tight always-on model, and its headline accuracy claim ("recall 1.0") is circular by the author's own admission, with real predictive recall unquoted.

**vs codegraph (the key comparison): additive and complementary, not redundant, and not strictly better.** Both build a local structural graph from Tree-sitter ASTs and serve it over MCP, so they overlap on the navigation primitive (callers/callees/imports). But they aim at different dev-loop stages: **codegraph is a tight, auto-syncing always-on graph for the Plan stage** (structural awareness during implementation, invisible integration, minimal tool surface) — the safer daily default. **code-review-graph is a review-stage specialist** (blast-radius impact sets, risk scoring, test-gap detection, a CI PR-review gate) with a much larger optional toolbox. A team that does heavy AI-assisted code review — especially with the GitHub Action as a merge gate — gets capabilities codegraph doesn't offer. Running both is reasonable; running CRG *instead of* codegraph trades a leaner Plan-stage experience for a richer Review-stage one.

**Adopt when:** code review (local or in CI) is a real bottleneck and you want blast-radius/risk analysis on diffs; you're willing to scope the MCP tool surface via `--tools`; and you value local-first privacy. Re-evaluate for ADOPT once co-change recall is published (proving impact accuracy beyond the circular metric), and if the default tool surface is trimmed or auto-scoped per task. **Stick with codegraph alone** if you only need always-on structural navigation during implementation and want the lightest possible footprint.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [code-review-graph](https://github.com/tirth8205/code-review-graph) | tool | Local-first code intelligence graph with blast-radius analysis | AI tools re-read whole codebases on review tasks; a structural graph gives agents the minimal affected file set | codegraph, code-context-engine, graphify, Understand-Anything |
