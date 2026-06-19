# Evaluation: sandcastle

**Repo:** [mattpocock/sandcastle](https://github.com/mattpocock/sandcastle)
**Stars:** 6,167 | **Last updated:** 2026-06-18 (v0.10.0) | **License:** MIT
**Dev loop stage:** Implement / Verify / Review / Ship (AFK agent orchestration harness)
**Layer:** Infrastructure (the orchestration engine) + Tooling (the CLI + templated harnesses you run)

---

## What it does

sandcastle (npm: `@ai-hero/sandcastle`) is a TypeScript library + CLI for orchestrating AI **coding** agents in isolated sandboxes. The core mechanism is a single `run()` call: you pass an agent provider (`claudeCode("claude-opus-4-7")`, also `codex`, `cursor`, `pi`, `opencode`, `copilot`), a sandbox provider (`docker()`, `podman()`, `vercel()`, `noSandbox()`, or a custom one), and a prompt; sandcastle spins up the sandbox, runs the agent against your repo on a configurable branch strategy, and merges the commits back. It is explicitly framed around your own dev loop — "parallelizing multiple AFK agents, creating review pipelines, or orchestrating your own agents" — not around building an AI product for end users.

`npx @ai-hero/sandcastle init` scaffolds a `.sandcastle/` directory (Dockerfile, prompt.md, .env) and writes a runnable `main.ts` from one of five templates (`blank`, `simple-loop`, `sequential-reviewer`, `parallel-planner`, `parallel-planner-with-review`), wired to an issue tracker (GitHub Issues, Beads, or custom). You then `npx tsx .sandcastle/main.ts` to drive the loop. Three branch strategies (`head` = write directly to host working dir; `merge-to-head` = throwaway temp branch merged on success; `branch` = land on a named branch for a PR) control how agent output relates to git. Beyond `run()` it exposes `createSandbox()` (a warm, reusable container for implement→verify→review chains, with `sandbox.exec()` to gate steps on `npm test`), `createWorktree()` (a first-class git worktree you can hand interactively then to an AFK agent), structured typed output via `Output.object()` with Zod/Standard Schema + auto-retry, session capture/`resume()`/`fork()` (fan-out from one parent session), lifecycle hooks split host vs sandbox, and `{{KEY}}` + `` !`command` `` prompt interpolation. Authored under mattpocock's AI Hero; the repo is heavily ADR-documented.

## How we tested it

Inspected the GitHub repo via the API and read the full README (1,400 lines): the `run()`/`createSandbox()`/`createWorktree()` APIs, all option/result tables, the agent-provider matrix, branch strategies, session capture/resume/fork semantics, structured output, hooks, templates, and the custom-provider contract. Reviewed repo metadata (release cadence, languages, ADR-driven `docs/`). Did NOT install or run it — this is an architecture/surface-area review to decide catalog placement, applying the same lens used for the aisuite (SKIP) and fast-agent (CONDITIONAL) evaluations. No metrics below are measured; all claims are sourced from the repo.

```bash
gh api repos/mattpocock/sandcastle --jq '{stars,license,description,pushed_at,created_at}'
gh api repos/mattpocock/sandcastle/readme --jq '.content' | base64 -d   # 1,400-line README
gh api repos/mattpocock/sandcastle/contents --jq '.[].name'             # src/, docs/, .sandcastle/, ADRs
gh api repos/mattpocock/sandcastle/releases --jq '.[0:3][] | {tag:.tag_name,date:.published_at}'
gh api repos/mattpocock/sandcastle/languages                            # 99% TypeScript
```

Reviewed: agent providers (`claudeCode`, `codex`, `cursor`, `pi`, `opencode`, `copilot`), sandbox providers (Docker/Podman bind-mount, Vercel/temp isolated, noSandbox), the `init` flow + 5 templates, branch strategies, session JSONL capture/resume/fork (incl. Claude Code subagent transcript capture), `Output.object()` structured output with `maxRetries`, and host/sandbox lifecycle hooks.

## What worked

- **It is a dev-loop tool, not a product-building framework.** Unlike aisuite/LangGraph (libraries you import to *build* an AI app), sandcastle is something you run *on your own repo* to get commits/PRs back. That places it squarely in Implement/Verify/Review/Ship, so it clears the bar that earned aisuite a SKIP.
- **First-class Claude Code integration.** `claudeCode()` is a native provider with effort levels (`low`→`max`), `permissionMode` mapping to Claude's `--permission-mode`, automatic session JSONL capture to the host for `claude --resume`, **and** capture of `Agent`/`Workflow` subagent transcripts. `resume()`/`fork()` use Claude's native `--resume`/`--fork-session`. This is deeper CC awareness than most orchestrators.
- **Real isolation with a clean provider abstraction.** Built-in Docker, Podman, and Vercel (Firecracker microVM via `@vercel/sandbox`) providers; a documented bind-mount vs isolated contract lets you add your own. AFK runs default to `--dangerously-skip-permissions` *inside* a container — the safety case for sandboxing autonomous agents.
- **Verify/Review primitives are dev-loop-shaped.** `createSandbox()` keeps a warm container so an implement step can be gated on `sandbox.exec("npm test")` before a review agent runs on the same branch; templates ship a `sequential-reviewer` and `parallel-planner-with-review` pipeline. Structured output with schema validation + auto-retry makes agents usable as scriptable graders.
- **Mature, active, well-documented.** v0.10.0 pushed 2026-06-18 (day before review), created 2026-03 — fast cadence; 99% TypeScript, MIT, ADR-backed design docs, non-interactive CLI flags for CI.

## What didn't work or surprised us

- **It is a parallel orchestration layer, not a Claude Code extension.** There is no sandcastle plugin/skill/MCP server/hook you add to Claude Code. Adopting it means writing a TypeScript harness that *invokes* agents — a separate runtime alongside your interactive CC session, the same caveat fast-agent has.
- **You write (and maintain) TypeScript orchestration code.** The power comes from the JS API; templates get you started, but a real multi-agent pipeline is bespoke `main.ts` code (branch strategy, prompts, hooks, merge handling) you own and debug. Non-trivial vs a one-line CLI tool.
- **Hard infra dependency.** Needs Docker Desktop, Podman, or a Vercel account for real isolation. `noSandbox()` exists but drops the central safety property. Node/tsx-centric — not a fit for non-JS shops wanting a zero-code tool.
- **Overlaps a crowded niche.** Competes with claude-squad/gastown (multi-agent workspace managers), omnigent (meta-harness), and the sandbox-infra layer (forkd/sandboxd) — sandcastle's differentiator is the *programmatic TS orchestration + git-merge-back*, not the sandboxing itself.
- **Pre-1.0.** v0.x with frequent ADRs reworking the API surface (branch strategy moved from provider to `run()`, fork semantics, completion-timeout) — expect churn.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Implement→`exec("npm test")`→review pipelines and `Output.object()` schema validation + retry let you gate agent work on verification before merge |
| Speed | + | Parallel AFK agents on separate branches and `fork()` fan-out from one warm session; `createSandbox()` reuses a warm container across runs |
| Maintainability | neutral | Agents edit your repo like any agent; you take on a bespoke TS harness to maintain in exchange for repeatable orchestration |
| Safety | + | Autonomous agents run inside Docker/Podman/Vercel isolation with merge-to-head strategy keeping HEAD untouched on failure; container is the blast radius |
| Cost Efficiency | + | Provider-agnostic agent strings let you route cheaper models (e.g. Sonnet reviewer over an Opus implementer) and reuse warm sandboxes; token-usage snapshots per iteration |

## Verdict

**CONDITIONAL**

sandcastle clears the bar aisuite did not: it is not a library for building AI products, but a harness you run against your own repo to orchestrate sandboxed coding agents (Claude Code, Codex, Cursor, Pi, etc.) with commits merged back — landing directly in the Implement, Verify, Review, and Ship stages. Its Claude Code integration is genuinely deep (native provider, session/subagent capture, resume/fork, permission modes) and the isolation + git-merge-back model is the right shape for safe AFK automation. It is mature, MIT, and actively developed by a credible author.

It is CONDITIONAL rather than ADOPT for the same reasons as fast-agent: (a) it is a *parallel* orchestration runtime, not an enhancement to your interactive Claude Code setup — there is no plugin/skill to install; (b) using it well means writing and maintaining bespoke TypeScript orchestration code; and (c) it requires container/VM infra (Docker, Podman, or Vercel). **Adopt it when** you want programmatic, sandboxed, multi-branch parallel AFK agents — issue-queue grinders, implement→test→review pipelines, or model-mixed fan-out — and you are comfortable in TypeScript with Docker available. If you only run one interactive Claude Code session at a time, or want a zero-code multi-agent UI, claude-squad/gastown are a lighter fit and the marginal benefit is smaller.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sandcastle](https://github.com/mattpocock/sandcastle) | framework | Orchestrate sandboxed coding agents in TypeScript | Need programmatic control over agent spawning and isolation | claude-squad, gastown, langgraph |
