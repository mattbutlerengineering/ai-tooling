# Evaluation: scenario

**Repo:** [langwatch/scenario](https://github.com/langwatch/scenario)
**Stars:** ~900 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Verify (agent testing)
**Layer:** Tooling

---

## What it does

A simulation-based agent testing framework from LangWatch. Instead of asserting on a single response, Scenario **simulates a user** interacting with your agent across scenarios and edge cases, then lets you judge or assert at any point in the resulting multi-turn conversation.

Mechanically you describe a scenario in natural language (a `description` that guides the simulated user), integrate your agent by implementing a single `call()` method, and run `scenario.run(...)`. During the simulation you get powerful multi-turn control: custom assertions over conversation state — e.g. `assert state.has_tool_call("get_current_weather")` — and you can stop/judge at chosen points. It's deliberately eval-framework-agnostic (combine with any LLM eval or custom checks) and available in Python, TypeScript, and Go.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the example (a weather/boat-trip scenario asserting a `get_current_weather` tool call). Confirmed the simulated-user model, the one-method (`call()`) agent integration, the multi-turn assertion/judging API (`ScenarioState`, `has_tool_call`), the eval-framework-agnostic stance, and the Python/TS/Go availability. Not run against a live agent, so condition-gated.

```bash
gh api repos/langwatch/scenario --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/langwatch/scenario/readme --jq '.content' | base64 -d
```

## What worked

- **Tests behavior, not just outputs.** Simulating a user across turns catches failures (wrong tool, derailed conversation, missed edge case) that single-shot eval of one response can't.
- **Assert on the trajectory.** `state.has_tool_call(...)` and point-in-conversation judging target the things that actually break agents — tool usage and multi-turn flow.
- **Low-friction, polyglot, agnostic.** One `call()` method to integrate, works in Python/TS/Go, and composes with whatever eval framework (deepeval, promptfoo, custom) you already use.

## What didn't work or surprised us

- **Simulation cost/flakiness.** A simulated user is itself an LLM, so runs spend tokens and can be non-deterministic — you'll want seeded/judge-pinned configs for stable CI.
- **You design the scenarios.** Coverage is only as good as the scenarios/edge cases you write; it won't discover unknown failure modes on its own.
- **Younger project.** ~900 stars; smaller ecosystem than the eval-metric tools it complements.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Multi-turn user simulation catches behavioral/tool-use regressions |
| Speed | neutral | Adds a simulation stage; simulated-user calls add latency |
| Maintainability | + | Repeatable behavioral tests guard agents against drift |
| Safety | + | Can assert agents don't take wrong/unsafe actions in edge cases |
| Cost Efficiency | - | Simulated-user runs consume tokens per scenario |

## Verdict

**CONDITIONAL**

Adopt for testing multi-turn agents where behavior and tool usage — not just a single answer — are what matter, and pair it with metric evals (deepeval/promptfoo) for output quality. Pin judge/simulator models and seed scenarios for stable CI signals. The simulation token cost is the price for catching trajectory-level bugs that single-response evals miss.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [scenario](https://github.com/langwatch/scenario) | framework | Simulation-based agent testing (Apache-2.0, by LangWatch) — simulates users across scenarios/edge cases with multi-turn control to judge/assert at any conversation point (e.g. `has_tool_call`); eval-agnostic, one `call()` to integrate; Python/TS/Go | Agents pass unit tests but break in real multi-turn conversations; want repeatable user-simulation tests with trajectory assertions | promptfoo, deepeval, vet, tdd-guard |
