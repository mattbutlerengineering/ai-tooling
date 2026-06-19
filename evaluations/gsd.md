# Evaluation: gsd-build / get-shit-done (GSD)

**Repo:** [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) — **now redirects to** [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)
**Stars:** 64,359 (gsd-build, frozen) / 4,521 (open-gsd/gsd-core, active) | **Last updated:** gsd-build pushed 2026-05-31 (deprecation chores only); gsd-core pushed 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan + Implement (spans Discuss → Plan → Execute → Verify → Ship)
**Layer:** Process (a phase-loop methodology) with a Tooling spine (an `npx` installer + a `gsd-tools.cjs` CLI)

---

## What it does

Catalog one-liner (as filed): "Standalone GSD: meta-prompting and spec-driven dev for Claude Code." GSD ("Git. Ship. Done.", by TÂCHES) is a context-engineering and spec-driven development framework that drives an AI coding agent through a disciplined five-step phase loop: **Discuss** (capture decisions before planning) → **Plan** (research, decompose, verify the plan fits a fresh context window) → **Execute** (run plans in parallel waves, each executor starting with a clean ~200K context) → **Verify** (walk through what was built, diagnose, fix before declaring done) → **Ship** (create the PR, archive the phase, repeat). Its central thesis is fighting *context rot* — the quality decay as a session fills its window — by pushing all heavy research/planning/execution into fresh-context subagents while the main session stays lean, with durable artifacts (`STATE.md`, `CONTEXT.md`, `PROJECT.md`, roadmap/phase files under `.planning/`) surviving session boundaries.

Mechanically it is not a Claude Code plugin. It installs via `npx @opengsd/gsd-core@latest` (formerly `npx get-shit-done-cc`), which prompts for runtime (Claude Code, Codex, Gemini CLI, Cursor, Windsurf, etc.) and writes a set of `/gsd:*` slash commands plus a `get-shit-done/` support tree (a `bin/gsd-tools.cjs` Node CLI, `references/`, `templates/`, `workflows/`) into the agent's config directory. The CLI handles deterministic mechanics (state transitions, milestone/phase/roadmap file scaffolding, decimal-phase insertion, model-profile resolution) so structural bookkeeping is reproducible rather than left to the model. The command surface is large — roughly 40+ `/gsd:*` commands (`new-project`, `discuss-phase`, `plan-phase`, `execute-phase`, `verify-work`, `complete-milestone`, `debug`, `map-codebase`, `set-profile`, etc.) — and it ships a fleet of restricted-tool subagents (`gsd-planner`, `gsd-executor`, `gsd-verifier`, `gsd-roadmapper`, `gsd-phase-researcher`, `gsd-codebase-mapper`, and more) that the orchestrating commands dispatch.

## How we tested it

**Source-grounded inspection plus inspection of the user's already-installed copy — I did not run a fresh install or execute a Discuss→Ship loop for this eval.** I queried GitHub metadata for both the old (`gsd-build/get-shit-done`) and new (`open-gsd/gsd-core`) repos, read the gsd-build README (now a redirect notice) and the gsd-core README, mapped the gsd-core tree (commands, agents, bin, src), and — critically for the redundancy question — inspected the user's local GSD footprint: `~/.claude/gsd-file-manifest.json` (version, file hashes), `~/.claude/get-shit-done/VERSION`, the `~/.claude/commands/gsd/` command set, the `gsd-*` hooks wired in `~/.claude/settings.json`, and the superpowers plugin directory to test whether GSD lives inside it.

```bash
gh api repos/gsd-build/get-shit-done --jq '{stars,license,description,pushed_at,archived}'   # 64,359 stars, MIT; README is a "moved" redirect
gh api repos/gsd-build/get-shit-done/readme | jq -r .content | base64 -d                       # → points to open-gsd/gsd-core
gh api repos/gsd-build/get-shit-done/contents/package.json | jq -r .content | base64 -d        # name "get-shit-done-cc", v1.50.0-canary.0
gh api repos/open-gsd/gsd-core --jq '{stars,license,description,pushed_at,created_at}'          # 4,521 stars, MIT, created 2026-05-22, active
gh api repos/open-gsd/gsd-core/contents/package.json | jq -r .content | base64 -d | grep name  # "@opengsd/gsd-core"
gh api "repos/open-gsd/gsd-core/git/trees/main?recursive=1" --jq '.tree[].path' | grep command # 40+ /gsd:* command files
# Local install footprint (the user's actual GSD):
cat ~/.claude/get-shit-done/VERSION            # 1.22.4
grep version ~/.claude/gsd-file-manifest.json  # "version": "1.22.4", files keyed under get-shit-done/...
ls ~/.claude/commands/gsd/                      # add-phase, execute-phase, plan-phase, verify-work, ...
grep -i gsd ~/.claude/settings.json             # gsd-check-update.js, gsd-context-monitor.js, gsd-statusline.js hooks
find ~/.claude/plugins/.../superpowers -iname '*gsd*'   # (empty — GSD is NOT inside superpowers)
```

## What worked

