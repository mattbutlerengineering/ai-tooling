# Evaluation: textgrad

**Repo:** [zou-group/textgrad](https://github.com/zou-group/textgrad)
**Stars:** ~3,600 | **Last updated:** 2025-07-25 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect (optimization / Outer Loop)
**Layer:** Tooling

---

## What it does

An autograd engine for *textual* gradients. TextGrad implements backpropagation through natural-language feedback provided by LLMs: it builds a computation graph, and where PyTorch would pass numeric gradients, TextGrad passes LLM-generated critique ("gradients") backward to improve each node against a textual loss. Published in Nature (2025).

Mechanically the API mirrors PyTorch — if you know PyTorch you know ~80% of TextGrad. You define variables (prompts, solutions, code, even molecules), a forward pass that produces an output, a textual loss, and then call backward; an LLM "backward engine" critiques and the optimizer rewrites the variables. It now runs on a litellm-backed engine (`get_engine("experimental:gpt-4o")` / `set_backward_engine(...)`), so any litellm-supported provider (OpenAI, Anthropic/Bedrock, Together, Gemini, …) works, with optional caching. Use cases in the repo include prompt optimization, solution refinement, and code/molecule optimization.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README, the PyTorch-analogous API, the litellm engine integration, and the Nature publication reference. Confirmed the backward-engine/optimizer loop, the multi-provider support via litellm, and the breadth of optimizable artifacts (prompts/solutions/code/molecules). Note the repo's last push is mid-2025 — stable research code rather than an actively iterated product. Not run on a live optimization task, so condition-gated.

```bash
gh api repos/zou-group/textgrad --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/zou-group/textgrad/readme --jq '.content' | base64 -d
```

## What worked

- **Principled, familiar abstraction.** The PyTorch-like autograd metaphor makes a fuzzy task (prompt/solution tuning) systematic and composable, with a low learning curve for ML engineers.
- **Peer-reviewed.** A Nature paper is unusually strong validation for a prompt-optimization framework — the method is credible, not just a clever README.
- **Provider-agnostic via litellm.** Works across providers and supports caching, so you can optimize with one model and run with another.

## What didn't work or surprised us

- **Optimization is token-expensive.** Each backward pass is an LLM critique call; non-trivial graphs and iteration counts add up — this is a dev-time/research tool, not a hot-path component.
- **Maintenance cadence is slow.** Last push ~2025-07; the new litellm engines are described as experimental with the old engines being deprecated.
- **Niche audience.** Most catalog users want eval (promptfoo/giskard/ragas) or runtime self-evolution (ACE); TextGrad is the deliberate, graph-based optimizer in between.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Systematic optimization of prompts/solutions against a textual loss |
| Speed | - | Each backward pass is an LLM call; iteration is slow/expensive |
| Maintainability | neutral | Familiar API, but slow upstream cadence and experimental engines |
| Safety | neutral | Optimization tool; no safety mechanism either way |
| Cost Efficiency | - | Token-heavy optimization loops; mitigated by caching |

## Verdict

**CONDITIONAL**

Reach for TextGrad when you have a measurable textual objective and want to optimize prompts, solutions, or code systematically rather than by hand — and you can absorb the token cost of the optimization loop. For routine prompt iteration, an eval harness (promptfoo) plus manual edits is cheaper; for runtime self-improvement, ACE/evolver fit better. Strong credibility (Nature) but watch the slow maintenance cadence.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [textgrad](https://github.com/zou-group/textgrad) | framework | Textual-gradient optimization (MIT, published in Nature) — a PyTorch-like autograd engine where LLMs backpropagate natural-language critique to optimize prompts, solutions, code, or molecules against a textual loss; litellm-backed | Prompt/solution tuning is ad-hoc and manual; want a principled, differentiable-by-text optimization loop | opik, giskard-oss, ragas, ACE |
