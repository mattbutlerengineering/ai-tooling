# Evaluation: AutoSci

**Repo:** [skyllwt/AutoSci](https://github.com/skyllwt/AutoSci)
**Stars:** ~1,360 | **Last updated:** 2026-06-20 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect (Research & Discovery)
**Layer:** Tooling

---

## What it does

AutoSci is a memory-centric agentic research system — "read, think, experiment, write, evolve" — that aims to handle the full scientific research lifecycle, powered by Claude Code. It evolved from an earlier OmegaWiki prototype and is positioned as a realization of Karpathy's LLM-Wiki vision.

Mechanically (per the paper, arXiv:2605.31468), the full system comprises **SciMem** (compounding cross-project memory), **SciFlow** (research workflow), **SciDAG** (task graph), and **SciEvolve** (self-improvement) — these live on the `paper` branch as a research snapshot, while `main` is a leaner, stable version. The defining idea is memory that **compounds across every project**: rather than starting each research task cold, the agent accumulates and reuses knowledge and methods over time.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the paper abstract (arXiv:2605.31468), noting the explicit `main` (stable/lean) vs `paper` (full system, research snapshot) branch split. Confirmed the SciMem/SciFlow/SciDAG/SciEvolve architecture and the compounding-memory thesis. The README is candid that the `paper` branch is "a research snapshot, not a finished product" with capabilities still being implemented. Not run live, so condition-gated.

```bash
gh api repos/skyllwt/AutoSci --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/skyllwt/AutoSci/readme --jq '.content' | base64 -d
```

## What worked

- **Compounding memory across projects.** The standout idea — research methods/knowledge that accumulate rather than reset per task — is exactly what single-shot research agents lack.
- **Full-lifecycle ambition + paper.** Covering read→experiment→write→evolve with an arXiv paper behind it is more rigorous than a prompt-chain research bot.
- **Honest staging.** Clearly separating the stable `main` from the experimental `paper` branch is responsible communication.

## What didn't work or surprised us

- **Research snapshot, not a product.** The full system (paper branch) is explicitly under active development with capabilities "still being implemented" — expect rough edges.
- **Young.** ~1.4K stars; durability and real-world results are unproven beyond the paper.
- **Overlaps ARIS / AutoResearchClaw / karpathy-llm-wiki.** Several autonomous-research harnesses exist; AutoSci's edge is the memory-centric (SciMem) compounding angle.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Cross-project memory reduces repeated dead-ends in research |
| Speed | + | Reuses prior methods/knowledge instead of starting cold |
| Maintainability | neutral | A research agent; not part of a codebase |
| Safety | neutral | Verify claims; research output needs human checking |
| Cost Efficiency | neutral | Long-horizon research loops are token-heavy |

## Verdict

**CONDITIONAL**

Promising for long-horizon, multi-project research where compounding memory (SciMem) would pay off — but it's an actively-iterating research project, so adopt the lean `main` for stability and treat the full `paper`-branch system as experimental. Overlaps ARIS/AutoResearchClaw; choose AutoSci for the memory-centric lifecycle angle. Re-evaluate as the implementation catches up to the paper.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [AutoSci](https://github.com/skyllwt/AutoSci) | harness | Memory-centric agentic research system (MIT, paper-backed) — full scientific-lifecycle agent (read→think→experiment→write→evolve) on Claude Code, with compounding cross-project memory (SciMem/SciFlow/SciDAG/SciEvolve) | Single-shot research agents lose context and don't improve; want a full-lifecycle research agent whose memory and methods compound across projects | ARIS, AutoResearchClaw, karpathy-llm-wiki, storm |
