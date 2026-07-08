# Evaluation: token-optimizer-mcp

**Repo:** [ooples/token-optimizer-mcp](https://github.com/ooples/token-optimizer-mcp)
**Stars:** 410 | **Last updated:** 2026-06-14 | **License:** MIT
**Last verified:** 2026-07-08  <!-- source-grounded re-check; not a hands-on re-verification -->
**Dev loop stage:** Implement / Verify (intervenes on tool calls across the inner loop)
**Layer:** Infrastructure

---

## What it does

95%+ context reduction for tool outputs (the catalog headline; the README's own production claim is the more modest **60-90% across 38,000+ operations**, with per-tool figures climbing to 95% only on cache *hits*). token-optimizer-mcp is a TypeScript MCP server that reduces context-window usage by storing content **externally in a local SQLite database** and handing the agent compressed/diffed surrogates instead of raw output.

The mechanism has two halves. First, a **cache-and-retrieve core**: `optimize_text` compresses a blob with **Brotli** (claimed 2-4x typical, up to 82x on repetitive content), counts tokens with **tiktoken**, writes the original to SQLite under a key, and returns the key plus stats — the full content is recoverable later with `get_cached`. So, like headroom's CCR, the compression is **reversible in principle**, but retrieval is **opt-in**: the agent only gets the original back if it knows to call `get_cached`. Second, a large surface of **"smart" tool replacements** (`smart_read`, `smart_grep`, `smart_glob`, `smart_edit`, `smart_diff`, git wrappers, API/DB wrappers, build/test wrappers) that emit diff-only or match-only output instead of full payloads — this part is **lossy and one-way** (e.g. `smart_read` returns only the diff on subsequent reads; `smart_grep` returns match-only). The project advertises **65 tools total**, but many (multi-tier cache, ML/ARIMA "predictive cache", alerting, Prometheus/Grafana integration, cron/user management) are general caching/ops infrastructure orthogonal to the context-reduction headline.

For Claude Code, integration is `npm install -g @ooples/token-optimizer-mcp`, whose **postinstall script auto-installs global hooks** that route every tool call through the optimizer (7-phase PreToolUse/PostToolUse pipeline). This auto-configuration of the user's machine on `npm install` is convenient but unusually invasive for an MCP package.

## How we tested it

**Evidence:** REVIEW

**Architecture-review evaluation — not exercised in a live Claude Code session.** This MCP server requires a global npm install whose postinstall auto-modifies the host's AI-tool configs and installs hooks; running it for honest savings numbers needs a multi-session window on a real workload, which was out of scope here. So every reduction figure below is the **project's own published claim**, not measured by us — including the 95% headline, which the project ties specifically to cache hits. Method: inspected GitHub metadata, the full README (feature list, per-tool reduction claims, How-It-Works, hooks system), the repo tree (57 test files incl. integration/benchmark suites, a PowerShell hooks dispatcher, SQLite cache engine), release history (v5.0.1, active versioning), and contributor list. Calibrated against the two peer token-reduction evals (headroom = CONDITIONAL, rtk = CONDITIONAL).

```bash
gh api repos/ooples/token-optimizer-mcp --jq '{stars,license,description,pushed_at}'
gh api repos/ooples/token-optimizer-mcp/readme --jq '.content' | base64 -d
gh api "repos/ooples/token-optimizer-mcp/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/ooples/token-optimizer-mcp/contributors --jq '.[].login'
gh api repos/ooples/token-optimizer-mcp/releases --jq '.[].tag_name'
# Calibration: evaluations/headroom.md (CONDITIONAL), evaluations/rtk.md (CONDITIONAL)
```

## What worked

- **Reversible core via SQLite + `get_cached`.** Unlike rtk (one-way for success cases) and caveman (prompt-drop, irreversible), the `optimize_text`/`get_cached` pair caches the original locally so a needed detail can be pulled back — the same safety property headroom's CCR provides, in a lighter package.
- **Genuinely offline and zero-runtime-dependency.** Brotli + tiktoken + SQLite all run locally; no data leaves the machine and no external service is on the critical path. Good safety/privacy posture.
- **Single MCP install, no Rust/ONNX/HF build chain.** Materially lighter to install than headroom's `[all]` extra (maturin/rustup/ONNX/HuggingFace). One `npm install -g` and an MCP slot.
- **Real maturity signals for a small project.** 410 stars, MIT, active release cadence (v5.0.1), **57 test files** including integration, concurrency-stress, and benchmark suites, and a documented hooks system. More test discipline than a typical weekend script.

## What didn't work or surprised us

- **The 95% headline is a cache-hit best case, not a steady-state result.** The README's own production number is 60-90% across 38K operations; 95% appears only on `smart_api_fetch`/cache hits. The catalog one-liner repeats the most optimistic figure. There are **no accuracy-retention benchmarks** (contrast headroom's published GSM8K/TruthfulQA/SQuAD deltas) — savings are claimed, fidelity is not measured.
- **The "smart" tool layer is lossy and one-way.** `smart_read` diff-only, `smart_grep` match-only, `smart_edit` diff-only output discard surrounding context, and unlike the `optimize_text` core there is no general retrieve path for these surrogates — the agent must re-run the raw tool if a dropped detail turns out to matter. This is the same irrecoverable-loss risk that rtk/caveman carry.
- **Invasive auto-install.** The postinstall script auto-detects and rewrites configs for Claude Desktop/Cursor/Cline and installs global hooks on `npm install` — convenient but a surprising amount of host modification for an MCP package, and the primary hooks dispatcher is **PowerShell** (Windows-first; macOS/Linux parity via shell scripts is less exercised).
- **Single primary author + feature sprawl.** Effectively one author (`ooples`) plus dependabot. The 65-tool surface dilutes the core value with ML "predictive cache" (ARIMA/LSTM), distributed replication, and Prometheus/Grafana/alerting tooling that read as scope creep rather than context reduction, and inflate the maintenance/abandonment risk for a layer on the tool-call critical path.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | `get_cached` makes the cache core recoverable, but the lossy "smart" tool surrogates are one-way and no accuracy-retention benchmarks are published to bound fidelity loss |
| Speed | + | Fewer input tokens per turn and SQLite cache hits mean faster responses and more runway before compaction (project-claimed; not measured here) |
| Maintainability | neutral | 57 tests + active releases, but single-author core, PowerShell-first hooks, and a 65-tool sprawl raise abandonment and critical-path risk |
| Safety | + | Fully local/offline (Brotli + SQLite + tiktoken); no data leaves the machine — but the postinstall auto-modifies host AI-tool configs |
| Cost Efficiency | + | The core value: project-claimed 60-90% input-token reduction (95% on cache hits) across tool outputs, directly cutting per-session spend |

## Verdict

**CONDITIONAL**

Adopt token-optimizer-mcp when you want a single, offline, MIT-licensed MCP server that caches and compresses tool outputs without headroom's heavy Rust/ONNX/HF build chain, and you value the reversible `optimize_text`/`get_cached` core for recovering full content on demand. It is a real, additive tool — not a thinner duplicate — but it sits **below** headroom in the same cluster: headroom is reversible across *all* content types with published accuracy benchmarks and bundles rtk; token-optimizer-mcp is MCP-only, mixes a reversible cache core with a lossy one-way "smart tool" layer, and substantiates savings but not fidelity. It stops short of ADOPT for four reasons: the 95% headline is a cache-hit best case (steady state is 60-90%), no accuracy-retention evidence is published, the postinstall auto-modifies the host and is PowerShell-first, and the single-author 65-tool sprawl is a maintenance/critical-path risk. Prefer it over headroom when you want a lighter single-MCP install and accept MCP-only scope; prefer headroom when you want reversible coverage of all content with measured accuracy; prefer rtk for transparent, near-zero-friction Bash-output compression. Skip it if you only use a provider's native compaction or won't run a global hooks installer that edits your AI-tool configs.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [token-optimizer-mcp](https://github.com/ooples/token-optimizer-mcp) | MCP server | 95%+ context reduction for tool outputs | Context window fills up too fast | headroom, rtk, context-mode, caveman |
