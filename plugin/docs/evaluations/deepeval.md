# Evaluation: deepeval

**Repo:** [confident-ai/deepeval](https://github.com/confident-ai/deepeval)
**Stars:** ~16,300 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Dev loop stage:** Verify / Reflect (LLM evaluation)
**Layer:** Tooling

---

## What it does

An open-source LLM evaluation framework — explicitly "Pytest, but specialized for unit testing LLM apps." From Confident AI.

Mechanically you write eval tests much like pytest cases: define test cases (input, actual output, optional expected output/context) and assert against **metrics**. DeepEval ships a large library of ready-to-use metrics — G-Eval (LLM-as-judge with custom criteria), task completion, answer relevancy, faithfulness, hallucination, contextual precision/recall, and more — each returning a score *and an explanation*. Metrics are powered by any LLM of your choice, statistical methods, or NLP models that run **locally on your machine**. It targets agents, RAG pipelines, and chatbots, integrates with LangChain/OpenAI/etc., and runs in CI to catch prompt drift and to compare models/prompts/architectures (e.g. deciding whether you can switch OpenAI→Claude safely). The optional Confident AI SaaS hosts results, reports, and iteration comparisons.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README, the pytest-analogy design, and the metrics catalog. Confirmed the test-case/metric model, the breadth of metrics (G-Eval, faithfulness, hallucination, task completion), the "metrics run locally / any-LLM-as-judge" property, and the CI + framework integrations. The optional Confident AI hosting is a separate paid layer. Not run on a live test suite, so condition-gated.

```bash
gh api repos/confident-ai/deepeval --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/confident-ai/deepeval/readme --jq '.content' | base64 -d
```

## What worked

- **Pytest mental model.** Framing evals as unit tests with assertions is immediately legible to engineers and slots into existing CI — low adoption friction.
- **Deep metric library with explanations.** G-Eval plus faithfulness/hallucination/relevancy metrics that each explain their score make failures actionable, not just a number.
- **Local-capable, model-agnostic judging.** Metrics can run with local NLP models or any LLM-as-judge, so you aren't forced into one provider or a paid backend.

## What didn't work or surprised us

- **LLM-as-judge cost/variance.** Judge-based metrics spend tokens and can be noisy; you'll want fixed judge models and thresholds for stable CI signals.
- **Gentle upsell to Confident AI.** The OSS framework is complete, but result hosting/reporting routes to the paid SaaS.
- **Overlaps promptfoo/ragas/giskard/opik.** deepeval's edge is the pytest ergonomics and metric breadth; choice depends on whether you want a test-framework feel (deepeval) vs. a config-driven CLI (promptfoo) vs. RAG-specific metrics (ragas).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Metric-driven evals catch hallucination/relevancy/faithfulness regressions |
| Speed | neutral | Adds an eval stage; judge calls add latency |
| Maintainability | + | Pytest-style suites in CI guard against prompt/model drift |
| Safety | + | Hallucination and faithfulness metrics flag unsafe outputs |
| Cost Efficiency | neutral | OSS framework free; LLM-judge metrics consume tokens |

## Verdict

**CONDITIONAL**

Adopt when you want LLM evals expressed as unit tests in CI — especially to validate model/prompt swaps and catch regressions on agents/RAG/chatbots. The pytest framing makes it the natural pick for test-driven teams; use the local/NLP metrics where possible to control cost, and pin judge models for stable signals. Overlaps existing eval tools (promptfoo, ragas, opik) — pick by ergonomics.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deepeval](https://github.com/confident-ai/deepeval) | framework | "Pytest for LLMs" (Apache-2.0, ★16K) — LLM eval framework with ready metrics (G-Eval, task completion, answer relevancy, hallucination, faithfulness) powered by any LLM/local NLP; unit-test agents/RAG/chatbots in CI | LLM apps regress silently on prompt/model changes; want pytest-style metric-driven evals to catch drift | promptfoo, ragas, giskard-oss, opik |
