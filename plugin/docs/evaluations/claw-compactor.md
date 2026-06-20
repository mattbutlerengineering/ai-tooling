# Evaluation: Claw Compactor

**Repo:** [open-compress/claw-compactor](https://github.com/open-compress/claw-compactor)
**Stars:** 2,198 | **Last updated:** 2026-04-01 (pushed) | **License:** MIT | **Language:** Python (PyPI: `claw-compactor`)
**Dev loop stage:** Memory & Context (token compression) — Implement
**Layer:** Tooling (CLI + library)

---

## What it does

Claw Compactor (by OpenClaw) is an **LLM token-compression engine** built around a **14-stage "Fusion Pipeline."** Each stage is a specialized compressor — **AST-aware code analysis**, JSON statistical sampling, RLE, simhash-based **semantic deduplication**, and more — chained through an immutable data-flow architecture where each stage's output feeds the next. Headline claims: **15–82% compression depending on content**, **zero LLM inference cost** (deterministic, not a summarizer model), **reversible** compression, AST-aware code analysis, intelligent content routing, and 1,600+ tests. CLI example `claw-compactor benchmark ./workspace` reports per-stage reduction and timing.

## How we tested it

**Source-grounded inspection — not installed, not run.** No workspace compressed, compression ratios not reproduced, reversibility not verified.

```bash
gh api repos/open-compress/claw-compactor --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 2198, MIT, pushed 2026-04-01
gh api repos/open-compress/claw-compactor/readme --jq '.content' | base64 -d | head -75               # 14-stage Fusion Pipeline, reversible, zero-inference
```

## What worked

- **Deterministic + reversible is the right design.** Compressing context with a *pipeline* (AST analysis, dedup, sampling) rather than an LLM summarizer means **zero inference cost** and — crucially — **reversibility**, so you don't silently lose information the way lossy summarization does. That's a meaningfully safer compression model.
- **Content-aware routing.** Different stages for code (AST) vs. JSON (statistical sampling) vs. repetitive text (RLE/simhash) is smarter than one-size-fits-all truncation, and the 15–82% spread honestly reflects content dependence.
- **Test-heavy.** 1,600+ tests for a compression engine signals attention to correctness (compression bugs are nasty).
- **MIT, library + CLI.** Embeddable into a pipeline or hook; free.

## What didn't work or surprised us

- **Crowded compression niche.** Overlaps headroom, context-mode, token-optimizer-mcp, rtk, lean-ctx — all attacking context bloat. The wedge is the deterministic, reversible, AST-aware multi-stage pipeline, not the goal.
- **Self-reported ratios.** 15–82% and the per-stage benchmark are vendor-stated and highly content-dependent; real savings need measuring on your data.
- **Integration is on you.** It's an engine/CLI, not a turnkey hook; wiring it into an agent's read/tool-output path (the way headroom/context-mode do automatically) is your work.
- **Slightly staler push (2026-04-01).** Active project but not same-week fresh; "OpenClaw" branding ties it to that ecosystem.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Reversible compression avoids the information loss of LLM summarization; correctness depends on faithful round-trips (1,600+ tests). |
| Speed | + | Deterministic stages run in ms (per the benchmark demo); no model round-trip. |
| Maintainability | neutral | A library to integrate; immutable pipeline is clean but it's another component in the stack. |
| Safety | + | Reversibility + zero-inference means no external data egress and no silent lossy summaries. |
| Cost Efficiency | + | Core pitch: 15–82% fewer tokens at zero inference cost directly cuts context spend. |

## Verdict

**CONDITIONAL** — Claw Compactor is a thoughtfully-designed, MIT **token-compression engine** whose differentiators are real: a **deterministic, reversible, content-aware 14-stage pipeline** (AST analysis, dedup, sampling) that cuts tokens with **zero LLM inference cost** and without the silent information loss of summarizer-based compression. Adopt it when you want to compress code/JSON/log-heavy context *reversibly* and don't want to pay a model to do it — especially where auditability and round-trip fidelity matter. It's CONDITIONAL because the ratios are self-reported and content-dependent, the niche is crowded, and you integrate the engine yourself (unlike auto-hook tools headroom/context-mode). Measure on your own workspace before trusting the headline numbers.

Compared to neighbors: **headroom**/**context-mode** auto-compress tool outputs reversibly via hooks; **token-optimizer-mcp** compresses via MCP; **rtk** proxies dev commands; **lean-ctx** compresses reads + persists memory. Claw Compactor's distinguishing pitch is **a deterministic, reversible, AST-aware multi-stage compression engine with zero inference cost.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claw-compactor](https://github.com/open-compress/claw-compactor) | tool | LLM token-compression engine (MIT, OpenClaw) — 14-stage "Fusion Pipeline" (AST-aware code analysis, JSON statistical sampling, simhash dedup) with reversible compression and zero LLM inference cost; 15–82% reduction depending on content | Verbose code/JSON/logs fill the context window; want deterministic, reversible compression without paying an LLM to summarize | headroom, context-mode, token-optimizer-mcp, rtk, lean-ctx |
