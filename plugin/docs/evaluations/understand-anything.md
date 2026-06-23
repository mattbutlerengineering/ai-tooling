# Evaluation: Understand-Anything

**Repo:** [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)
**Stars:** 63,945 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan (codebase understanding / onboarding before and during implementation)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Turns code into interactive knowledge graphs explorable by humans/agents."

Understand-Anything is a **Claude Code plugin** (also installable on Codex, Cursor, Copilot, Gemini CLI, OpenCode and ~13 other platforms via `install.sh`) that runs a multi-agent batch pipeline over a codebase and emits a knowledge graph plus an interactive web dashboard for a human to explore. The mechanism: `/understand` orchestrates 5 specialized sub-agents — `project-scanner` (discover files, detect languages/frameworks), `file-analyzer` (extract functions/classes/imports into nodes and edges), `architecture-analyzer` (assign layers: API/Service/Data/UI/Utility), `tour-builder` (generate guided learning tours ordered by dependency), and `graph-reviewer` (validate referential integrity). `/understand-domain` adds a 6th (`domain-analyzer`) and `/understand-knowledge` a 7th (`article-analyzer` for Karpathy-pattern LLM wikis). The result is written to `.understand-anything/knowledge-graph.json`.

The engine is a Tree-sitter + LLM hybrid: Tree-sitter deterministically parses source into a CST and extracts structural facts (imports, exports, definitions, call sites, inheritance) — pre-resolved into an `importMap` and used for fingerprint-based change detection — while the LLM produces the semantic layer (plain-English summaries, tags, layer assignments, business-domain mapping, guided tours, language-concept callouts). File analyzers run up to 5 concurrent, 20-30 files per batch.

Consumption is primarily **human-facing**: `/understand-dashboard` opens an interactive web UI (pan/zoom/search/click, color-coded by layer, persona-adaptive detail). Secondary agent-/dev-facing commands exist: `/understand-chat` (ask questions about the codebase), `/understand-diff` (impact analysis of current changes), `/understand-explain <path>` (deep-dive a file/function), `/understand-onboard` (generate an onboarding guide). The graph is plain JSON intended to be committed so teammates skip the pipeline. Updates are **incremental by default** (only changed files re-analyzed via fingerprints), and an optional `/understand --auto-update` installs a post-commit hook to patch the graph on every commit.

## How we tested it

**Evidence:** REVIEW

**Method: inspected the GitHub repo, full README, plugin manifest, recursive file tree, releases, and test layout. Not installed or run hands-on.** No `/understand` pipeline was executed against a real codebase, so no graph-quality, token-cost, or dashboard-UX numbers below are reproduced figures — token-usage and incremental-update claims are the author's. Honesty note per the catalog integrity rule: this is an architecture/maturity review calibrated against `evaluations/codegraph.md` (ADOPT) and `evaluations/code-context-engine.md` (CONDITIONAL).

What was actually inspected:

```
gh api repos/Egonex-AI/Understand-Anything --jq '{stars,license,description,pushed_at,created_at,language,forks}'
# {stars:63945, license:MIT, lang:TypeScript, created:2026-03-15, pushed:2026-06-19, forks:5284}

gh api repos/Egonex-AI/Understand-Anything/readme --jq '.content' | base64 -d        # full README
gh api repos/Egonex-AI/Understand-Anything/releases --jq '.[].tag_name'              # v2.7.3 ... v1.2.0
gh api 'repos/Egonex-AI/Understand-Anything/git/trees/HEAD?recursive=1' --jq '.tree[].path'  # 40+ test files, monorepo
gh api repos/Egonex-AI/Understand-Anything/contents/.claude-plugin/marketplace.json  # plugin manifest
```

