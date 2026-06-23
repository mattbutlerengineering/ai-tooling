# Evaluation: gsd-build / get-shit-done (GSD)

**Repo:** [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) — **now redirects to** [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)
**Stars:** 64,359 (gsd-build, frozen) / 4,819 (open-gsd/gsd-core, active) | **Last updated:** gsd-build pushed 2026-05-31 (deprecation chores only); gsd-core pushed 2026-06-22 | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Plan + Implement (spans Discuss → Plan → Execute → Verify → Ship)
**Layer:** Process (a phase-loop methodology) with a Tooling spine (an `npx` installer + a `gsd-tools.cjs` CLI)

---

## What it does

Catalog one-liner (as filed): "Standalone GSD: meta-prompting and spec-driven dev for Claude Code." GSD ("Git. Ship. Done.", by TÂCHES) is a context-engineering and spec-driven development framework that drives an AI coding agent through a disciplined five-step phase loop: **Discuss** (capture decisions before planning) → **Plan** (research, decompose, verify the plan fits a fresh context window) → **Execute** (run plans in parallel waves, each executor starting with a clean ~200K context) → **Verify** (walk through what was built, diagnose, fix before declaring done) → **Ship** (create the PR, archive the phase, repeat). Its central thesis is fighting *context rot* — the quality decay as a session fills its window — by pushing all heavy research/planning/execution into fresh-context subagents while the main session stays lean, with durable artifacts (`STATE.md`, `CONTEXT.md`, `PROJECT.md`, roadmap/phase files under `.planning/`) surviving session boundaries.

Mechanically it is not a Claude Code plugin. It installs via `npx @opengsd/gsd-core@latest` (formerly `npx get-shit-done-cc`), which prompts for runtime (Claude Code, Codex, Gemini CLI, Cursor, Windsurf, Kimi, Kilo, and ~10 more) and location, then writes the framework into the agent's config directory. **As of the v1.5.0 release measured here the user-facing surface has migrated from `/gsd:*` slash commands to a fleet of `gsd-*` *skills*** — the install scaffolds **69 skills** (`gsd-new-project`, `gsd-discuss-phase`, `gsd-plan-phase`, `gsd-execute-phase`, `gsd-verify-work`, `gsd-ship`, `gsd-complete-milestone`, `gsd-debug`, `gsd-map-codebase`, …), **34 restricted-tool subagents** (`gsd-planner`, `gsd-executor`, `gsd-verifier`, `gsd-roadmapper`, `gsd-phase-researcher`, `gsd-codebase-mapper`, `gsd-security-auditor`, …), a hook set, and a **`gsd-core/bin/` support tree** holding the deterministic `gsd-tools.cjs` Node CLI (backed by 118 `bin/lib/*.cjs` modules). The CLI handles deterministic mechanics — state transitions, milestone/phase/roadmap file scaffolding, decimal-phase insertion, model-profile resolution, slug generation — so structural bookkeeping is reproducible rather than left to the model. The orchestrating skills dispatch the subagents; the CLI is the mechanical spine underneath.

## How we tested it

**Evidence:** MEASURED

