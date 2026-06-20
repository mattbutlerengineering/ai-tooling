# Evaluation: Vet (Verify Everything)

**Repo:** [imbue-ai/vet](https://github.com/imbue-ai/vet)
**Stars:** 476 | **Last updated:** 2026-06-10 (pushed) | **License:** AGPL-3.0 | **Language:** Python (PyPI: `verify-everything`)
**Dev loop stage:** Code Review & Quality / Verify
**Layer:** Tooling (CLI + agent skill + CI)

---

## What it does

Vet (by [Imbue](https://imbue.com)) is **a standalone verification tool for code changes and coding-agent behavior** — "find issues worth your attention." It **reviews intent and code**: it checks agent *conversations* for goal adherence and code *changes* for correctness. It **runs anywhere** — from the terminal, as an agent skill (auto-runs after code changes to flag issues and request/action mismatches), or in CI. It's **bring-your-own-model** (any provider via your keys), works with existing **Anthropic/OpenAI subscriptions** (`--agentic`), and is **free/open source** (AGPL-3.0) with no account, fees, or data collection — requests go directly to your inference provider. The skill installs across `.agents/`, `.opencode/`, `.claude/`, and `.codex/` skill directories (project or user level), so multiple agents discover it.

## How we tested it

**Source-grounded inspection — not installed, not run.** No changes verified, no agent session exported.

```bash
gh api repos/imbue-ai/vet --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 476, AGPL-3.0, pushed 2026-06-10
gh api repos/imbue-ai/vet/readme --jq '.content' | base64 -d | head -60               # reviews intent+code, runs anywhere, BYO-model, skill install
```

## What worked

- **Verifies intent *and* code — not just the diff.** Checking the agent *conversation* for goal adherence (did it do what the user asked?) alongside code correctness targets the failure mode pure diff-review misses: confidently-wrong work that drifts from the request. This is the distinctive idea.
- **Independent verifier.** A separate tool reviewing the agent's behavior is exactly the "evidence before completion" discipline good workflows preach — and harder for the agent to rationalize past than self-review.
- **Runs everywhere, auto-triggers.** Terminal, CI, or an agent skill that proactively runs after changes; cross-installs for Claude Code/Codex/OpenCode so it's agent-agnostic.
- **BYO-model, no data collection.** Uses your keys/subscriptions, requests go straight to your provider, no account — privacy-friendly and cheap if you already pay for a model.
- **Credible origin.** Imbue is a serious AI-research lab; the framing ("verify everything") is principled.

## What didn't work or surprised us

- **AGPL-3.0.** Strong copyleft — fine for a dev-time tool you run, but a consideration if embedded into a product/service.
- **Lower traction (476 stars).** Younger/smaller than the review incumbents; less battle-tested than code-review/pr-review-toolkit.
- **Verification costs inference.** Reviewing intent + code per change is model calls; cheap on a subscription but not free, and adds a step.
- **Quality is model-bound.** "Find issues worth your attention" depends on the chosen model's judgment; false-positive/negative rate unverified here.
- **Overlaps the review field.** Conceptually near code-review/pr-review-toolkit/brooks-lint; the wedge is intent-adherence + agent-behavior verification, not code-only review.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Independently checks diffs for correctness *and* whether the agent did what was asked — catches goal drift. |
| Speed | neutral | Auto-running after changes adds a verification step; faster than discovering drift in review/prod. |
| Maintainability | + | Catches request↔action mismatches early, before wrong work compounds. |
| Safety | + | An independent verifier of agent behavior is a guard against over-claimed/incorrect completion. |
| Cost Efficiency | neutral | Free/AGPL, BYO-model; per-change verification consumes inference (cheap on a subscription). |

## Verdict

**CONDITIONAL** — Vet is a principled, Imbue-built **independent verifier** whose distinctive value is checking **both** the diff for correctness **and** the agent conversation for goal adherence — catching the "confidently did the wrong thing" failure that code-only review misses. Adopt it as an auto-running agent skill (or CI step) when you want an outside check on agent behavior, not just its output, and you're comfortable with AGPL-3.0 and BYO-model inference. It's CONDITIONAL given lower traction (476 stars), the AGPL license, and model-dependent judgment quality. It complements rather than replaces diff-reviewers: pair it with code-review/pr-review-toolkit for code rigor and let Vet own intent-adherence.

Compared to neighbors: **code-review**/**pr-review-toolkit** review the diff across dimensions; **brooks-lint** reviews for design decay. Vet's distinguishing pitch is **verifying coding-agent behavior (goal adherence) alongside code correctness, runnable as a terminal/CI/skill, BYO-model.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vet](https://github.com/imbue-ai/vet) | tool | Standalone verification for code changes AND coding-agent behavior (Imbue, AGPL-3.0) — checks agent conversations for goal adherence and diffs for correctness; runs from the terminal, as an agent skill (auto-runs after changes), or in CI; BYO-model | Agents drift from the user's request and ship subtly wrong code; want an independent verifier of both intent-adherence and correctness | code-review, pr-review-toolkit, brooks-lint |
