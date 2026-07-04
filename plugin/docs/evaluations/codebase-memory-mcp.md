# Evaluation: codebase-memory-mcp

**Repo:** [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)
**Stars:** 8,056 | **Created:** 2026-02-24 | **Last commit:** 2026-06-19 | **Latest release:** v0.8.1 (2026-06-12) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan / Implement (inner loop) — code understanding
**Layer:** Tooling

---

## What it does

A code-intelligence MCP server that full-indexes a codebase into a persistent knowledge graph of functions, classes, call chains, HTTP routes, and cross-service links, then answers structural queries (search, trace, architecture, impact analysis, dead-code detection, Cypher queries) in under a millisecond. It ships as a single static C binary with zero runtime dependencies for macOS (arm64/amd64), Linux (arm64/amd64), and Windows (amd64). Parsing is tree-sitter AST across 158 languages, augmented by "Hybrid LSP" semantic type resolution for 11 languages (Python, TS/JS/JSX/TSX, PHP, C#, Go, C, C++, Java, Kotlin, Rust). The headline pitch: index an average repo in milliseconds, the Linux kernel (28M LOC) in ~3 minutes, with claims of ~120x fewer tokens versus file-by-file exploration.

The `install` command auto-detects 11 coding agents (Claude Code, Codex CLI, Gemini CLI, Zed, OpenCode, Antigravity, Aider, KiloCode, VS Code, OpenClaw, Kiro) and writes MCP entries, instruction files, skills, and pre-tool hooks for each. Exposes 14 MCP tools. Optional `--ui` variant serves a 3D interactive graph at `localhost:9749`. Also indexes IaC (Dockerfiles, Kubernetes, Kustomize) as graph nodes with cross-references, and has an auto-index mode with a git-based background watcher.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — we did **not** install or run the binary (it writes to agent config files and pre-tool hooks; out of scope for a read-only eval). All claims below are from the README, badges, and repo metadata, not independent measurement.

```
gh api repos/DeusData/codebase-memory-mcp --jq '{desc,stars,pushed,created,license}'
gh api repos/DeusData/codebase-memory-mcp/git/trees/HEAD --jq '.tree[].path'
gh api repos/DeusData/codebase-memory-mcp/readme --jq '.content' | base64 -d | head -130
gh api repos/DeusData/codebase-memory-mcp/releases --jq '.[0:3][] | {tag:.tag_name,date}'
```

## What worked

- **Unusually strong trust signals for an 8K-star tool.** OpenSSF Scorecard badge, SLSA Level 3 provenance, signed/checksummed release binaries, VirusTotal scan (70+ engines) per release, a SECURITY.md, and a DCO. This is far above the median MCP server's supply-chain hygiene.
- **Backed by a preprint.** The design and benchmarks are in arXiv:2603.27277, evaluated across 31 repos (83% answer quality, 10x fewer tokens, 2.1x fewer tool calls). Having a paper with a stated methodology is rare and raises confidence in the token-savings claims (note: the README headline says 120x, the paper says 10x — the gap is unexplained and worth treating skeptically).
- **Genuinely broad language coverage.** 158 tree-sitter grammars vendored into the binary plus Hybrid LSP for 11 — wider than most neighbors and with semantic (not just syntactic) resolution for the popular languages.
- **Single static binary, zero deps, local-only.** No Docker, no API keys, code never leaves the machine. The one-line installer and 11-agent auto-config make adoption low-friction.
- **5,604 passing tests** advertised, with CI and a public Makefile/test-infrastructure tree.

## What didn't work or surprised us

- **Pre-1.0 and very young.** Created Feb 2026, currently v0.8.x — three releases all dated the same day (2026-06-12) suggests rapid, possibly unstable, iteration. No track record of API stability yet.
- **The installer writes to your agent config and pre-tool hooks.** The README is upfront about this ("That is what it is designed to do"), but auto-editing instruction files and hooks across 11 agents is a high-blast-radius action that warrants reading the script first (the Windows path even tells you to).
- **Headline numbers are inconsistent and unverified by us.** "120x fewer tokens" (README) vs "10x" (paper) vs "99% fewer" (GitHub description) — three different figures. We did not run it, so treat all performance claims as vendor-stated.
- **Crowded niche.** This is the seventh-ish entrant in our code-intelligence-graph cluster (codegraph, code-context-engine, trace-mcp, SocratiCode, gortex, Understand-Anything). Its differentiators are the security posture, the paper, and 158-language breadth — not the core idea.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Knowledge graph of call chains, routes, and cross-service links gives agents accurate structure instead of guessing from partial reads; Hybrid LSP adds semantic type resolution |
| Speed | + | Sub-ms structural queries; one graph query replaces dozens of grep/read cycles (vendor-stated 2.1x fewer tool calls) |
| Maintainability | + | Impact analysis and dead-code detection help reason about change blast radius before editing |
| Safety | + | SLSA 3, OpenSSF Scorecard, signed/VirusTotal-scanned binaries, 100% local processing — but installer auto-edits agent hooks/config (read the script) |
| Cost Efficiency | + | Vendor-claimed 10x–120x token reduction; single binary, no API keys or hosted service costs |

## Verdict

**CONDITIONAL**

The most security-hardened and best-documented entry in our code-intelligence-graph cluster, and the only one with a published preprint and benchmark methodology — that combination is the reason to look at it over `gortex` (more languages: 257, but thinner trust signals) or `code-context-engine` (simpler, search-only). Adopt it when you need a local, zero-dependency, broad-language structural index and you value the supply-chain provenance. It stays CONDITIONAL rather than ADOPT for two reasons: it is pre-1.0 and only four months old (no stability track record, three same-day releases), and its installer auto-writes agent config and pre-tool hooks across 11 agents — a high-trust action you should audit before running. The conflicting token-savings figures (10x/99%/120x) also argue for measuring on your own repo before believing the headline. Re-evaluate at a 1.0 release.

## Catalog entry

**Target category: MCP Servers**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | MCP server | Static-binary code-intelligence engine indexing 158 languages into a persistent knowledge graph, sub-ms queries (8K stars) | Agents waste tokens reading files; need fast, local, broad-language structural indexing with supply-chain provenance | code-context-engine, gortex, SocratiCode, trace-mcp, codegraph |