Cross-referenced against `evaluations/codegraph.md` (the catalog's ADOPT auto-syncing MCP code-intelligence tool) and the graphify entry it overlaps with.

## What worked

- **Strong traction and maturity for a young repo:** 63.9K stars, 5.3K forks, created 2026-03-15, pushed today, at **v2.7.3** (past 2.0). This is the opposite of a thin repo — it clears the maturity bar comfortably.
- **Real test surface:** 40+ test files across the monorepo (`packages/core`, `packages/dashboard`, per-language extractor tests for go/java/python/rust/php/ruby/kotlin/dart/cpp/csharp), Vitest config, ESLint, CI directory. Not a README-only project.
- **Tree-sitter + LLM hybrid is the right architecture** — deterministic structural edges (reproducible) plus LLM semantics (summaries, layers, domains). Same split codegraph and CCE use; sound.
- **Incremental updates + optional auto-update hook** mitigate the usual batch-tool staleness problem: fingerprint-based change detection re-analyzes only changed files, and `--auto-update` installs a post-commit hook to keep a committed graph fresh.
- **Genuinely distinctive output:** an interactive, persona-adaptive visual dashboard plus guided tours, diff-impact view, and onboarding-guide generation. This is a *human onboarding/comprehension* artifact, which neither codegraph (agent-facing MCP, no viz) nor a typical search index produces.
- **Broad platform reach + commit-and-share model:** one pipeline configures ~17 platforms; the JSON graph commits to the repo so teammates and PR reviewers reuse it without re-running.

## What didn't work or surprised us

- **It is a batch pipeline, not an always-on MCP server.** This is the decisive contrast with codegraph (ADOPT). Understanding is produced by invoking `/understand` (and refreshed incrementally or via a post-commit hook); there is **no MCP server an agent queries live mid-loop** for "who calls this?" / "where's the definition?". The agent-loop ergonomics are weaker — the graph informs humans and on-demand commands (`/understand-chat`, `/understand-explain`), not transparent in-session navigation.
- **First run is token-expensive.** The README itself warns the initial whole-codebase `/understand` "can consume a significant number of tokens on large projects" and recommends a subscription/token plan or a local model. Codegraph's local indexing has no per-token LLM cost for the structural graph.
- **No reproducible cost/quality benchmark in-repo.** Unlike codegraph (16% cost / 58% fewer tool calls) and CCE (published R@10 numbers), there are no committed retrieval/accuracy or savings benchmarks — the value case is qualitative.
- **Overlap with graphify is real on the visualization axis.** Both turn a codebase into an explorable clustered graph (HTML/JSON). Understand-Anything is codebase-specialized (layers, tours, domains, diff-impact, multi-platform plugin); graphify is general-input (code/docs/papers/images) and is the user's own ADOPT-adjacent skill.
- **Primary value is human comprehension, not raising code quality.** Like all code-understanding tools it improves navigation/onboarding; it doesn't directly make the code more correct or maintainable.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Layer/domain/diff-impact views give humans (and `/understand-chat`/`/understand-explain`) structural context, reducing blind edits — but no benchmarked correctness gain |
| Speed | + | Onboarding and "where does X live" comprehension is far faster via the dashboard/tours than reading 200K LOC blind; committed graph lets teammates skip the pipeline |
| Maintainability | neutral | Helps humans understand structure; doesn't change the code itself |
| Safety | neutral | Local-first option (Ollama) for privacy; no specific security tooling, but sends code to an LLM by default |
| Cost Efficiency | - | First-run analyzes the whole codebase via LLM agents and "can consume a significant number of tokens"; incremental runs are cheaper but there's a real upfront LLM cost codegraph doesn't have |

## Verdict

**CONDITIONAL**

Understand-Anything is a mature, well-tested, high-traction (63.9K-star, v2.7.3, MIT) code-comprehension plugin with a genuinely distinctive output: an interactive visual dashboard plus guided tours, domain mapping, diff-impact, and onboarding-guide generation across ~17 platforms. It clears the maturity bar easily — this is not a SKIP-for-thinness case.

**vs codegraph (the key comparison): additive, different shape, not a replacement.** Codegraph is an always-on, auto-syncing **MCP server** agents query live for structural facts during a task (definitions, callers, callees) — invisible, cheap, agent-loop-native, which is why it's ADOPT. Understand-Anything is a **batch pipeline producing a human-facing visual graph** plus on-demand comprehension commands; it has incremental updates and an optional post-commit hook, but no live MCP query surface and a real first-run token cost. They serve different jobs: codegraph makes the *agent* navigate better mid-loop; Understand-Anything helps a *human* (and on-demand the agent) comprehend an unfamiliar codebase and onboard. You could run both.

**Use Understand-Anything when:** you're onboarding to a large/unfamiliar codebase (its stated 200K-LOC use case), you want a shareable committed visual graph for team onboarding/PR review/docs-as-code, or you want guided tours / domain mapping / diff-impact that a search index doesn't produce — and you can absorb the first-run token cost (or point it at a local model). For transparent, always-on, low-cost structural awareness *inside the agent loop*, codegraph remains the default. Re-evaluate toward ADOPT if it adds a live MCP query interface or publishes reproducible cost/quality benchmarks.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | tool | Turns code into interactive knowledge graphs explorable by humans/agents | Onboarding to and comprehending a large unfamiliar codebase is slow when reading code blind | codegraph, graphify, code-context-engine |
