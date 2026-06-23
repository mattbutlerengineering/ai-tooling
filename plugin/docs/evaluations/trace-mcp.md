# Evaluation: trace-mcp

**Repo:** [nikolai-vysotskyi/trace-mcp](https://github.com/nikolai-vysotskyi/trace-mcp)
**Stars:** 88 | **Last updated:** 2026-06-18 (pushed); latest release v1.43.1 (2026-06-16) | **License:** MIT
**Dev loop stage:** Plan / Implement (code understanding before and during a change); touches Review (CI change-impact reports) and Reflect (decision memory)
**Layer:** Tooling (a queryable code-graph index served over MCP)

---

## What it does

Catalog one-liner: *"One tool call replaces ~42 minutes of agent exploration via deep trace-based code understanding."*

Mechanically, trace-mcp builds a **framework-aware, cross-language dependency graph** of a codebase once (tree-sitter symbol extraction → cross-file resolution via PSR-4 / ES modules / Python modules / Vue + Inertia bridges / Blade inheritance / ORM relations → optional LSP enrichment), stores it in `~/.trace-mcp/`, keeps it incrementally fresh via a file watcher, and exposes it through MCP. Instead of the agent issuing dozens of Read/Grep/Glob calls to reconstruct structure every turn, it calls a graph tool once. The headline capability is `get_change_impact` (reverse-dependency blast radius across languages) and `get_task_context` / `get_feature_context` (an "optimal code subgraph" for a described task). Beyond plain symbol lookup, it claims **framework-aware edges** — e.g. it understands that `Inertia::render('Users/Show')` links a PHP controller to a Vue page, that `@Injectable()` creates a DI edge, that `$user->posts()` maps to a `posts` table reconstructed from migrations. It layers on **code-linked decision memory** (mines Claude Code / Codex JSONL session logs for decisions and links them to symbols), **cross-session intelligence** (`get_wake_up`, `plan_turn`, `search_sessions` over FTS5), **security scanning** (OWASP/taint), **subproject/cross-service impact**, **CI/PR change-impact reports**, and the *same engine over markdown vaults* (Obsidian/Logseq — `[[wikilinks]]` become graph edges). It also ships an Electron desktop app with a GPU graph explorer over the same index.

The project advertises 81 framework integrations across ~80 languages and ~170 tools. It self-describes as "the recomputation → reuse layer for AI systems."

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — installed and cloned locally, but NOT run against a live MCP client and NOT benchmarked on a real project.** I shallow-cloned the repo to `/tmp/trace-mcp-eval`, pulled metadata via `gh api`, read the full README, the benchmark estimator source (`src/analytics/benchmark.ts`), the security model (`SECURITY.md`), the Claude Code routing block (`AGENTS.md`), and the PreToolUse guard hook (`hooks/trace-mcp-guard.sh`). I did **not** run `npx trace-mcp benchmark .`, did not wire it into Claude Code, and did not reproduce any token or time figure. Every number below is cited as the **project's own claim**, not a measurement I made.

```bash
gh api repos/nikolai-vysotskyi/trace-mcp --jq '{stars,license,description,pushed_at,created_at}'
# stars 88 · MIT · created 2026-04-03 · pushed 2026-06-18
gh release list -R nikolai-vysotskyi/trace-mcp   # → v1.43.1 latest; releases through v1.41–v1.43 in June
gh api repos/nikolai-vysotskyi/trace-mcp/contributors --jq 'length'   # → 4
npm view trace-mcp version    # → 1.43.1 (published to npm)
gh repo clone nikolai-vysotskyi/trace-mcp -- --depth 1
find tests -name '*.test.ts' | wc -l   # → 624 test files
grep -rni "42 min" .                    # → only one hit: README prose
head -50 hooks/trace-mcp-guard.sh        # enforcement tiers: advisory (default) / strict / off
sed -n '1,15p' src/analytics/benchmark.ts   # "SYNTHETIC ESTIMATOR, not a real measurement harness"
```

## What worked

- **Genuinely mature for an 88-star project.** This is not a thin repo. v1.43.1 on npm, a 144 KB CHANGELOG, 624 test files, CI + CodeQL + Semgrep + OpenSSF Scorecard badges, Dependabot, a security policy with path-traversal / symlink-escape / secret-file exclusion controls, and a release-please pipeline. Maturity is far above the "thin → SKIP" bar.
- **The core idea is sound and matches a real failure mode.** Agents *do* re-read hot files 5–15× per task and re-derive structure every turn. Serving a precomputed graph over MCP is the right architecture, and it's the same bet codegraph (ADOPT) makes.
- **Framework-aware cross-language edges are a real differentiator.** The PHP→Vue (Inertia), DI (`@Injectable()`), and ORM→migration→table reconstruction are capabilities plain symbol-graph tools (and codegraph as described) don't claim. If they work as advertised, `get_change_impact` crossing a PHP/Vue boundary is materially better than grep.
- **Local-first and privacy-respecting.** Index lives in `~/.trace-mcp/`, never inside the repo; ONNX embeddings run offline by default with no API keys; no telemetry; the whole footprint is one deletable directory.
- **Honest benchmark methodology in the source.** `src/analytics/benchmark.ts` openly labels itself a "SYNTHETIC ESTIMATOR, not a real measurement harness" producing "upper-bound estimates," and the README's token table is explicitly the tool's *own* TS/Vue codebase under structured tasks, with "expect 40–50% on mixed production workloads" stated plainly. The transparency is better than most.
- **Real Claude Code integration depth.** `trace-mcp init` wires the MCP client, adds a routing block to CLAUDE.md/AGENTS.md, and (Claude Code only) can install a PreToolUse guard hook and tweakcc system-prompt rewrites. The catalog's most Claude-Code-native code-graph entry.

## What didn't work or surprised us

- **The headline "~42 minutes" is marketing, not a measured or even computed figure.** It appears exactly once, in README prose ("instead of 80 Grep calls and 190 file reads … ~42 minutes of agent exploration"). Nothing in the source derives it — there is no wall-clock model, no `minutes` constant, no time benchmark behind it. It is a rhetorical translation of a synthetic, upper-bound token estimate into human time. Treat it as a slogan, not a metric. (The token tables are at least reproducible via `npx trace-mcp benchmark .`; the minutes claim is not.)
- **Scope sprawl is a risk.** ~170 tools, 81 integrations, 80 languages, decision memory, cross-session intelligence, security scanning, subprojects, CI reports, a desktop app, *and* markdown-vault indexing — from 4 contributors on a 2-month-old repo. Breadth this wide on a young project means per-integration depth/accuracy is unproven and the surface area to maintain is enormous. The 99% token-reduction peaks are self-benchmarks on its own codebase; real-stack accuracy of the framework edges is the open question.
- **The guard hook can hard-block native tools.** Level 3/4 enforcement installs a PreToolUse hook that, in `strict` mode, *denies* Read/Grep/Glob on source files and redirects to trace-mcp. Default is `advisory` (warn, allow), and there are sensible exemptions (offset/limit reads, non-code files, MCP-down fallback) — but a `strict` + stale-index or MCP-down combination is a self-inflicted footgun that can degrade the agent. This is a meaningful behavioral change to the harness, not just a passive index.
- **170 tools is a lot of MCP surface.** Exposing many tools inflates the tool-list context budget and can confuse routing — partly why the project leans so hard on CLAUDE.md routing rules and a guard hook to force usage. A tool you must *coerce* the agent into using is a friction signal.
- **Adoption is still small (88 stars, 4 contributors).** Quality and release cadence are high, but it has not been battle-tested by a large community. Long-term maintenance of this surface area by a tiny team is a bet.
- **Not verified hands-on here.** All capability claims (framework edges, impact accuracy, vault indexing) are from the README and source comments, not reproduced.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (claimed) | Framework-aware cross-language impact analysis and graph-derived task context should reduce wrong-file exploration and missed dependencies; unverified here, and bounded by integration accuracy. |
| Speed | + (claimed) | One `get_task_context` / `get_change_impact` call replaces a chain of ~10 sequential Read/Grep ops — fewer round-trips. The "~42 min saved" framing is a slogan, but the fewer-tool-calls direction is real. |
| Maintainability | + | CI/PR change-impact reports, dead-code/test-gap detection, and decision memory help keep changes scoped and rationale recorded. Adds an external index + guard hook to the toolchain. |
| Safety | neutral / − | Local-first, no telemetry, real path-traversal/symlink/secret controls (good). But the strict-mode guard hook actively denies native tools — a new failure mode if the index is stale or the daemon is down. |
| Cost Efficiency | + (claimed) | Project claims ~40–50% token reduction on mixed workloads (up to 99% on structured calls) from serving precomputed graph slices instead of full reads; self-benchmarked, upper-bound estimator. |

## Verdict

**CONDITIONAL**

trace-mcp is a surprisingly mature, well-engineered, local-first code-graph MCP server whose core thesis — serve a precomputed framework-aware graph instead of letting the agent re-read the repo every turn — is exactly right and well-targeted at the Plan/Implement bottleneck. Its real differentiator over [codegraph](https://github.com/colbymchenry/codegraph) (ADOPT) and [code-context-engine](https://github.com/elara-labs/code-context-engine) is **framework-aware cross-language edges** (PHP↔Vue via Inertia, DI graphs, ORM→migration schema reconstruction) plus code-linked decision memory and deep Claude Code integration. **Adopt it conditionally on framework-heavy, multi-language stacks it explicitly supports** (Laravel/Vue/Inertia, NestJS, Django, Rails, etc.) where those edges pay off — and run `npx trace-mcp benchmark .` on your own repo to see real numbers before committing.

It is **not** an unconditional ADOPT like codegraph because: (1) the headline "~42 minutes" metric is unverified marketing prose with no derivation in the code; (2) it's young (88 stars, 4 contributors, 2 months old) with enormous, unproven scope (~170 tools, 81 integrations); and (3) the strict guard hook is an aggressive harness change that can hard-block native tools — keep it in `advisory` mode. It is **not SKIP**: the repo is substantial, honestly documented (the benchmark code self-labels as a synthetic estimator), MIT-licensed, and the framework-edge capability genuinely extends the catalog. Re-evaluate toward ADOPT once it has broader adoption and a hands-on benchmark on a real polyglot project confirms the framework edges and impact accuracy.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [trace-mcp](https://github.com/nikolai-vysotskyi/trace-mcp) | MCP server | Local-first framework-aware code graph over MCP — cross-language change-impact, task context, and code-linked decision memory in one tool call | Agents recompute structure every turn (re-read/re-grep the repo) and are framework-blind to cross-language edges (PHP↔Vue, DI, ORM→schema) | codegraph, code-context-engine, SocratiCode, gortex, Serena (graph navigation); MemPalace / claude-mem (decision memory) |
