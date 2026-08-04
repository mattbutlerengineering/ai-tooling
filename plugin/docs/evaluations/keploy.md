# Evaluation: keploy

**Repo:** [keploy/keploy](https://github.com/keploy/keploy)
**Stars:** ~17,600 | **Last updated:** 2026-06-20 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
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

**discovery-log — tentative read**

Adopt to bootstrap integration/API test coverage from real traffic with zero code changes — especially valuable as a regression net over code an agent generated. Mind that captured tests encode current behavior (curate them) and that eBPF capture has platform requirements. Pairs well with aimock (deterministic AI-dependency mocks) and unit-level TDD (tdd-guard).

## Triage note

Left at `discovery-log`, not SKIPped — the banding is a category error. `stryker-js` (STACK)
mutation-tests existing tests to ask whether they would catch a bug; keploy uses eBPF to record
real API calls, DB queries and queue traffic at the network layer and replay them as tests. One
grades a suite you already wrote; the other *creates* the suite from traffic, with no code changes
and no SDK. They compose — mutation-test what keploy captured — rather than compete.

The reason it is worth a real look is the framing in its own evaluation: a regression net over code
an agent generated. Agent-written code is exactly where a from-traffic behavioural snapshot is most
valuable, because nobody hand-wrote the invariants.

Open questions a bulk pass cannot settle: captured tests encode *current* behaviour including its
bugs, so they need curating, and eBPF capture has platform requirements worth confirming before it
goes in a loop. Apache-2.0, ★18K, actively pushed.

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [keploy](https://github.com/keploy/keploy) | tool | Auto-generate API/integration tests from real traffic (Apache-2.0, ★18K) — eBPF records API calls, DB queries (Postgres/MySQL/Mongo), and queues (Kafka/RabbitMQ) at the network layer, replays as code-less tests + data-mocks; language-agnostic | Writing/maintaining integration tests and mocks is slow; want coverage auto-captured from real traffic with zero code changes | aimock, scenario, tdd-guard, stryker-js |
