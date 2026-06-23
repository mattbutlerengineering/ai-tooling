# Spike: Best agent harness for the GLM-5.2 model

**Issue:** [#116](https://github.com/mattbutlerengineering/ai-tooling/issues/116) ·
**Date:** 2026-06-23 · **Status:** complete (recommendation below) ·
**Evidence:** REVIEW — source-grounded (Z.ai official docs + community reports +
catalog/COMPARISON cross-check). **Not run hands-on against GLM-5.2**: this spike
did not install a Z.ai key or execute any harness against the live model. Verdicts
here are *leads for a MEASURED follow-up*, not exercised verdicts. Slugs/licenses
were verified via `gh api` on 2026-06-23.

> Spikes live outside `evaluations/` on purpose: they compare many tools and carry
> no single `## Verdict`, so they are not parsed by the eval/verdict integrity gates.
> Promoting any recommendation here into an ADOPT catalog verdict requires a real
> MEASURED eval under `evaluations/TEMPLATE.md`.

---

## The question

The ticket asked for the best harness to run **GLM-5.2** and named two candidates
(`opencode`, `omp`/oh-my-pi) with "search for other similar harnesses." This spike
evaluates **12+ harnesses**, applies the repo's adoption bars strictly, and names a
clear pick.

## TL;DR — strict recommendation

The decisive fact is **how GLM is served, not which harness wraps it.** Z.ai exposes
**both** an Anthropic-compatible endpoint (`https://api.z.ai/api/anthropic`) and an
OpenAI-compatible one (`https://api.z.ai/api/coding/paas/v4`). GLM-5.2's one
documented weakness is **tool-calling reliability** (malformed/hallucinated tool
params; tool calls leaking into reasoning traces). The fix is endpoint-level, not
harness-level: route through an **exacto-class endpoint** (a backend selected for
verified tool-use success — Z.ai's own coding endpoint, or OpenRouter `:exacto`) and
use a **leaner, mechanically-precise system prompt**. Any harness on a naive route
will under-perform; any competent harness on a good route will do well.

Given that, the harness choice reduces to license + ergonomics + GLM-specific tuning:

| Rank | Pick | When | Why | Adoptable? |
|------|------|------|-----|------------|
| **1 (practical)** | **Claude Code → GLM** via `ANTHROPIC_BASE_URL` | You'll accept a proprietary CLI | Z.ai's #1 documented integration; two-line config; tool-calling reliable because GLM speaks the **Anthropic protocol natively** on this endpoint; "$18/mo Claude Code" framing | ❌ **No** — proprietary (license `NONE`); fails the MIT-permissive stack bar. *Use it, don't stack-adopt it.* |
| **1 (open-source)** | **opencode** (`anomalyco/opencode`, MIT, ★178K) | You need permissive OSS | Consensus OSS pick; officially listed by Z.ai; positive GLM-5.2 hands-on reports; cleanest multi-provider system (OpenAI- *and* Anthropic-compat custom base URLs); headless-capable | ✅ MIT — **the strict ADOPT candidate**, pending a MEASURED eval |
| **2 (dark horse)** | **oh-my-pi / omp** (`can1357/oh-my-pi`, MIT, ★14K) | Complex codebases; "tokenmaxxer" workflows | The **only** harness shipping *explicit GLM-coding-plan tuning* (per-family tool-call conversion, stream-watchdog idle floor tuned for GLM hosts); batteries-included (LSP, DAP, Python, subagents) | ✅ MIT — but currently **SKIP** in the catalog (it replaces Claude Code wholesale). Re-evaluate given the GLM tuning. |
| **ref** | **Cline** (`cline/cline`, Apache-2.0, ★64K) | VS Code; you want the integration playbook | **Best-documented GLM integration anywhere** — it is the canonical source on the tool-calling failure mode and the exacto fix; cut its system prompt 56k→24k for GLM | ✅ Apache-2.0 |

**Bottom line:** for an open-source answer, **opencode** is the pick. If proprietary
is acceptable, **Claude Code pointed at the GLM Coding Plan** is the lowest-friction,
most-reliable option Z.ai itself leads with. **Either way, route via an exacto-class
endpoint** — that single decision moves correctness more than the harness does.

---

## GLM-5.2 facts that drive harness choice

- **Real model.** GLM-5.2 (Z.ai, formerly Zhipu), released **2026-06-16**, is the
  current flagship coding model. Open-weight (reported MIT — *unconfirmed on the
  official model page*) + API. ~1M-token context. ([docs.z.ai/guides/llm/glm-5.2](https://docs.z.ai/guides/llm/glm-5.2))
- **Dual endpoints (the crux).** Anthropic Messages **and** OpenAI Chat Completions.
  Claude Code uses the Anthropic one; everything else uses the OpenAI one.
  ([docs.z.ai/devpack/tool/claude](https://docs.z.ai/devpack/tool/claude))
- **Agentic-tuned, but tool-calling is the soft spot.** Strong long-horizon coding
  benchmarks (SWE-bench **Pro** 62.1; Terminal-Bench 2.1 81.0, vs Opus 4.8 85.0),
  but community + Cline report tool-call breakage on naive routing.
  ([VentureBeat](https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost),
  [Cline blog](https://cline.bot/blog/cline-our-commitment-to-open-source-zai-glm-4-6))
- **~1/6 the cost of Opus** (~$1.40/$4.40 per 1M in/out via OpenRouter; GLM Coding
  Plan from **$18/mo**). Cost is GLM's main draw, so the harness should not add
  per-token middleman cost. ([docs.z.ai/devpack/overview](https://docs.z.ai/devpack/overview))
- **Officially supported harnesses (Z.ai docs):** Claude Code, Claude-for-IDE,
  opencode, Cursor, Cline, TRAE, Qoder, Droid, Kilo Code, Roo Code, Crush, Goose,
  Eigent. Overview foregrounds **Claude Code, Cline, opencode**.
  ([docs.z.ai/devpack/tool/others](https://docs.z.ai/devpack/tool/others))

---

## Candidate evaluation (12+ harnesses)

Verified `gh api` 2026-06-23. "GLM fit" weighs endpoint flexibility, GLM-specific
tuning, and community evidence. "Bar" applies the repo's license-adoption bar
(MIT-like permissive only) + maintenance.

| Harness | Slug | License | Endpoint fit for GLM | GLM-specific evidence | Catalog status | Verdict for this use |
|---------|------|---------|----------------------|------------------------|----------------|----------------------|
| **opencode** | `anomalyco/opencode` | MIT ✓ | OpenAI- + Anthropic-compat, custom providers | "GLM-5.2 on opencode: impressed" (DEV.to); Z.ai-listed | discovery-log (eval CONDITIONAL) | **ADOPT-candidate (OSS)** — needs MEASURED |
| **Claude Code** | `anthropics/claude-code` | **NONE (proprietary)** ✗ | Anthropic-compat (native) | Z.ai's #1 documented integration | not catalogued (it's the baseline) | **Use, don't stack-adopt** (fails license bar) |
| **oh-my-pi / omp** | `can1357/oh-my-pi` | MIT ✓ | OpenAI-compat + 40+ providers | **Ships explicit GLM-coding-plan tuning** | **SKIP** (replaces Claude Code) | **Re-evaluate** — dark horse |
| **Cline** | `cline/cline` | Apache-2.0 ✓ | OpenAI-compat | Best-documented GLM tuning + the fix | discovery-log (SOURCE-ONLY) | Strong (VS Code); reference playbook |
| **Kilo Code** | `Kilo-Org/kilocode` | MIT ✓ | OpenAI-compat | Published own GLM-4.6 analysis | discovery-log (eval CONDITIONAL) | Good (in-editor) |
| **Goose** | `aaif-goose/goose` | Apache-2.0 ✓ | OpenAI- + Anthropic-compat | Z.ai-listed; MCP-heavy | discovery-log (eval CONDITIONAL) | Good (MCP workflows) |
| **OpenHands** | `OpenHands/OpenHands` | **NOASSERTION** ⚠ | OpenAI-compat (LiteLLM) | **Z.ai benchmarks GLM-5.2 on OpenHands** | catalogued (platform) | Strong for autonomous SWE; **confirm license** before adopt |
| **aider** | `Aider-AI/aider` | Apache-2.0 ✓ (pushed 2026-05) | OpenAI-compat (LiteLLM) | Works via generic config; fewer tool-call horror stories | referenced, no eval | Solid for diff/git flows |
| **Qwen Code** | `QwenLM/qwen-code` | Apache-2.0 ✓ | OpenAI-compat, multi-protocol | Off-label for GLM (tuned for Qwen) | discovery-log (eval CONDITIONAL) | Deprioritize — not GLM-first |
| **Crush** | `charmbracelet/crush` | **FSL-1.1-MIT (NOASSERTION)** ✗ | OpenAI-compat | GLM via community requests | **not catalogued (gap)** | **EXCLUDE** — non-permissive (FSL) |
| **Roo Code** | `RooCodeInc/Roo-Code` | Apache-2.0 but **ARCHIVED** ✗ | OpenAI-compat | Same caveats as Cline | catalogued | **EXCLUDE** — archived/unmaintained |
| **Gemini CLI** | `google-gemini/gemini-cli` | Apache-2.0 | **Gemini-only** ✗ | No real GLM path | discovery-log (eval CONDITIONAL) | **EXCLUDE** — vendor-locked |
| **grok-cli** | `superagent-ai/grok-cli` | MIT | **xAI Grok only** ✗ | None | discovery-log | **EXCLUDE** — vendor-locked |
| Cursor / Droid / TRAE / Qoder | — | **proprietary** ✗ | OpenAI-compat | Z.ai-listed | n/a | **EXCLUDE** — proprietary |

### Bridges (if you must run Claude Code → GLM through a proxy)
Permissive routers that sit between an Anthropic/OpenAI-shaped harness and GLM:
**`ccs`** (`kaitranntt/ccs`, MIT — names GLM explicitly), **`claude-code-router`**
(`musistudio/claude-code-router`, MIT — Z.ai-sponsored, exports `ANTHROPIC_BASE_URL`),
**`litellm`** (MIT, the standard gateway). Note: routing Claude-tuned agentic traffic
to a weaker model has an **unmeasured correctness cost** — prefer Z.ai's native
endpoints over a proxy where possible.

---

## Exclusions (strict)

- **Crush** — FSL-1.1-MIT is *source-available, not permissive* (time-limited
  non-compete before it converts to MIT). Fails the MIT-like bar. Keep as a UX
  reference; do not adopt. *(Also a catalog gap — not currently listed.)*
- **Roo Code** — Apache-2.0 but the repo is **archived** (last push 2026-05-15).
  Unmaintained → exclude; prefer Cline (its upstream lineage).
- **Cursor / Droid (Factory) / TRAE / Qoder / Eigent** — proprietary; can't adopt
  under a permissive-OSS bar even though they support GLM.
- **Gemini CLI / grok-cli** — vendor-locked to Gemini / Grok; no real GLM path.
- **Qwen Code** — permissive and capable, but tuned for Qwen; GLM is off-label. Not
  "best harness for GLM."

## Evidence & limitations

- **No hands-on run against GLM-5.2** (no Z.ai key provisioned). All GLM-fit claims
  are source-grounded; treat as REVIEW.
- **Unconfirmed:** GLM-5.2 open-weights license (MIT per secondary sources, not on
  the official model page); OpenHands and Crush show `NOASSERTION` on GitHub —
  confirm the actual license text before any adoption.
- Benchmarks cited are Z.ai's own figures (SWE-bench **Pro**, not Verified).

## Recommended next steps

1. **MEASURED eval** (`evaluations/TEMPLATE.md`) of **opencode** and **oh-my-pi** on
   GLM-5.2 via the **OpenAI-compat coding endpoint with exacto-class routing** — same
   task on both, scoring tool-call success rate, edit accuracy, and cost. This is what
   would graduate a recommendation here into a catalog ADOPT verdict.
2. **Re-examine oh-my-pi's SKIP** verdict in light of its explicit GLM tuning.
3. **Catalog gap:** `charmbracelet/crush` is uncatalogued — add it (with a non-OSS/FSL
   note) so the exclusion is recorded, or deliberately skip-with-reason.
4. If a proprietary CLI is acceptable, the **practical** answer needs no eval:
   Claude Code + GLM Coding Plan, two-line `ANTHROPIC_BASE_URL` config.

## Sources

- [docs.z.ai/guides/llm/glm-5.2](https://docs.z.ai/guides/llm/glm-5.2) ·
  [docs.z.ai/devpack/tool/claude](https://docs.z.ai/devpack/tool/claude) ·
  [docs.z.ai/devpack/tool/others](https://docs.z.ai/devpack/tool/others) ·
  [docs.z.ai/devpack/overview](https://docs.z.ai/devpack/overview)
- [Cline: commitment to open source + GLM-4.6](https://cline.bot/blog/cline-our-commitment-to-open-source-zai-glm-4-6)
- [DEV.to: testing GLM-5.2 on opencode](https://dev.to/danielbergholz/testing-glm-52-on-opencode-im-impressed-1780)
- [HuggingFace: GLM-5.2 blog (OpenHands benchmark)](https://huggingface.co/blog/zai-org/glm-52-blog)
- [VentureBeat: GLM-5.2 beats GPT-5.5 for 1/6 the cost](https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost)
- [oh-my-pi models doc](https://github.com/can1357/oh-my-pi/blob/main/docs/models.md) ·
  [crush FSL discussion](https://github.com/charmbracelet/crush/discussions/1482)
