# Evaluation: garak

**Repo:** [NVIDIA/garak](https://github.com/NVIDIA/garak)
**Stars:** ~8,150 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Verify (security red-teaming)
**Layer:** Tooling

---

## What it does

An LLM vulnerability scanner from NVIDIA — "Generative AI Red-teaming & Assessment Kit." The README's own analogy: if you know `nmap` or Metasploit, garak does similar things but for LLMs.

Mechanically, garak runs a battery of **probes** against a target model and uses **detectors** to decide whether each probe succeeded in making the model fail. It combines static, dynamic, and adaptive probes covering prompt injection, jailbreaks, data leakage, hallucination, misinformation, toxicity generation, and more. Targets are pluggable: Hugging Face Hub generative models, OpenAI chat/completion, AWS Bedrock, Replicate, litellm (so anything litellm supports), local gguf models via llama.cpp, and "pretty much anything accessible via REST." Output is a structured report of which attack classes the model is susceptible to.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented probe/detector model and target list. Confirmed the nmap-style probe→detector design, the breadth of attack classes, and the multi-backend target support (HF/OpenAI/Bedrock/Replicate/litellm/REST/gguf). Not run against a live model — a real scan needs a target endpoint/keys and meaningful runtime — so verdict is condition-gated.

```bash
gh api repos/NVIDIA/garak --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/NVIDIA/garak/readme --jq '.content' | base64 -d
```

## What worked

- **Systematic, scriptable red-teaming.** A standard probe/detector battery replaces ad-hoc "try a few jailbreaks" spot checks — repeatable in CI and comparable across models.
- **Backend-agnostic.** Works against hosted APIs, Bedrock, local gguf, or any REST endpoint, so you can scan the exact model/config you ship.
- **Credible provenance.** NVIDIA-maintained, Apache-2.0, DEF CON-presented; this is a serious security tool, not a toy.

## What didn't work or surprised us

- **It's an assessment tool, not a fix.** garak tells you *where* a model fails; remediation (guardrails, prompt hardening) is on you.
- **Runtime/cost.** Comprehensive probe runs make many model calls — budget time and tokens, especially against paid APIs.
- **Overlaps promptfoo's red-teaming.** promptfoo also does vulnerability scanning; garak is the deeper, security-specialist probe library, promptfoo the broader eval+red-team CLI.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Surfaces hallucination/misinformation failure modes pre-ship |
| Speed | neutral | Adds a scanning stage; not a runtime change |
| Maintainability | + | Repeatable, comparable security baselines across model changes |
| Safety | + | Directly targets injection, jailbreak, and data-leakage risks |
| Cost Efficiency | - | Thorough scans make many (possibly paid) model calls |

## Verdict

**discovery-log — tentative read**

Adopt when you ship an LLM-backed feature and need a real, repeatable security assessment (prompt injection, jailbreaks, data leakage) rather than spot checks — ideally gated in CI before model/prompt changes go live. For lighter needs, promptfoo's red-team mode may suffice; reach for garak when you want NVIDIA's specialist probe depth.

## Triage note

Left at `discovery-log`, not SKIPped — the banding is a category error. `SkillSpector` (STACK)
scans third-party *skill packages* for prompt injection before you install them. garak red-teams a
*model endpoint* you ship — jailbreaks, data leakage, hallucination, toxicity — with a specialist
probe suite. One protects the agent from what it installs; the other protects users from what you
deploy. Neither substitutes for the other.

It is not a P0 candidate for this stack for a scope reason rather than a quality one: garak earns
its keep when you ship an LLM-backed feature and gate model/prompt changes in CI. This catalog's
loop is AI-assisted *development*, where that endpoint does not exist.

Apache-2.0, NVIDIA-maintained, ★8.4K, actively pushed. The right row to keep and the right tool to
reach for the moment an LLM feature ships; `promptfoo`'s red-team mode is the lighter first step.

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [garak](https://github.com/NVIDIA/garak) | tool | LLM vulnerability scanner (Apache-2.0, by NVIDIA) — "nmap for LLMs": static/dynamic/adaptive probes for prompt injection, jailbreaks, data leakage, hallucination, toxicity against HF/OpenAI/Bedrock/litellm/REST/gguf | Need to systematically red-team an LLM for known failure modes before shipping, not ad-hoc spot checks | promptfoo, giskard-oss, SkillSpector, ghostsecurity/skills |
