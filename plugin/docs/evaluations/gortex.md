# Evaluation: gortex

**Repo:** [zzet/gortex](https://github.com/zzet/gortex)
**Stars:** 642 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Dev loop stage:** Plan (primary: structural navigation during implementation); Review (PR triage, blast radius, line-anchored findings)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "High-performance code-intelligence engine supporting 257 languages — CLI, MCP."

gortex is a single static Go binary (Apache-2.0, by Andrey Kumanyaev / `zzet`) that indexes one or many repositories into a persistent, in-memory knowledge graph of functions, classes, call chains, HTTP routes, and cross-service contracts, then exposes that graph to AI coding agents over an MCP server, an HTTP `/v1/*` API, and a CLI. The design goal is the same as codegraph and code-review-graph: let an agent ask the graph for exactly the symbols/relationships it needs instead of grep-and-read across whole files, cutting input tokens (project claims "up to 50x fewer tokens per response").

The 257-language claim is tiered, not uniform: a core set (Python, TS/JS, PHP, C#, Go, C/C++, Java, Kotlin, Swift, Zig, Rust, Ruby, Elixir, OCaml, Haskell, and more) gets bespoke tree-sitter extractors plus "compiler-grade" in-process resolvers (LSP-style symbol resolution); a second tier uses tree-sitter ASTs; and the long tail falls back to regex and "forest-backed signatures." So "257 languages" means *reachable/indexable* via tree-sitter grammars with a strong confidence/provenance model on top — full call-graph resolution only holds for the bespoke-resolver core. Notebooks (Jupyter, Databricks) are also handled.

Architecturally it runs as a long-living Unix-socket daemon: one process serves every IDE/agent window, watches the filesystem via fsnotify, persists a gob+gzip snapshot, and supports per-session isolation. Distinctive features beyond codegraph's tight navigation graph: a precomputed depth-3 reach index for O(seeds x reach) blast-radius queries; cross-repo API contract detection (HTTP/gRPC/GraphQL/Kafka/WebSocket/env-var/OpenAPI/Temporal) normalized to canonical IDs and matched provider-to-consumer across repo boundaries; speculative execution (`preview_edit`, `simulate_chain`) that answers "what would change if I applied this WorkspaceEdit" without touching disk; live editor overlays (unsaved-buffer shadow graph); a custom GCX1 wire format claimed to save a further ~27% tokens vs JSON; PR review tooling (`gortex prs`, `gortex review` with BLOCK/REVIEW/APPROVE verdicts); and a Next.js Web UI with 3D force-directed graph views. Semantic search is on by default via an embedded 3.8 MB GloVe model (hybrid BM25 + vector + RRF), with opt-in MiniLM/Ollama/OpenAI. `gortex install` auto-detects and configures 16 coding agents (Claude Code, Cursor, Windsurf, Copilot, Continue, Cline, OpenCode, Codex CLI, Gemini CLI, Zed, Aider, and more).

## How we tested it

**Method: inspected the repo via the GitHub API — repo metadata, the full README, the BENCHMARK.md surface, release/tag history, contributor count, and the top-level repo tree. Not installed, not built, no MCP session driven.** Per the catalog integrity rule this is an architecture/maturity review calibrated against the existing codegraph (ADOPT) and code-review-graph (CONDITIONAL) evaluations. Every performance number below is the **project's own published benchmark on a single operator's machine** (the README and BENCHMARK.md both say so explicitly), not a figure reproduced here.

What was actually inspected:

```
gh api repos/zzet/gortex --jq '{stars,forks,license,description,pushed_at,created_at,language,archived,open_issues}'
# stars:642, forks:49, license:Apache-2.0, lang:Go, created:2026-04-06, pushed:2026-06-18,
# archived:false, open_issues:14

gh api repos/zzet/gortex/readme --jq '.content' | base64 -d         # full README
gh api repos/zzet/gortex/contents/BENCHMARK.md --jq '.content' | base64 -d   # 5 benchmark surfaces
gh api repos/zzet/gortex/git/trees/main --jq '.tree[].path'         # cmd/ internal/ pkg/ docs/ eval/ bench/ examples/
gh api repos/zzet/gortex/releases --jq '.[].tag_name' | wc -l       # 30 releases, v0.1.0 -> v0.48.0
gh api repos/zzet/gortex/contributors --jq 'length'                 # 6 contributors
```

Repo structure indicates real engineering rigor: a CI workflow, `make test` running `go test -race ./...`, `golangci-lint`, separate `bench/` and `eval/` trees, a `docs/04-evaluation/` methodology directory, SECURITY.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md, THIRD_PARTY_NOTICES.md, and a notably strong supply-chain posture (Sigstore/cosign-signed releases, SLSA Level 3 build provenance, OpenSSF Scorecard badge, VirusTotal 0/91). BENCHMARK.md documents five reproducible benchmark surfaces, each with a headline number, a published table, a "How to reproduce" block, and an update protocol.

## What worked

- **Strong supply-chain and security posture** — Sigstore-signed binaries, SLSA L3 provenance, OpenSSF Scorecard, VirusTotal clean. Install verifies SHA256 + cosign. This exceeds every other code-intelligence tool in the catalog on supply-chain hardening and is a meaningful trust signal for a binary you run as a daemon over all your repos.
- **Honest benchmarking discipline.** BENCHMARK.md states plainly the numbers "come from a single operator's machine" and "reproducing them on your hardware will yield different absolute timings." It documents the offline-verifiable fixture path separately from the network-dependent full run, and ships reproduction recipes per surface. The token-savings claim is exposed live via `gortex savings` (per-call/session/cumulative, priced in USD) rather than asserted once.
- **Differentiated feature set vs the catalog's existing graph tools** — cross-repo API contract detection (8 contract types matched provider-to-consumer), speculative edit simulation without touching disk, live unsaved-buffer overlays, and a published round-trippable wire format (GCX1) are capabilities neither codegraph nor code-review-graph offers.
- **Operationally serious** — long-living daemon serving every IDE window, fsnotify live updates, on-disk snapshots, per-session isolation, OS-supervised lifecycle. Single static binary, zero runtime deps, cross-platform (macOS/Linux/Windows), one-command install configuring 16 agents.
- **Local-first and private by default** — everything in-process, no network or model download to start (embedded 3.8 MB GloVe); telemetry off by default, opt-in only, honours `DO_NOT_TRACK`.
- **Active and versioned** — 30 releases from v0.1.0 to v0.48.0 in ~2.5 months, CI + race-tested test suite, dedicated `eval/` and `bench/` trees.

## What didn't work or surprised us

- **Low maturity by star/adoption signal.** 642 stars, 49 forks, 6 contributors, repo created 2026-04-06. That is roughly 1/30th of code-review-graph's adoption (18.7K) and a fraction of codegraph's (51K). The engineering looks more mature than the numbers, but field-tested-at-scale evidence and community validation are thin.
- **Pre-1.0 and single-maintainer-dominated.** Versioning is still v0.x (48 minor releases, no 1.0), 6 contributors with one clearly dominant author. API/graph-schema stability and bus factor are open risks for something you'd wire into 16 agents as a daemon.
- **175 (configurable) / "100+" MCP tools is a very heavy context surface** — even larger than code-review-graph's 30, which the catalog flagged as a concern. The README emphasizes "use only what you need," so per-task tool filtering is essential, not optional; the burden is on the user to scope it.
- **Headline claims are project claims, unverified here.** "Up to 50x fewer tokens," "−27% vs JSON" (GCX1), the depth-3 O(seeds x reach) blast-radius perf, and the linux/vscode index throughput all come from the author's machine. The BENCHMARK.md "How to reproduce" full run requires network to clone reference repos; only an in-tree nestjs fixture is offline-verifiable.
- **Requires CGO (Go 1.26+) to build from source** for the tree-sitter C bindings — fine for the prebuilt binary, a friction point for from-source users or locked-down environments.
- **Feature sprawl** — contracts, speculative execution, overlays, PR review, Web UI with 3D graph modes, 9 optional LLM providers, custom wire format. Powerful, but a large surface for a v0.x project to keep stable.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Provenance-tiered graph with confidence model + compiler-grade resolvers for core languages; cross-repo contract matching surfaces orphan providers/consumers and mismatches an agent would otherwise miss (project claims) |
| Speed | + | Precomputed depth-3 reach index makes blast-radius O(seeds x reach); daemon + fsnotify keeps the graph live; sub-ms impact p95 on fixture (author benchmark) |
| Maintainability | + | `verify_change`/`check_guards`/`audit_agent_config` flag broken callers, guard violations, stale docs; PR review with BLOCK/REVIEW/APPROVE verdicts adds review-stage reach |
| Safety | + | Strongest supply-chain posture in the category (Sigstore + SLSA L3 + Scorecard + VirusTotal); local-first, telemetry off by default, honours DO_NOT_TRACK |
| Cost Efficiency | + | Graph-native lookups vs full-file reads; "up to 50x" + GCX1 −27% (project claims); `gortex savings` exposes realized token/USD savings live |

## Verdict

**CONDITIONAL**

gortex is an impressively engineered, local-first, Apache-2.0 code-intelligence engine that is in several respects *more* ambitious than the catalog's existing graph tools — cross-repo API contract matching, speculative edit simulation, live editor overlays, a published wire format, and a best-in-category supply-chain posture (Sigstore + SLSA L3). The benchmarking discipline and security hygiene are genuine trust signals. It falls short of an outright ADOPT on the one axis that has been decisive for this category: **maturity and adoption**. At 642 stars / 6 contributors / pre-1.0 (v0.48.0) on a ~2.5-month-old repo, it has neither codegraph's proven always-on simplicity nor code-review-graph's community validation, and its "100+/175 MCP tools" default is an even heavier context surface than the one already flagged on code-review-graph. All headline metrics remain author-claimed, not reproduced.

**vs codegraph (ADOPT, the daily-driver structural graph) and code-review-graph (CONDITIONAL, the review specialist): additive in capability, not yet additive enough in trust.** gortex overlaps the same navigation primitive (Tree-sitter AST → graph → MCP) but extends it furthest — multi-repo contracts and speculative execution are unique to it. Yet codegraph earns ADOPT on a *tighter, proven, auto-syncing* model with a minimal tool surface; gortex offers more surface and more risk. It is **not redundant** with the catalog (its cross-repo contract analysis and speculative-edit features are unduplicated), but it is **not a safer default than codegraph** today.

**Adopt when:** you work across multiple repositories with real cross-service API contracts (the standout feature), you want the strongest supply-chain guarantees in the category, you're comfortable running a pre-1.0 daemon and scoping the 100+ MCP tools to a per-task subset, and you value a single self-contained binary with zero runtime deps. **Re-evaluate for ADOPT** once it reaches a stable 1.x with broader adoption/contributor base, and once an independent benchmark corroborates the token-savings and blast-radius performance claims. **Stick with codegraph** if you only need always-on single-repo structural navigation with the lightest, most-proven footprint.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gortex](https://github.com/zzet/gortex) | MCP server | High-performance code-intelligence engine supporting 257 languages — CLI, MCP, Web UI, single Go binary | AI agents waste tokens reading whole files for structure and miss cross-repo/cross-service API contract relationships | codegraph, code-review-graph, code-context-engine, graphify, Understand-Anything |
