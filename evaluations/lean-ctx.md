# Evaluation: lean-ctx

**Repo:** [yvgude/lean-ctx](https://github.com/yvgude/lean-ctx)
**Stars:** 2,795 | **Last updated:** 2026-06-19 (pushed; created 2026-03-23) | **License:** Apache-2.0
**Last verified:** 2026-07-08  <!-- source-grounded re-check; not a hands-on re-verification -->
**Dev loop stage:** Spans the inner loop as a *substrate*, not a stage — it sits between the agent and the repo/shell on every read and command (Implement-heavy), plus a memory layer that aids Plan and an impact-graph that aids Review. Closest single anchor: Implement.
**Layer:** Tooling + Infrastructure (one local Rust binary that is both an MCP server and a transparent shell hook; holds local SQLite/graph state, optional HTTP serve, browser dashboard).

---

## What it does

Catalog one-liner framing: "Control what your AI can see — Lean Context." **LeanCTX** is a single local Rust binary that sits between AI agents and your code/shell/data and manages context as a first-class resource. The README organizes it as "four dimensions": **Compression** (10 file read modes — `full`/`map`/`signatures`/`diff`/`lines:N-M`/`density:X`; cached re-reads ~13 tokens; 95+ shell-output patterns compressing git/npm/cargo/docker/kubectl/terraform; tree-sitter AST for 18 languages), **Routing** (an adaptive `ModePredictor` that learns the best read mode per file type, an `IntentEngine` classifying query complexity), **Memory** (session memory "CCP" surviving compaction, a temporal knowledge graph, a multi-edge property graph for impact analysis), and **Verification** (a browser Context Manager dashboard with live token tracking, per-agent budgets/SLOs, and `ctx_proof`/`ctx_verify` with CI drift gates). It advertises **77 MCP tools** including web/PDF/YouTube ingestion (`ctx_url_read`, SSRF-guarded), LSP refactoring via rust-analyzer/tsserver/pylsp/gopls, multi-agent handoff (`ctx_agent`/`ctx_handoff`), and a **signed, tamper-evident savings ledger** (SHA-256 chain) claiming 60–90% token reduction.

Mechanically it ships as a Rust crate (`crates.io`), npm binary wrapper (`lean-ctx-bin`), Homebrew, AUR, and an install script, with editor packages for VS Code, JetBrains (Kotlin), and a Chrome extension, plus Rust/Python client SDKs. Install is `lean-ctx onboard`/`setup` (auto-detects 30+ agents and wires MCP + shell hooks), then `lean-ctx doctor` to verify; `lean-ctx gain --live` shows running savings. It is explicitly local-first with opt-in telemetry and a `lean-ctx-off` kill switch.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No binary was installed (no curl-install, brew, cargo, or npm), no agent was onboarded, no shell hook was activated, no file was read through a mode, and no `gain`/savings ledger was generated. The 60–90% reduction, "~13 tokens on re-read," "77 MCP tools," and per-command compression figures are the **authors' README/benchmark claims, not measurements I made**. Everything below is from the repository (GitHub metadata, README, recursive file tree, commit/release counts) and the project's framing.

```bash
gh api repos/yvgude/lean-ctx --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,topics}'
gh api repos/yvgude/lean-ctx/readme --jq '.content' | base64 -d | head -300
gh api "repos/yvgude/lean-ctx/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # Rust crates + clients/{rust,python} + packages/{vscode,jetbrains,chrome}
gh api repos/yvgude/lean-ctx/commits  --jq 'length'   # 30 (page-1 cap; pushed same-day, very active)
gh api repos/yvgude/lean-ctx/releases --jq 'length'   # 30+ (real release cadence — unlike most peers)
```

## What worked

- **Genuinely broad, single-binary scope.** Most context-optimizers do one thing (compress tool output). LeanCTX bundles read-mode compression, shell-output compression, session memory, a code property graph, LSP refactoring, web ingestion, and a savings ledger into one Rust binary with `onboard` auto-wiring for 30+ agents. If the claims hold, that's a lot of surface from one install.
- **"Prove the savings" is a differentiator.** A signed, tamper-evident per-event ledger (`lean-ctx savings`, SHA-256 chain, tokenizer transparency) directly answers the "does this actually save tokens?" skepticism that dogs every tool in this category — peers (`context-mode`, `token-optimizer-mcp`) assert percentages; LeanCTX ships a receipt mechanism.
- **JIT / progressive-disclosure read modes are the right idea.** `signatures` returning an outline with `lines:N-M` spans for on-demand body expansion, plus `density:X` entropy budgeting, is a smarter approach than blunt whole-output compression — it gives the model structure first, detail on request.
- **Mature release & repo engineering.** 30+ tagged releases on a ~3-month-old repo, CI + CodeQL + a dedicated security-check workflow, CLA, issue templates (incl. a "compression_pattern" template), Rust/Python SDKs, and multi-IDE packages. The release cadence and security tooling are well above the category norm.
- **Local-first with explicit off-ramps.** `lean-ctx-off`, `--raw` passthrough, `agents-only` shell activation, per-project `.lean-ctx.toml`, opt-in telemetry — the safety/escape hatches are thought through, which matters for a thing intercepting every read and shell command.

## What didn't work or surprised us

- **Surface area vastly exceeds the catalog slot.** This is marketed as a "cognitive context layer" with a roadmap toward multi-agent governance, OTel/Prometheus SLOs, and "Context as Code." For a Memory & Context entry that competes with output-compressors, the scope is enormous — and large scope on a young project means many of the 77 tools are likely shallow or beta. README breadth ≠ depth.
- **A shell hook intercepting every command is invasive.** Transparently rewriting `git`/`npm`/`cargo`/`docker`/`kubectl`/`terraform` output is powerful but high-blast-radius: a compression bug can silently corrupt what the model (or you) sees from a real command. The `--raw`/off switches exist precisely because this is risky; it needs trust the project hasn't yet earned at 3 months old.
- **All performance numbers are self-reported.** 60–90% reduction, ~13-token re-reads, the benchmark GIFs — generated from the project's own VHS tapes/benches. No third-party validation, and the ledger "proves" savings *against LeanCTX's own baseline assumptions*, not against an independent tokenizer audit.
- **Young, single-maintainer-shaped, high churn.** Created 2026-03-23, pushed same day as inspection, 30+ releases in ~3 months — impressive velocity but also a moving target with little settling time. Betting your whole read/shell path on a 3-month-old binary is a real stability risk.
- **Overlap and redundancy with tools you may already run.** The code-graph/impact/LSP-refactor features overlap heavily with serena/codebase-memory-mcp; the memory features overlap with claude-mem/OMEGA; the compression overlaps with headroom/context-mode. Adopting all of LeanCTX risks duplicating capabilities you've already chosen elsewhere.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Cost Efficiency | + | The core pitch and best-evidenced area: read-mode + shell-output compression and cached re-reads cut tokens; the savings ledger at least attempts to quantify it (self-reported 60–90%). |
| Speed | + / − | Less context to process and JIT disclosure can speed the agent; offset by the binary's interception overhead on every read/shell call and onboarding/restart friction. |
| Correctness | + / − | Session memory + property-graph impact analysis can improve grounding; but lossy compression of file/shell output risks the model acting on a truncated view — net depends on mode discipline. |
| Safety | − / neutral | Intercepts every read and shell command (high blast radius), but local-first, opt-in telemetry, SSRF-guarded web reads, and explicit `--raw`/`lean-ctx-off` kill switches mitigate. Trust gated by repo youth. |
| Maintainability | neutral | Doesn't change your code; adds an always-on binary in your dev/agent loop you must keep updated and reason about when output looks wrong. |

## Verdict

**CONDITIONAL — try the compression + savings-ledger core on a non-critical project to validate the token claims yourself; do not adopt the full "cognitive context layer" surface yet.** LeanCTX is the most ambitious entry in this category — a single Rust binary spanning compression, memory, code-graph, and verification, with unusually mature release/security engineering and a genuinely novel signed savings ledger that addresses the category's core credibility gap. The catch is exactly that ambition: at ~3 months old it's a fast-moving target whose 77 tools far exceed any single catalog slot, whose shell-hook interception is high-blast-radius, and whose every performance number is self-reported. The disciplined move is to use it narrowly (read-mode compression + `gain`/`savings`), measure real savings against your own baseline, and resist letting it subsume the memory/graph/refactor jobs you've already assigned to other tools.

Compared to neighbors: **context-mode**, **headroom**, and **token-optimizer-mcp** are simpler, single-purpose output-compressors — easier to trust and reason about, and sufficient if all you want is fewer tokens from verbose tool output. LeanCTX is the heavyweight: it does what all three do *plus* memory, a code property graph, LSP refactoring, web ingestion, and verification — so it competes not just with them but with serena (impact/refactor), claude-mem/OMEGA (memory), and claude-context (code intelligence). It wins on breadth, release maturity, and provable savings; it loses on focus, maturity-of-each-feature, and the inherent risk of routing your entire read/shell path through one young binary.

## Catalog entry

Target category: **Memory & Context**.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lean-ctx](https://github.com/yvgude/lean-ctx) | tool | Local Rust binary + MCP server that compresses reads/shell output (10 read modes, ~13-tok re-reads), persists session memory, builds a code property graph, and proves savings via a signed ledger | AI agents waste context on re-reads and verbose tool output, forget across chats, and offer no proof of token savings | context-mode, headroom, token-optimizer-mcp, claude-mem, serena, claude-context |
