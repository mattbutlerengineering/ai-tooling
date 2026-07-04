# Evaluation: ARIS (Auto-Research-In-Sleep)

**Repo:** [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
**Stars:** 12,350 | **Last updated:** 2026-06-19 (pushed; created 2026-03-10) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Research & Discovery (a research-automation methodology; the cross-model adversarial-review and self-evolution patterns also touch Review and Reflect)
**Layer:** Process + Tooling (a portable skill-based workflow *plus* an optional standalone Rust CLI, "ARIS-Code")

---

## What it does

ARIS is an **autonomous research workflow** — "hand it a fuzzy direction, wake up to reviewed work." It's framed as a *methodology, not a platform*: a five-step loop (**plan → draft → adversarial review → iterate → persist**) packaged as Markdown skills you can run inside Claude Code, Codex CLI, Cursor, Antigravity, Copilot CLI, or its own standalone CLI. Its origin is academic ML research (paper search, idea generation, paper writing/review — it has an arXiv technical report and was a Hugging Face #1 daily paper), but the same loop is generalized by sibling projects (ARIS-Anything) to investment due-diligence, legal/market research, and engineering retros.

The two pillars that distinguish it:
- **Cross-model adversarial review.** Rather than one model self-reviewing (which it likens to a stochastic bandit — predictable, gameable), ARIS pairs an *executor* model with a different *reviewer* model that actively probes for weaknesses (e.g. Claude executing, Codex/gpt-5.5 reviewing across multiple GO/NO-GO rounds). The README's own changelog is written this way — every release reviewed phase-by-phase by "Codex MCP (gpt-5.5 xhigh)". v0.4.17 lets you wire a ChatGPT subscription in as the reviewer with **no OpenAI API key** via Codex MCP.
- **Research Wiki + self-evolution.** A persistent knowledge base (papers / ideas / experiments / claims + a relationship graph) gives long-horizon memory across sessions; `/meta-optimize` analyzes run logs and proposes patches to its own SKILL.md files.

It ships 13+ named workflows, MCP tool dispatch on both Anthropic and OpenAI-family providers, multi-provider support (Kimi/GLM/MiniMax/DeepSeek/local Ollama/LM Studio), and an optional macOS floating monitor widget.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No skills copied, no CLI built, no research run executed. Claims come from the repository (GitHub metadata, README, detailed per-release changelog, topics) and its linked technical report — the project's own documentation, not observed research quality.

```bash
gh api repos/wanshuiyin/Auto-claude-code-research-in-sleep --jq '{stars,created_at,pushed_at,license:.license.spdx_id,topics}'
gh api repos/wanshuiyin/Auto-claude-code-research-in-sleep/readme --jq '.content' | base64 -d   # methodology, workflows, changelog
gh api repos/wanshuiyin/Auto-claude-code-research-in-sleep/releases --jq 'length'                # 30
```

## What worked

- **Cross-model adversarial review is the standout idea.** "No model signs off on its own work" is a genuinely strong correctness pattern, and it's portable far beyond research — it's exactly the executor/reviewer split good agent dev loops want. The 1→2 model argument (break self-play blind spots; 2-player converges to Nash faster than n-player) is well reasoned.
- **Persistent Research Wiki addresses real long-horizon memory loss.** A structured, queryable claims/experiments graph is more durable than chat-history context — the same problem the catalog's Memory & Context tools target, applied to research.
- **Self-evolution (`/meta-optimize`).** Analyzing logs to propose its own skill patches is a concrete take on the catalog's "feedback arcs make each cycle better" thesis.
- **Genuinely portable + provider-agnostic.** Runs as skills across many harnesses or as its own CLI; supports many providers and zero-API-key cross-model review via a ChatGPT subscription. MIT-licensed.
- **Visibly serious engineering.** 30 releases, an arXiv report, a meticulous changelog showing adversarial review applied to its own development, active contributor community.

## What didn't work or surprised us

- **Primary domain is academic research, not software dev.** Most built-in workflows are paper-centric (literature search, paper writing, citation audit, conference talks). For a software dev loop the *value is the methodology* (adversarial review, persistent wiki, meta-optimize), not the out-of-the-box pipelines.
- **Large, fast-moving surface.** A Rust CLI + dozens of skills + MCP + multi-provider routing is a lot to adopt and is iterating very rapidly (16-release polish run in weeks); the changelog is dense with provider-edge-case bug fixes, signaling real complexity to keep stable.
- **Cross-model review doubles cost and setup.** Running two model families (executor + reviewer) is more tokens and more configuration than a single-model loop — justified for high-stakes output, overkill for routine work.
- **Sprawl of sibling repos** (ARIS-Anything, ARIS-Movie-Director, ARIS-in-AI-Offer, ARIS-Monitor) makes the "what exactly am I adopting" boundary fuzzy; the core repo mixes a CLI, a methodology, and a marketing surface.
- **Self-reported, unverified.** Benchmarks and quality claims come from the project; not independently reproduced here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Cross-model adversarial review (reviewer ≠ executor, multi-round GO/NO-GO) is a strong guard against self-approved errors; persistent claims wiki reduces context loss. |
| Speed | + / − | Autonomous overnight ("in sleep") runs parallelize human time (+); two-model review rounds add latency per iteration (−). |
| Maintainability | neutral | Affects research/work output, not your codebase structure. |
| Safety | + / neutral | Reviewer-as-gate + approval gates for untrusted MCP tools; standard agent file/exec trust model otherwise. |
| Cost Efficiency | − | Two model families per loop + long autonomous runs spend meaningfully more tokens than single-model workflows. |

## Verdict

**CONDITIONAL** — adopt the *methodology* broadly and the *tool* narrowly. The cross-model adversarial-review pattern (no model reviews its own work) and the persistent Research Wiki are excellent, transferable ideas that any high-stakes agent loop should steal. As a turnkey tool it's strongest for **autonomous academic/ML research** (its native domain); for general software work the built-in paper-centric workflows are a partial fit and the two-model cost is real. Adopt if you do research-heavy autonomous work and want adversarial review + durable memory out of the box; otherwise mine it for the patterns. MIT-licensed, actively and seriously developed.

Compared to neighbors: **autoresearch** (Karpathy) runs automated experiments but without the cross-model review/persistent-wiki scaffolding; **llm-council** convenes a multi-model committee for one-shot answers rather than a persistent iterate-and-persist loop; **deer-flow** is a research harness. ARIS is the most complete **autonomous, adversarially-reviewed, memory-backed research loop** of the set — at the cost of breadth and token spend.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | skill | Autonomous research loop (plan→draft→cross-model adversarial review→iterate→persist) as portable skills + a Rust CLI, with a persistent Research Wiki and self-evolution | Single-model self-review is gameable and context is lost between runs; want overnight research with a reviewer model and durable memory | autoresearch, llm-council, deer-flow, PaperOrchestra |
