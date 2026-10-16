# Evaluation: sandcastle

**Repo:** [mattpocock/sandcastle](https://github.com/mattpocock/sandcastle)
**Stars:** 7,210 | **Last updated:** 2026-06-29 | **License:** MIT
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement / Verify / Review / Ship (AFK agent orchestration harness)
**Layer:** Infrastructure (the orchestration engine) + Tooling (the CLI + templated harnesses you run)

---

## What it does

sandcastle (npm: `@ai-hero/sandcastle`) is a TypeScript library + CLI for orchestrating AI **coding** agents in isolated sandboxes. The core mechanism is a single `run()` call: you pass an agent provider (`claudeCode("claude-opus-4-7")`, also `codex`, `cursor`, `pi`, `opencode`, `copilot`), a sandbox provider (`docker()`, `podman()`, `vercel()`, `noSandbox()`, or a custom one), and a prompt; sandcastle spins up the sandbox, runs the agent against your repo on a configurable branch strategy, and merges the commits back. It is explicitly framed around your own dev loop — "parallelizing multiple AFK agents, creating review pipelines, or orchestrating your own agents" — not around building an AI product for end users.

`npx @ai-hero/sandcastle init` scaffolds a `.sandcastle/` directory (Dockerfile, prompt.md, .env) and writes a runnable `main.ts` from one of five templates (`blank`, `simple-loop`, `sequential-reviewer`, `parallel-planner`, `parallel-planner-with-review`), wired to an issue tracker (GitHub Issues, Beads, or custom). You then `npx tsx .sandcastle/main.ts` to drive the loop. Three branch strategies (`head` = write directly to host working dir; `merge-to-head` = throwaway temp branch merged on success; `branch` = land on a named branch for a PR) control how agent output relates to git. Beyond `run()` it exposes `createSandbox()` (a warm, reusable container for implement→verify→review chains, with `sandbox.exec()` to gate steps on `npm test`), `createWorktree()` (a first-class git worktree you can hand interactively then to an AFK agent), structured typed output via `Output.object()` with Zod/Standard Schema + auto-retry, session capture/`resume()`/`fork()` (fan-out from one parent session), lifecycle hooks split host vs sandbox, and `{{KEY}}` + `` !`command` `` prompt interpolation. Authored under mattpocock's AI Hero; the repo is heavily ADR-documented.

## How we tested it

**Evidence:** RUN

**Hands-on** — installed it via `npm i -D @ai-hero/sandcastle typescript tsx @types/node` (v0.12.0, 7s, 14 packages, 0 vulnerabilities) in five throwaway git repos under `/tmp/eval-sandcastle/`, scaffolded each of the five templates with `npx sandcastle init`, type-checked the generated harnesses with `tsc --strict`, then ran the generated `simple-loop` harness and `sandcastle docker build-image` in a sandbox that has the `docker` CLI but no Docker daemon.

```
npx sandcastle init --template <blank|simple-loop|sequential-reviewer|parallel-planner|parallel-planner-with-review> \
  --agent claude-code --model claude-opus-4-7 --sandbox docker --issue-tracker github-issues \
  --create-label false --build-image false --install-template-deps false
  -> all five exit 0; files written under .sandcastle/:
     blank                         .env.example .gitignore Dockerfile main.mts prompt.md                      (main.mts 12 lines)
     simple-loop                   same five files                                                           (50 lines)
     sequential-reviewer           + CODING_STANDARDS.md, implement-prompt.md, review-prompt.md              (119 lines)
     parallel-planner              + plan/implement/merge-prompt.md                                          (204 lines)
     parallel-planner-with-review  + CODING_STANDARDS.md, review-prompt.md                                   (226 lines)

tsc -p . (strict, NodeNext, zod installed)
  blank, simple-loop, sequential-reviewer         -> rc=0
  parallel-planner                                -> rc=1, 8x TS7006 (implicit any: issue, outcome, i, entry, b)
  parallel-planner-with-review                    -> rc=1, 8x TS7006 (same shape)

npx tsx .sandcastle/main.mts          (simple-loop, no daemon, 2.0s wall)
  WorktreeError: Provider 'docker' create failed: Image 'sandcastle:t-simple-loop' not found locally.
                 Build it first with 'sandcastle docker build-image'.
  -> uncaught exception stack trace; exit non-zero

npx sandcastle docker build-image
  x Docker operation failed: docker build failed: ERROR: failed to connect to the docker API at unix:///var/run/docker.sock
  |  . Is Docker running?

git branch --list 'sandcastle/*' ; git worktree list     (after two failed runs)
  + sandcastle/worker/20261016-024353-ca8ede
  + sandcastle/worker/20261016-024402-c543e8      <- two preserved worktrees under .sandcastle/worktrees/
```

## Test design

- **Task/corpus:** the five shipped `init` templates scaffolded into five fresh empty git repos; the one runnable path available here (`simple-loop`) driven to the point where a container is required.
- **Baseline:** none. There is no without-the-tool arm for scaffolding or for sandbox orchestration, so this is a RUN, not a MEASURED, eval.
- **Metric:** exit codes, files generated, `tsc --strict` pass/fail and error counts, error text on the daemon-less run.
- **Reproduce:** the commands in the block above, in an empty `git init` directory with Node 22.

## What worked

- **Install and scaffold are fast and clean.** 7s install, 0 vulnerabilities, 5/5 templates scaffold with exit 0 and a consistent file layout; the `--template/--agent/--sandbox/--issue-tracker` flags make `init` fully scriptable (no wizard needed).
- **Three of five generated harnesses type-check under `--strict`** (`blank`, `simple-loop`, `sequential-reviewer`), so the typed API surface in the README is real and the shortest harness is 12 lines.
- **Failure is explicit about the cause.** With no Docker daemon, the run names the missing image and the remedy (`sandcastle docker build-image`), and the build command names the daemon and asks "Is Docker running?".
- Release cadence is fast (0.10.0 at the earlier review, 0.12.0 at install), which is evidence of activity.

## What didn't work or surprised us

- **The core function was never exercised.** No Docker/Podman daemon, no Vercel account and no agent credentials exist in this sandbox, so no agent ran inside a sandbox and no commit was merged back. Everything about branch strategies, `createSandbox()`, `fork()` and structured output remains README-sourced.
- **Two scaffolded templates fail `tsc --strict`** (`parallel-planner`, `parallel-planner-with-review`): 8 implicit-any errors each on callbacks over the planner's output. Under a non-strict tsconfig this may be a non-issue; the strict setting is our choice, not the template's, and `tsx` runs the files without type-checking.
- **A failed run leaves state behind.** Each failed `run()` printed an uncaught `WorktreeError` stack trace and preserved a worktree plus a `sandcastle/worker/...` branch in the host repo (two after two attempts), with cleanup left to the user via `git worktree remove --force`.
- **Needs infra before first value.** Image build is a prerequisite; with no daemon nothing runs.
- Remains a parallel TypeScript orchestration runtime rather than a Claude Code extension, pre-1.0 and overlapping claude-squad / gastown (see prior review).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Scaffolds type-check (3/5 strict) but no agent output was produced, so correctness of the orchestrated work is untested |
| Speed | neutral | Install 7s and `init` is instant; parallel-agent speedup claims remain unmeasured |
| Maintainability | neutral | Generated harnesses are 12–226 lines of bespoke TypeScript the adopter owns; two need type fixes under strict mode |
| Safety | + (unverified) | The Docker/Podman isolation design is the stated blast-radius control, but it never ran here; failed runs leave worktrees/branches on the host |
| Cost Efficiency | neutral | No token or cost data; model routing per agent string is README-sourced |
| Verifiability | neutral | Merge-to-branch output is reviewable as ordinary git diffs, but the scaffold-level run produced nothing to verify |

## Verdict

**discovery-log — tentative read** — scaffolding and install work (5/5 templates, 3/5 strict type-check), but the container-backed run path stopped at the missing Docker daemon, so no agent-in-sandbox behaviour was measured; a human or a runner with a Docker daemon and a model credential should complete the simple-loop run before any verdict.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sandcastle](https://github.com/mattpocock/sandcastle) | framework | Orchestrate sandboxed coding agents in TypeScript | Need programmatic control over agent spawning and isolation | claude-squad, gastown, langgraph |
