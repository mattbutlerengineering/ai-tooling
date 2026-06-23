# Evaluation: aimock

**Repo:** [CopilotKit/aimock](https://github.com/CopilotKit/aimock)
**Stars:** ~630 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Verify (test infrastructure)
**Layer:** Tooling

---

## What it does

Mock infrastructure for testing AI applications. aimock (the class is still `LLMock` after the v1.7.0 rename from `@copilotkit/llmock`) runs a single local server that mocks *everything* an AI app talks to: LLM chat/completion APIs, embeddings, image/audio/video generation, transcription/TTS/translation, MCP tools, A2A agents, AG-UI event streams, vector databases, search, rerank, and moderation — "one package, one port, zero dependencies."

Mechanically you construct a mock (`new LLMock({ port: 0 })`), program canned responses (`mock.onMessage("hello", { content: "Hi there!" })`), start it, then point your SDK at it by setting the provider base URL/key to the mock before constructing the client (e.g. `OPENAI_BASE_URL=${mock.url}/v1`). Your tests then run fully offline and deterministically, with no real API calls and no surprise bills. The README explicitly warns that env vars must be set *before* the SDK client is constructed, since many SDKs cache the base URL at construction.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the quick-start code. Confirmed the single-server/single-port design, the breadth of mocked AI surfaces (LLM/embeddings/media/MCP/A2A/AG-UI/vector DB/search/rerank/moderation), the base-URL-redirect integration pattern, and the construction-order caveat. Verified the package rename history (`llmock` → `aimock`). Not wired into a live test suite, so condition-gated.

```bash
gh api repos/CopilotKit/aimock --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/CopilotKit/aimock/readme --jq '.content' | base64 -d
```

## What worked

- **Deterministic, offline, no-bill tests.** Programmed responses make AI-dependent tests fast and repeatable, and eliminate the flakiness and cost of hitting real providers in CI.
- **Breadth on one port.** Mocking not just the LLM but embeddings, MCP tools, A2A, AG-UI streams, and vector DBs covers the whole modern agent stack from a single dependency.
- **Drop-in via base URL.** No code changes beyond redirecting the provider base URL — works with standard OpenAI-format SDKs.

## What didn't work or surprised us

- **Footgun: construction order.** If the client is built before the env vars are set, it talks to the *real* API (surprise bills) — the README flags this, but it's an easy mistake.
- **Mocks ≠ real behavior.** Canned responses test your app's plumbing/branching, not real model quality — complements eval tools (deepeval/scenario), doesn't replace them.
- **Younger/niche.** ~630 stars; the value shows up specifically in AI-app test suites, not general development.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Deterministic mocks test app branching/error handling reliably |
| Speed | + | Offline tests run fast with no network round-trips |
| Maintainability | + | Stable, repeatable CI for AI-dependent code paths |
| Safety | neutral | Test infra; no runtime safety effect |
| Cost Efficiency | + | Zero API spend in tests (when wired correctly) |

## Verdict

**CONDITIONAL**

Adopt when you have an AI/agent app and want fast, deterministic, zero-cost tests of its plumbing — request handling, branching, error paths, tool wiring — without hitting real providers. Mind the env-var-before-client construction caveat. Pair with behavioral/eval tools (scenario, deepeval) which test real model quality; aimock tests everything around the model.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [aimock](https://github.com/CopilotKit/aimock) | tool | Mock infrastructure for AI-app testing (MIT, by CopilotKit) — one zero-dependency local server mocks LLM APIs, embeddings, media gen, MCP tools, A2A, AG-UI streams, vector DBs, search/rerank/moderation; redirect your SDK base URL for deterministic offline tests | LLM/agent tests hit real APIs — flaky, slow, expensive; want deterministic mocked AI dependencies on one port | scenario, promptfoo, deepeval |
