# Evaluation: keploy

**Repo:** [keploy/keploy](https://github.com/keploy/keploy)
**Stars:** ~17,600 | **Last updated:** 2026-06-20 | **License:** Apache-2.0
**Dev loop stage:** Verify (test generation)
**Layer:** Tooling

---

## What it does

A developer-centric API and integration testing tool that **auto-generates tests and data-mocks from real traffic** — faster than writing unit tests, and code-less. You run your app with `keploy record`, and it captures real API calls, database queries, and streaming events, then replays them as tests.

Mechanically, the differentiator is that it uses **eBPF to capture traffic at the network layer** — so there are no SDKs to add and no code changes, and it's language-agnostic. It records and replays complex, distributed API flows as mocks/stubs, and goes beyond HTTP mocking to virtualize databases (Postgres/MySQL/MongoDB), streaming/queues (Kafka/RabbitMQ), and external APIs ("complete infra-virtualization"). The result is high integration-test coverage derived from actual application behavior rather than hand-written cases.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented record/replay model. Confirmed the eBPF network-layer capture (no SDK/code changes), the language-agnostic positioning, the auto-generated tests + data-mocks, and the infra-virtualization breadth (DBs, queues, external APIs) beyond HTTP. The "faster than unit tests / 90% coverage" framing is marketing; the mechanism (record real flows → replay as tests) is sound. Not run against a live app, so condition-gated.

```bash
gh api repos/keploy/keploy --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/keploy/keploy/readme --jq '.content' | base64 -d
```

## What worked

- **Tests from real behavior, zero code changes.** eBPF capture means no SDK, no instrumentation, and language-agnostic coverage — a low-friction path to integration tests that reflect actual flows.
- **Infra-virtualization, not just HTTP mocks.** Recording DB queries and queue events (not only HTTP) makes the replayed tests far more faithful to real integration behavior.
- **Complements AI-generated code.** Auto-captured regression tests are a strong safety net for code an agent wrote and you don't fully trust.

## What didn't work or surprised us

- **Records what happens, including bugs.** Tests generated from traffic encode current behavior; if a flow is already wrong, the "test" enshrines it — you must curate captured cases.
- **eBPF/runtime constraints.** Network-layer capture has platform/permission requirements (Linux/eBPF); not a pure userspace drop-in everywhere.
- **Coverage-claim framing.** "90% coverage / faster than unit tests" is aspirational marketing; real value depends on how representative your captured traffic is.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Regression tests from real flows catch integration breakage |
| Speed | + | Auto-generates tests/mocks far faster than hand-writing them |
| Maintainability | + | Replayable mocks for DBs/queues stabilize integration tests |
| Safety | + | Regression net for AI-written code and refactors |
| Cost Efficiency | + | Free/OSS; saves substantial test-authoring effort |

## Verdict

**CONDITIONAL**

Adopt to bootstrap integration/API test coverage from real traffic with zero code changes — especially valuable as a regression net over code an agent generated. Mind that captured tests encode current behavior (curate them) and that eBPF capture has platform requirements. Pairs well with aimock (deterministic AI-dependency mocks) and unit-level TDD (tdd-guard).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [keploy](https://github.com/keploy/keploy) | tool | Auto-generate API/integration tests from real traffic (Apache-2.0, ★18K) — eBPF records API calls, DB queries (Postgres/MySQL/Mongo), and queues (Kafka/RabbitMQ) at the network layer, replays as code-less tests + data-mocks; language-agnostic | Writing/maintaining integration tests and mocks is slow; want coverage auto-captured from real traffic with zero code changes | aimock, scenario, tdd-guard, stryker-js |