**Ran the GSD tooling spine hands-on on 2026-06-22** (macOS arm64, Node v20.19.5 / npm 10.8.2). I installed `@opengsd/gsd-core@latest` (**v1.5.0**) non-interactively into an **isolated throwaway config dir** under `mktemp -d` (`--config-dir`, so the user's real `~/.claude` was never touched — confirmed afterward it still reads v1.22.4, untouched), enumerated the full scaffolded surface (skill/agent/CLI counts), then **drove the deterministic `gsd-tools.cjs` CLI end-to-end against a throwaway git project** — running state/scaffolding/resolver subcommands and verifying their real on-disk effects. The temp dir was deleted afterward. **The agent phase-loop itself (Discuss→Plan→Execute→Verify→Ship) was NOT exercised** — it requires live Claude Code subagent sessions and cannot run headless; what I measured is the *tooling spine* the loop rides on, not generated-code quality.

```bash
TMPD=$(mktemp -d)                                                   # isolated; never ~/.claude
npx -y @opengsd/gsd-core@latest --help                             # 16 runtimes, --profile flags
npx -y @opengsd/gsd-core@latest --claude --global --config-dir "$TMPD/config"
#   → "Installed 69 skills", "Installed agents", "Wrote VERSION (1.5.0)", 14 hooks configured
TOOLSBIN="$TMPD/config/gsd-core/bin/gsd-tools.cjs"
node "$TOOLSBIN" --help                                            # 64 subcommands
node "$TOOLSBIN" current-timestamp                                 # {"timestamp":"2026-06-23T01:54:39.039Z"}
node "$TOOLSBIN" generate-slug "Add OAuth login flow"              # {"slug":"add-oauth-login-flow"}
node "$TOOLSBIN" resolve-model gsd-planner                         # {"model":"opus","profile":"balanced","effort":"xhigh"}
node "$TOOLSBIN" resolve-model gsd-executor                        # {"model":"sonnet","profile":"balanced","effort":"high"}
cd "$TMPD/proj" && git init -q
node "$TOOLSBIN" config-new-project                                # {"created":true,"path":".planning/config.json"}
node "$TOOLSBIN" init new-project                                  # full env resolution (git/greenfield/models)
node "$TOOLSBIN" phase add "Auth foundation"                       # Error: ROADMAP.md not found (correct precondition gate)
rm -rf "$TMPD"                                                     # cleaned up
```

**Install (measured).** Despite an `EBADENGINE` warning (the package declares `node >=22`; I ran v20.19.5), the install completed cleanly in **~2 s wall**: `npx -y @opengsd/gsd-core@latest --claude --global --config-dir <temp>` printed `✓ Installed 69 skills to skills/`, `✓ Installed agents`, `✓ Wrote VERSION (1.5.0)`, `✓ Wrote package.json (CommonJS mode)`, and configured **14 hooks** (update-check, context-window monitor, prompt-injection guard, read-before-edit guard, read-injection scanner, worktree-path guard, statusline, etc.). The install command in the catalog/docs resolves and works headless on this host.

**Scaffolded surface (measured, counted from the live install — not the README).** `ls` of the temp config dir gave **69 skills**, **34 agents** (`gsd-agents/*.md`), **118 `bin/lib/*.cjs`** modules behind the CLI, and **9 wired hook handlers** referenced in the generated `settings.json` (`gsd-context-monitor.js`, `gsd-prompt-guard.js`, `gsd-read-injection-scanner.js`, `gsd-worktree-path-guard.js`, …). This is a notable migration: the prior eval (and v1.22.4 install) described a `/gsd:*` *slash-command* surface; v1.5.0 ships the same loop as **skills** instead.

**Deterministic CLI driven end-to-end (measured).** `node gsd-tools.cjs --help` enumerated **64 subcommands** (`agent`, `commit`, `config-*`, `init`, `milestone`, `phase`, `phases`, `roadmap`, `resolve-model`, `resolve-granularity`, `scaffold`, `state`, `validate`, `verify`, `workstream`, `worktree`, …). Exercised against a fresh `git init` temp project:
- `current-timestamp` → clean JSON `{"timestamp":"2026-06-23T01:54:39.039Z"}`.
- `generate-slug "Add OAuth login flow"` → `{"slug":"add-oauth-login-flow"}` (deterministic kebab-case).
- `resolve-model gsd-planner` → `{"model":"opus","profile":"balanced","effort":"xhigh"}`; `resolve-model gsd-executor` → `{"model":"sonnet",...,"effort":"high"}` — the model-profile resolver maps each agent role to a model/effort tier deterministically.
- `config-new-project` → created a real `.planning/config.json` on disk (`{"created":true,...}`) — a 60-key config (model_profile, git branching templates, a full `workflow` block with research/plan-check/verifier/security gates, plan-review source-grounding).
- `init new-project` → ran a genuine environment-resolution pass on the temp repo: detected git (`"has_git":true`, resolved worktree root), classified it greenfield (`"is_brownfield":false`, `"has_codebase_map":false`), resolved per-role models, confirmed `"agents_installed":true` and `"agent_runtime":"claude"`.
- `phase add "Auth foundation"` → correctly errored `ROADMAP.md not found` — a real precondition gate, not a crash; subcommands invoked without their required state print self-documenting errors listing valid subcommands (e.g. `phase` → `uat-passed, next-decimal, add, add-batch, insert, remove, complete`).

**Latency (measured).** Cold CLI invocations averaged **~60 ms each** (5× `current-timestamp` = 300 ms wall) — fast enough to call inline from skills without perceptible overhead.

**Not exercised (disclosed).** The Discuss→Plan→Execute→Verify→Ship agent loop, executor green-rates, generated-code quality, and brownfield phase evolution all require live agent subagent sessions and were **not** run for this eval. This is expected for a methodology framework, not a tooling failure — the measurable, deterministic spine (installer + `gsd-tools.cjs`) is what was verified.

## What worked

- **Installs headless on macOS arm64 in ~2 s** via `npx -y @opengsd/gsd-core@latest --claude --global --config-dir <temp>` — non-interactive flags exist (`--claude`/`--global`/`--config-dir`/`--profile`), so the install can be scripted and isolated. The `--config-dir` flag kept the run fully out of the user's real `~/.claude` (verified untouched at v1.22.4 afterward).
- **The deterministic CLI spine is real and reproducible.** `gsd-tools.cjs` exposes **64 subcommands** that produce clean JSON and write real `.planning/` state; `generate-slug`, `current-timestamp`, `resolve-model`, `config-new-project`, and `init new-project` all ran end-to-end with the outputs quoted above. Structural bookkeeping genuinely lives in code, not in the model.
- **Precondition gating is honest.** `phase add` refused with `ROADMAP.md not found` rather than scaffolding garbage; missing-arg invocations print the valid subcommand list. The mechanics fail loudly and self-document.
- **The model-profile resolver is a concrete cost lever.** `resolve-model` deterministically assigns opus/xhigh to the planner and sonnet/high to the executor — heavy reasoning where it pays, cheaper models for execution, decided by code.
- **Security-conscious install.** The scaffold wires a prompt-injection guard, a read-injection scanner, a read-before-edit guard, and a worktree-path guard as hooks, plus a `package-legitimacy` CLI command (supply-chain check) — rails beyond the bare phase loop.
- **Strong, current maturity at the active home.** `open-gsd/gsd-core` is MIT, on npm (`@opengsd/gsd-core` v1.5.0), pushed the day of this eval; the combined lineage (64K stars frozen + 4.8K active) reflects heavy real use.

## What didn't work or surprised us

- **The v1.5.0 surface has migrated from `/gsd:*` commands to skills.** The prior eval and the user's installed v1.22.4 describe a 40+ `/gsd:*` *slash-command* surface; the current package scaffolds **69 `gsd-*` skills** plus **34 subagents** instead. The loop is the same, but the catalog one-liner's "/gsd:* commands" framing is now stale for the active package.
- **Declared Node engine is `>=22`; I ran v20.19.5.** The installer and CLI both emitted `npm warn EBADENGINE` but ran correctly anyway. On a strict environment that enforces engines, the install could be refused — worth pinning Node 22+ for production use.
- **The catalog entry's original "standalone vs superpowers" premise is wrong.** GSD has no relationship to superpowers (confirmed in prior inspection: the superpowers plugin dir contains zero GSD files); it installs independently via the npx installer. There is no lighter "GSD without superpowers" variant — it is simply *the* GSD.
- **The repo in the catalog row is deprecated.** `gsd-build/get-shit-done`'s README is now a "GSD Has Moved" redirect to `open-gsd/gsd-core`; the canonical home (issues, releases, the published `@opengsd/gsd-core` package) has moved. The catalog should track `open-gsd/gsd-core`.
- **The agent loop was not exercised.** Generated-code quality, executor green-rates, and brownfield phase evolution rest on docs/source plus this spine run — not an observed Discuss→Ship loop, which requires live agent sessions.
- **Heavy ceremony for small changes.** 69 skills, 34 subagents, and a 60-key per-project config are a lot of process for a one-line fix — the same "great for greenfield/large features, overkill for a typo" tradeoff noted for spec-kit and Taskmaster.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Discuss→Plan→Verify gates and goal-backward verification force alignment and a build-actually-works check before a phase is declared done. Measured: the CLI gates preconditions (`phase add` refused without a ROADMAP) rather than scaffolding inconsistent state. |
| Speed | + (large/multi-session) / - (small) | Fresh-context subagents + durable `STATE.md`/`CONTEXT.md` make long projects resumable without re-planning; the phase ceremony is overhead for a bug fix. CLI itself is fast (~60 ms/call, measured). |
| Maintainability | + | `PROJECT.md`, roadmap, phase, and `CONTEXT.md` artifacts persist intent/decisions in the repo across sessions. Measured: `config-new-project`/`init new-project` write a real, inspectable `.planning/` state tree rather than ephemeral prompt state. |
| Safety | neutral/+ | Restricted-tool subagents, atomic commits, and a verify step add rails; runs inside the existing Claude Code session with no extra API key. Measured: the install wires a prompt-injection guard, read-injection scanner, read-before-edit and worktree-path guards as hooks. |
| Cost Efficiency | neutral/+ | Context-rot mitigation (lean main session, scoped subagents) is designed to cut wasted tokens; offset by multiple subagent passes per phase. Measured: `resolve-model` deterministically routes the planner to opus and the executor to sonnet — a concrete cost lever decided by code. |

## Verdict

**KEEP** (already installed; this is the user's own GSD, not a new tool to add)

This catalog row does not describe a candidate to adopt — under a mistaken "standalone vs superpowers" framing it describes **the exact GSD the user already runs** (verified at v1.22.4 in `~/.claude/`, installed via the npx installer, independent of superpowers). The hands-on run here confirms the *tooling spine* is real and reproducible: the v1.5.0 installer scaffolds 69 skills + 34 subagents + a 64-command deterministic CLI in ~2 s, and that CLI genuinely resolves models, generates slugs, and writes/gates `.planning/` state on disk. The agent phase-loop — the part that actually produces code — was not exercised (it needs live subagent sessions), so this KEEP rests on a verified spine plus a sound, well-motivated process design, not on observed generated-code quality. The only actions warranted are catalog hygiene: (1) **retarget the entry to `open-gsd/gsd-core`**, the active MIT home of the `@opengsd/gsd-core` package, since `gsd-build/get-shit-done` is a redirect stub; (2) **fix the one-liner** to drop the false "without the superpowers plugin" premise and reflect the v1.5.0 *skills* surface (not `/gsd:*` commands); and (3) optionally note the user should run `/gsd:update` (or reinstall) to close the v1.22.4 → v1.5.0 gap. Relative to the SDD trio already evaluated: GSD is the user's *incumbent* Plan→Implement→Verify framework, which is precisely why **spec-kit** and **claude-task-master** were judged largely redundant *for this user*.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [GSD (gsd-core)](https://github.com/open-gsd/gsd-core) | framework | Git. Ship. Done — context-engineering + spec-driven phase loop (Discuss→Plan→Execute→Verify→Ship) for Claude Code and other runtimes, via `npx @opengsd/gsd-core` (4.8K stars; 64K on the frozen gsd-build repo) | Context rot and "prompt and pray" degrade AI output on multi-session work; run heavy work in fresh-context subagents with durable cross-session state | spec-kit, claude-task-master, BMAD-METHOD, OpenSpec, feature-dev |