- **This *is* the user's installed GSD — verified, not inferred.** The local manifest (`~/.claude/gsd-file-manifest.json`, v1.22.4) keys every file under `get-shit-done/`, the `VERSION` file reads `1.22.4`, the `/gsd:*` command set is present in `~/.claude/commands/gsd/`, and three `gsd-*` hooks are wired into `settings.json`. The old `gsd-build/get-shit-done` repo's npm package is `get-shit-done-cc`; the new home publishes `@opengsd/gsd-core`. The catalog row points at the genuine upstream of what the user already runs.
- **The phase loop is a real, well-structured Plan→Implement→Verify methodology.** Discuss→Plan→Execute→Verify→Ship with a deterministic CLI for state/scaffolding and restricted-tool subagents for each role is a disciplined answer to "prompt and pray," comparable in rigor to spec-kit's Specify→Plan→Tasks→Implement.
- **Context-rot mitigation is the genuine differentiator.** Running heavy work in fresh-context subagents while keeping the main session lean, plus durable `STATE.md`/`CONTEXT.md` artifacts across sessions, is a concrete, well-motivated design — not persona theater.
- **Strong, current maturity at the active home.** `open-gsd/gsd-core` is MIT, on npm (`@opengsd/gsd-core`), has CI/tests, changesets-based releases, 30 contributors on the lineage, and was pushed the day of this eval. The combined lineage (64K stars on the frozen repo + 4.5K on the new one) reflects a heavily-used project, not a toy.
- **Multi-runtime by installer.** The installer targets Claude Code, Codex, Gemini CLI, Cursor, Windsurf, and more — portability the user's current single-runtime install doesn't expose but the framework supports.

## What didn't work or surprised us

- **The catalog entry's core premise is wrong.** It frames gsd-build as "standalone GSD … without the full superpowers plugin," implying (a) GSD is normally bundled inside superpowers and (b) gsd-build is a slimmer alternative. Both are false. GSD has **no relationship to superpowers** — I confirmed the superpowers plugin directory contains zero GSD files, and the user's GSD is installed independently via the npx installer to `~/.claude/`. There is no "GSD (superpowers)" entry that gsd-build is a lighter version *of*; it is simply *the* GSD, and the user already has it.
- **The repo in the catalog row is deprecated.** `gsd-build/get-shit-done`'s default-branch README is now a "GSD Has Moved" redirect to `open-gsd/gsd-core`; recent commits are pure deprecation chores (auto-close workflow, Discord-link updates). Source still exists on the branch, but the canonical home — issues, releases, the published `@opengsd/gsd-core` package — has moved. The catalog should track `open-gsd/gsd-core`.
- **Version drift on the user's machine.** The installed copy is v1.22.4 (manifest timestamped 2026-03-05); the old repo's package.json shows v1.50.0-canary and the new package is at its own version line. The user is materially behind upstream; `/gsd:update` exists precisely for this.
- **Heavy command surface and ceremony.** 40+ `/gsd:*` commands and a multi-agent fleet are a lot of process for small changes — the same "great for greenfield/large features, overkill for a one-line fix" tradeoff noted for spec-kit and Taskmaster.
- **Not hands-on validated here.** Claims about generated-code quality, executor green-rates, and how cleanly the phase loop survives brownfield evolution rest on docs, source, and the installed file tree — not an observed Discuss→Ship run for this eval.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Discuss→Plan→Verify gates and goal-backward verification force alignment and a build-actually-works check before a phase is declared done |
| Speed | + (large/multi-session) / - (small) | Fresh-context subagents + durable `STATE.md`/`CONTEXT.md` make long projects resumable without re-planning; the phase ceremony is overhead for a bug fix |
| Maintainability | + | `PROJECT.md`, roadmap, phase, and `CONTEXT.md` artifacts persist intent/decisions in the repo across sessions rather than in throwaway prompts |
| Safety | neutral/+ | Restricted-tool subagents, atomic commits, and a verify step add rails; runs inside the existing Claude Code session with no extra API key or sandbox |
| Cost Efficiency | neutral/+ | Context-rot mitigation (lean main session, scoped subagents) is explicitly designed to cut wasted tokens; offset by multiple subagent passes per phase |

## Verdict

**KEEP** (already installed; this is the user's own GSD, not a new tool to add)

This catalog row does not describe a candidate to adopt — it describes, under a mistaken "standalone vs superpowers" framing, **the exact GSD the user already runs** (verified at v1.22.4 in `~/.claude/`, installed via the npx installer, independent of superpowers). There is nothing to install and no second framework to weigh: gsd-build/get-shit-done is the (now-deprecated) upstream repo of that install. The only actions warranted are catalog hygiene, not adoption: (1) **retarget the entry to `open-gsd/gsd-core`**, the active MIT home and source of the `@opengsd/gsd-core` package, since `gsd-build/get-shit-done` is a redirect stub; (2) **fix the one-liner and "problem it solves"** to drop the false "without the superpowers plugin" premise — GSD is not part of superpowers, so the implied lighter-weight variant does not exist; and (3) optionally note the user should run `/gsd:update` to close the v1.22.4 → current gap. Relative to the SDD trio already evaluated: GSD is the user's *incumbent* Plan→Implement→Verify framework, which is precisely why **spec-kit** and **claude-task-master** were both judged largely redundant *for this user* — they overlap the loop GSD already provides natively in-session.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [GSD (gsd-core)](https://github.com/open-gsd/gsd-core) | framework | Git. Ship. Done — context-engineering + spec-driven phase loop (Discuss→Plan→Execute→Verify→Ship) for Claude Code and other runtimes, via `npx @opengsd/gsd-core` (4.5K stars; 64K on the frozen gsd-build repo) | Context rot and "prompt and pray" degrade AI output on multi-session work; run heavy work in fresh-context subagents with durable cross-session state | spec-kit, claude-task-master, BMAD-METHOD, OpenSpec, feature-dev |
