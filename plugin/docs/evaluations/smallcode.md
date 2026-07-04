# Evaluation: SmallCode

**Repo:** [Doorman11991/smallcode](https://github.com/Doorman11991/smallcode)
**Stars:** 1,903 | **Last updated:** 2026-06-04 (pushed; created 2026-05-18) | **License:** MIT | **Releases:** 24
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (a terminal coding agent; touches all inner-loop stages)
**Layer:** Tooling (JavaScript; `npm i -g smallcode` / `npx smallcode`)

---

## What it does

SmallCode is a **terminal coding agent designed from the ground up for small, local LLMs (8B–35B parameters)** running on consumer hardware. Its premise: tools like OpenCode assume frontier models with 128k+ context and perfect tool calling, which small models don't have — so SmallCode compensates with architecture rather than model power. Its own comparison table spells out the adaptations vs. OpenCode:

- **Context**: budget-managed and summarized (not "dump everything").
- **Tool calling**: a *forgiving multi-format parser* instead of assuming reliable JSON.
- **Planning**: TODO-file-decomposed steps instead of single-shot.
- **Editing**: search-and-replace patches instead of full-file writes.
- **Privacy**: fully local, no network needed (vs. cloud API calls).

It's explicit about the sweet spot: **8B–35B**. It warns that ≤4B models "struggle with multi-step tool use and lose context across turns," and that >35B models don't need its adaptations and are better served by frontier-oriented tools.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No model loaded, no session. Claims (including the "87% benchmark with a 4B-active model" tagline) come from the repository (GitHub metadata, README comparison table, 24 releases) — the project's own documentation, not reproduced benchmarks.

```bash
gh api repos/Doorman11991/smallcode --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/Doorman11991/smallcode/readme --jq '.content' | base64 -d   # OpenCode vs SmallCode table, model-size guidance
gh api repos/Doorman11991/smallcode/releases --jq 'length'             # 24
```

## What worked

- **Genuinely underserved niche.** Almost every catalog agent assumes frontier models; SmallCode targets *local 8B–35B* models on consumer hardware. For privacy-constrained, offline, or cost-zero use, that's a real and distinct value.
- **The adaptations are the right ones.** Forgiving multi-format tool-call parsing, context budgeting/summarization, TODO-file planning, and search-replace patches are exactly the failure modes small models hit — this is thoughtful architecture, not just a config preset.
- **Fully local / no network** is a strong privacy and cost story — no API calls, no data egress.
- **Honest scoping.** Explicitly telling users ≤4B and >35B are the *wrong* fit is unusually candid and builds trust in the benchmark framing.
- **Active, MIT, npm-installable**, 24 releases since mid-May.

## What didn't work or surprised us

- **Ceiling is the small model itself.** No amount of harness cleverness makes an 8B–35B model match a frontier model on hard, multi-file tasks; SmallCode raises the floor, it doesn't remove the gap. Expect more babysitting on complex work.
- **Benchmark is self-reported.** "87% with a 4B-active model" is a headline number from the project, unverified here and benchmark-dependent; treat as indicative, not proven.
- **Tagline vs. guidance tension.** The README touts a 4B-active result while also warning ≤4B models struggle — likely a MoE "active params" nuance, but worth understanding before expecting tiny-model performance.
- **Young and single-maintainer.** ~1.9K stars, ~1 month old; longevity unproven.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Forgiving tool parsing + TODO planning + patch edits reduce small-model failure modes; absolute quality still bounded by the local model. |
| Speed | neutral | Local inference speed depends on your hardware; the harness adds structure, not raw speed. |
| Maintainability | neutral | A coding tool, not a codebase-structure influence. |
| Safety | + | Fully local, no network — strong privacy posture; standard shell/file trust model otherwise. |
| Cost Efficiency | + + | Runs entirely on local models — zero API/token cost; the core value proposition. |

## Verdict

**CONDITIONAL** — adopt if you specifically want agentic coding on **local 8B–35B models** for privacy, offline, or zero-cost reasons, and accept the quality ceiling that comes with small models. It's the rare tool built *for* that constraint, and its adaptations (forgiving tool parsing, context budgeting, TODO planning, patch edits) are well-aimed. Skip it if you have frontier-model access — those models plus a frontier-oriented harness (opencode, Claude Code) will outperform, and SmallCode's own docs say so. Treat the headline benchmark as unverified.

Compared to neighbors: **open-interpreter** also targets cheap open models (Deepseek/Kimi/Qwen) with native sandboxing; **DeepSeek-Reasonix** tunes for one provider's caching; **oh-my-pi**/**gemini-cli** assume capable hosted models. SmallCode is the most explicitly **small-local-model-optimized, fully-offline** agent of the set — the privacy/zero-cost end of the spectrum.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [smallcode](https://github.com/Doorman11991/smallcode) | tool | Terminal coding agent built for small local LLMs (8B–35B) — context budgeting, forgiving multi-format tool parsing, TODO-file planning, patch edits, fully offline | Frontier-oriented agents assume huge context + perfect tool calls; small/local models need a harness that compensates, with zero cloud cost | open-interpreter, DeepSeek-Reasonix, oh-my-pi, gemini-cli |
