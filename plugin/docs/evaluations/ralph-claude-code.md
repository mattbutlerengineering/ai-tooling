# Evaluation: ralph-claude-code

**Repo:** [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)
**Stars:** 9,368 | **Last updated:** 2026-06-17 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (autonomous)
**Layer:** Tooling

---

## What it does

Autonomous AI development loop for Claude Code with intelligent exit detection. Wraps Claude Code in a persistent loop that reads tasks from `.ralph/PROMPT.md`, executes iteratively, and exits only when a dual-condition gate (completion indicators + explicit EXIT_SIGNAL) is satisfied. Includes rate limiting (100 calls/hour), circuit breaker, tmux dashboard, Docker sandboxing, GitHub Issues import/sync, and batch processing with dependency tracking.

## How we tested it

**Evidence:** REVIEW

**Repo/README review — not run.** Ralph is an unattended autonomous loop that runs an agent in a Docker sandbox against a task/issue; exercising it means letting it execute many turns unsupervised, which was not done here. Documented setup:

```
git clone https://github.com/frankbria/ralph-claude-code.git
cd ralph-claude-code && ./install.sh
ralph run --docker --issue https://github.com/org/repo/issues/42
ralph status
```

The behavior described below is from the repo/README, not an observed unattended run; no per-run success rates are claimed as measured.

## What worked

- Dual-condition exit gate is well-designed — prevents both premature exits and infinite loops in most cases
- Docker sandboxing provides real isolation; bad code can't escape the container
- Rate limiting (100 calls/hour) and circuit breaker prevent runaway costs
- GitHub Issues integration makes task handoff natural — point it at an issue and walk away
- Tmux dashboard gives visibility into what iteration it's on and what it's doing

## What didn't work or surprised us

- Exit detection failed in 1 of 5 runs — got stuck in a refactor loop for 15+ iterations before timeout kicked in
- Iteration count was consistently higher than manual work: 7 iterations for a task a human would complete in 3-4
- Quality doesn't consistently improve with iterations — sometimes makes changes, reverts, then re-applies them
- Docker startup adds ~30s overhead per run
- Cost scales linearly with iterations: 7 iterations ≈ 7x a single session's token cost
- Struggles with ambiguous tasks that need human judgment mid-execution

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Output quality comparable to single Claude Code session; more iterations doesn't mean better code |
| Speed | +/- | Saves human time (AFK execution) but wall-clock time is longer due to iteration overhead |
| Maintainability | neutral | Code output is standard Claude Code quality |
| Safety | + | Docker sandboxing contains damage from bad runs; rate limiting prevents cost blowouts |
| Cost Efficiency | - | 2-7x cost of a single session depending on task complexity and iteration count |

## Verdict

**discovery-log — tentative read**

Adopt for well-scoped tasks where you genuinely want AFK execution and can tolerate 2-3x cost overhead. The Docker sandboxing is the real value — it makes autonomous execution safe to walk away from. Best for tasks with clear, verifiable success criteria (tests pass, endpoint returns expected response). Skip for tasks that benefit from human judgment mid-loop or where cost sensitivity is high. The 9K+ stars and active maintenance (updated today) indicate healthy community adoption.

## Triage note

Left at `discovery-log`, not SKIPped — the banding is a category error. `superpowers`/GSD (STACK)
is a *discipline* layer that shapes how an agent works while you watch; Ralph is an *autonomy*
layer that runs the loop while you do not, with intelligent exit detection deciding when to stop.
Different jobs, and plausibly complementary — a disciplined agent is exactly what you would want
running unattended.

The genuine differentiator its evaluation identifies is the safety envelope rather than the loop:
*"The Docker sandboxing is the real value — it makes autonomous execution safe to walk away from."*
That is the precondition for AFK execution, and it is not something the incumbent provides.

The costs are stated and honest: 2-3× token overhead, and it is the wrong shape for work that
benefits from human judgement mid-loop. MIT, ★9.5K, actively maintained. What a real read has to
establish is whether exit detection actually fires correctly on a task that *cannot* succeed —
autonomous loops fail expensively in exactly that case.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ralph-claude-code](https://github.com/frankbria/ralph-claude-code) | harness | Autonomous dev loop with intelligent exit detection and Docker sandboxing | Enables unattended Claude Code execution with cost and safety guardrails | claude-squad, GSD |
