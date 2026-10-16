# Evaluation: ralph-claude-code

**Repo:** [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)
**Stars:** 9,584 | **Last updated:** 2026-07-18 | **License:** MIT
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement (autonomous)
**Layer:** Tooling

---

## What it does

Autonomous AI development loop for Claude Code with intelligent exit detection. Wraps Claude Code in a persistent loop that reads tasks from `.ralph/PROMPT.md`, executes iteratively, and exits only when a dual-condition gate (completion indicators + explicit EXIT_SIGNAL) is satisfied. Includes rate limiting (100 calls/hour), circuit breaker, tmux dashboard, Docker sandboxing, GitHub Issues import/sync, and batch processing with dependency tracking.

## How we tested it

**Evidence:** RUN

**Hands-on** — installed it via `bash install.sh` (HEAD `4fd2fe9`, 2026-10-10) into an isolated `$HOME`, enabled it in three throw-away git repos with `ralph-enable-ci`, and ran the real `ralph` loop (`ralph_loop.sh`) against a scripted stand-in for the `claude` CLI (`CLAUDE_CODE_CMD`), one scenario per repo. The stand-in emits Claude-CLI-style JSON containing a `---RALPH_STATUS---` block and counts how many times the loop calls it. The loop, rate limiter, response analyzer, exit gate and circuit breaker are Ralph's own code; only the model is replaced.

```
mode=complete    (iter 1 commits a file, STATUS: COMPLETE, EXIT_SIGNAL: true)
  stub_calls=2   wall=38s  -> "Exit condition: Multiple completion signals (2 >= 2)" / "Graceful exit triggered"
mode=impossible (no file change, STATUS: IN_PROGRESS, EXIT_SIGNAL: false, TESTS_STATUS: FAILING)
  stub_calls=3   wall=50s  -> "Circuit breaker opened - halting execution" (Reason: No recovery, opening circuit after 3 loops)
                              ralph --circuit-status: State OPEN, Loops since progress: 3
mode=churn      (commits a file every iteration, EXIT_SIGNAL: false, FILES_MODIFIED: 1)
  stub_calls=11  at the 170s harness cap -> never exited on its own; only my timeout stopped it
baseline: naive `for` loop around the same stand-in with no stop logic -> ran all 6 iterations requested (stop is the caller's problem)
```

Documented commands checked on the installed build: `ralph run --docker --issue <url>` and `ralph status` (the invocations the previous revision of this eval listed) both answer `Unknown option`; the real forms in `ralph --help` are `--sandbox docker`, `--github-issue REF` and `--status`.

## Test design

- **Task/corpus:** three deterministic scenarios (clean completion, a task that cannot make progress, endless refactoring with visible file changes), each in a fresh git repo set up by `ralph-enable-ci`. The model is a bash stub (`claude` that prints the scripted JSON after a 3s sleep); it is a fixture for the loop controls, not a coding agent.
- **Baseline:** a naive `for i in 1..6` loop calling the same stub with no exit detection, plus the stub call counts as the cost proxy (each real call would be one full agent session).
- **Metric:** stub invocations before the loop stops, and the stop reason Ralph prints; wall-clock as printed by the harness.
- **Reproduce:** `bash install.sh` with `HOME` redirected, `ralph-enable-ci` in a fresh repo, then `STUB_MODE=<mode> CLAUDE_CODE_CMD=<stub> ralph --timeout 1 -c 100` (stub source: 14 lines of bash emitting a status block via `jq -nc`).

## What worked

- Exit gate stops a finished task: completion plus `EXIT_SIGNAL: true` ended the run after 2 calls, with the reason printed.
- Circuit breaker stops a stuck task: three consecutive loops with zero changed files and `EXIT_SIGNAL: false` opened the breaker after 3 calls; state persists and `ralph --circuit-status` reports it, `--reset-circuit` is the documented way back.
- Install is a single script with a dependency check (node, jq, git, timeout) and a `~/.local/bin` PATH reminder; `ralph-enable-ci` is non-interactive and works in a repo with no prior setup.
- The rate limit (`MAX_CALLS_PER_HOUR=100`) and the thresholds (`CB_NO_PROGRESS_THRESHOLD=3`, `CB_SAME_ERROR_THRESHOLD=5`) are plain `.ralphrc` values.

## What didn't work or surprised us

- Churn never stops itself: with a file changing every iteration and `EXIT_SIGNAL: false`, 11 calls ran in 170s and the loop only ended when the harness killed it. The circuit breaker keys on lack of progress, so visible activity that never converges is bounded only by `MAX_CALLS_PER_HOUR` and the operator. This is the expensive failure mode of an unattended loop.
- A finished task costs one extra call: the gate wanted two completion signals (`MAX_CONSECUTIVE_DONE_SIGNALS=2`), so a one-shot task was invoked twice.
- A call that returns in under about a second is classified "Claude Code process exited immediately" and retried after a 30s wait, even with valid JSON and exit code 0. Real responses are slower than that; it cost three false starts in my first stub.
- The stand-in is the main limit of this run: nothing here shows how often a real model emits a correct `EXIT_SIGNAL`, so the previous revision's claims (exit detection failed 1 of 5 runs, 7 iterations against 3-4 by hand, 30s Docker startup) are unsupported here and have been removed rather than carried forward.
- Docker sandboxing (`--sandbox docker`), the tmux dashboard, GitHub issue sync and the PR-creation flags were outside this run (no Docker daemon, no model credentials, no tracked issue); the safety claims about them rest on the README only.
- The README bullet for starting a run in the previous revision of this eval named flags that do not exist in the current CLI.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Output quality comes from the model; Ralph only decides when to stop, and its stop decisions were right in 2 of 3 scenarios (churn never stopped) |
| Speed | +/- | Saves attended time, adds one confirmation call after completion; 30s retry wait on sub-second returns |
| Maintainability | neutral | Plain bash plus `.ralphrc`; no effect on the code produced |
| Safety | + (unverified for the sandbox) | Circuit breaker and call cap measured; the container isolation was not exercised |
| Cost Efficiency | +/- | Stopped an unproductive loop at 3 calls instead of unbounded; a finished task still pays 2 calls and a churning one pays until the hourly cap |
| Verifiability | + | The stop reason is printed in the log and the breaker state is queryable (`--circuit-status`), so a reviewer can see why a run ended |

## Verdict

**discovery-log — tentative read** — the loop controls behave as documented on two of three scripted scenarios (finish after 2 calls, halt a stuck task after 3) and fail open on endless visible churn (11 calls, no stop); with a stand-in for the model and no sandbox run, this does not support a real verdict. A real read needs one attended run with a live model on a task that cannot succeed, and a Docker-sandbox run.

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
