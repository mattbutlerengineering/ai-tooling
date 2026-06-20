# Evaluation: TDD Guard

**Repo:** [nizos/tdd-guard](https://github.com/nizos/tdd-guard)
**Stars:** 2,205 | **Last updated:** 2026-06-16 (pushed) | **License:** MIT | **Language:** TypeScript (npm: `tdd-guard`; Claude Code plugin)
**Dev loop stage:** Code Review & Quality / Verify — enforces TDD during Implement
**Layer:** Tooling (Claude Code hook + test reporters)

---

## What it does

TDD Guard is **automated Test-Driven Development enforcement for Claude Code.** It runs as a hook: "when your agent tries to skip tests or over-implement, TDD Guard blocks the action and explains what needs to happen instead." Features: **test-first enforcement** (blocks implementation without a failing test), **minimal implementation** (prevents code beyond current test requirements), **lint integration** (enforces refactoring via your lint rules), customizable validation rules, a choice of faster vs. more-capable validation model, and mid-session toggle. It supports **9 test frameworks** (Vitest, Jest, Storybook, pytest, PHPUnit, Go, Rust, RSpec, Minitest) via community-contributed reporters. Install via the Claude Code plugin marketplace (`/plugin marketplace add nizos/tdd-guard` → install → `/tdd-guard:setup`). Roadmap: validate edits made through MCPs/shell, encourage meaningful refactors when green.

## How we tested it

**Source-grounded inspection — not installed, not run.** No hook wired in, no TDD violation triggered, blocking behavior not observed.

```bash
gh api repos/nizos/tdd-guard --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 2205, MIT, pushed 2026-06-16
gh api repos/nizos/tdd-guard/readme --jq '.content' | base64 -d | head -75               # enforcement features, frameworks, plugin install
```

## What worked

- **Mechanical enforcement, not a prompt.** The catalog (and most TDD "skills") *ask* the agent to write tests first; TDD Guard *blocks the tool call* when it doesn't. That's the difference between guidance and a guardrail, and it directly targets the most common agent failure mode (skipping/over-implementing).
- **Both halves of TDD.** It enforces test-first *and* minimal-implementation (no gold-plating beyond the current test), plus lint-driven refactor — covering red, green, and refactor rather than just "tests exist."
- **Broad framework support via community.** 9 frameworks across JS/TS, Python, PHP, Go, Rust, Ruby — contributed by many hands, a healthy sign.
- **Tunable + escapable.** Custom rules, ignore patterns, validation-model choice, and a mid-session toggle keep it from being a straitjacket; security workflow + audits are documented.
- **Clean install.** First-class Claude Code plugin with a setup skill.

## What didn't work or surprised us

- **Claude Code-specific.** It's a CC hook; not portable to other agents (unlike a generic skill).
- **Hook trust + a second model.** Hooks run with your permissions, and validation can call a model per action — a (small) cost and latency tax, and a config surface to get right.
- **Bypassable by design.** Agents can route around hooks via MCP/shell (the README's own roadmap flags MCP/shell validation as not-yet-done); "strengthening enforcement" docs exist precisely because determined agents can evade.
- **TDD is a methodology choice.** Teams that don't practice strict TDD will find it friction; it enforces a discipline, not a universal good.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Forces a failing test before implementation and blocks over-build — tests actually drive the code. |
| Speed | neutral / − | Slower per step (validation + write-test-first), faster overall if it prevents untested rework. |
| Maintainability | + | Enforced test-first + lint-driven refactor yields better-tested, smaller-diff code over time. |
| Safety | + | A hard guardrail against the agent skipping verification; security scanning on the project itself. |
| Cost Efficiency | neutral | MIT/free; per-action validation model adds some token cost (configurable to a cheaper model). |

## Verdict

**CONDITIONAL** — TDD Guard is the rare tool that turns "please write tests first" from a *request* into an *enforced guardrail*: a Claude Code hook that blocks implementation without a failing test and blocks over-implementation, across 9 test frameworks. Adopt it if your team genuinely practices TDD and wants the agent held to red-green-refactor mechanically rather than by hope — it's the enforcement layer the `tdd`/`test-driven-development` skills only advise. Accept that it's Claude-Code-specific, adds a small per-action validation cost, and (today) can be bypassed via MCP/shell paths. For teams that don't do strict TDD, it's friction by design.

Compared to neighbors: **stryker-js** is mutation testing (are your tests *good*?); **superpowers**' TDD skill *advises* test-first; **pr-review-toolkit** reviews after the fact. TDD Guard's distinguishing pitch is **blocking the agent in real time when it violates test-first/minimal-implementation discipline.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tdd-guard](https://github.com/nizos/tdd-guard) | plugin | Automated TDD enforcement for Claude Code (MIT) — a hook that blocks implementation without a failing test and over-implementation beyond current test requirements, with lint-driven refactor support; 9 test frameworks (Vitest/Jest/pytest/Go/Rust/RSpec/…) | Agents skip tests and over-build; want red-green-refactor discipline mechanically enforced, not just requested | stryker-js, superpowers (tdd skill), pr-review-toolkit |
