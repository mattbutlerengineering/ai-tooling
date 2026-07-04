# Evaluation: opencode-swarm

**Repo:** [ZaxbyHub/opencode-swarm](https://github.com/ZaxbyHub/opencode-swarm)
**Stars:** 356 | **Last updated:** 2026-06-19 (pushed; created 2026-01-27) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Spans the inner loop end-to-end — Plan (architect + critic gate), Implement (coder), Verify (test_engineer + automated checks + regression sweep), Review (reviewer + critic), and into Ship (PR monitor, CI-fix). It is a gated pipeline, not a single-stage tool.
**Layer:** Tooling + Infrastructure — an installable OpenCode plugin (npm package, ~2,000 TypeScript files) that injects a hub-and-spoke agent team, scope-enforcement guardrails, shell-write static analysis, and persistent `.swarm/` state into a coding session.

---

## What it does

OpenCode Swarm is a plugin for [OpenCode](https://opencode.ai) that turns one AI coding session into an **architect-led team of specialized agents**. The pitch is the trust gap: most AI tools let one model write code and ask that same model whether it is good — Swarm separates planning, implementation, review, testing, and documentation into distinct internal roles and enforces **gated execution** so "nothing ships until every required gate passes." `bunx opencode-swarm install` registers the plugin, writes a global config, and disables OpenCode's native `explore`/`general` agents so the Swarm architect coordinates everything.

The roster is large and the README insists `/swarm agents` is the live source of truth, but it lists: architect, coder, reviewer, test_engineer, critic, explorer, sme, docs, designer, plus a cluster of critic-oversight/drift/hallucination verifiers and a "council" (generalist, skeptic, domain expert). The flow on "Build me a JWT auth system" is: clarify only what it cannot infer → scan codebase → consult cached SME guidance → write a phased plan → pass it through a **critic gate** before any code → execute one task at a time (coder → automated checks → reviewer → test engineer → architect regression sweep, failures looping back with structured feedback) → update docs and retrospectives per phase. All state lives in `.swarm/` (plans, evidence, knowledge, telemetry), making sessions resumable: if `.swarm/` exists, the architect jumps straight to RESUME → EXECUTE.

Beyond orchestration it ships real safety machinery: **scope enforcement** (declared write targets persisted to `.swarm/scopes/` with TTL, symlink guards, fail-closed validation, and scope-aware blocking of recursive deletes), **shell write detection** (a `bash-parser` AST plus PowerShell/cmd regex heuristics that intercept redirects, in-place editors, network downloaders, archive extraction, and destructive git ops before execution), per-task SAST/secrets/dependency scanning, an opt-in external-skill curation pipeline (prompt-injection + unsafe-instruction scans + SHA-256 provenance gates), and an opt-in GitHub PR monitor that polls CI/review/merge status and can auto-inject PR-feedback mode on failures.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `bunx install` was executed, no OpenCode session was launched, and no gated pipeline was observed. Every claim is from the repository (GitHub metadata, README, recursive file tree, `package.json`), not from measured agent behavior. The "6000+ tests" badge and "closes the trust gap" framing are the authors' claims, not anything verified here.

```bash
gh api repos/ZaxbyHub/opencode-swarm --jq '{desc,stars:.stargazers_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id}'
gh api repos/ZaxbyHub/opencode-swarm/readme --jq '.content' | base64 -d | head -130
gh api "repos/ZaxbyHub/opencode-swarm/git/trees/HEAD?recursive=1" --jq '.tree | length'   # 2967 entries
gh api "repos/ZaxbyHub/opencode-swarm/git/trees/HEAD?recursive=1" --jq '[.tree[].path|select(test("\\.(ts|tsx)$"))]|length'  # 1965 .ts
gh api "repos/ZaxbyHub/opencode-swarm/git/trees/HEAD?recursive=1" --jq '[.tree[].path|select(test("test|spec"))]|length'    # 1566
gh api repos/ZaxbyHub/opencode-swarm/contents/package.json --jq '.content' | base64 -d   # v7.79.7, npm-published
gh api repos/ZaxbyHub/opencode-swarm/releases --jq 'length'   # 30 (page-1 cap; release-please cadence)
gh api repos/ZaxbyHub/opencode-swarm/contributors --jq '[.[].login]'  # human + Copilot/claude/codex bots
```

## What worked

- **This is a real, substantial codebase, not a prompt pack.** 2,967 tree entries, ~1,965 TypeScript files, ~1,566 test/spec files, published to npm at v7.79.7, with `release-please` automation, biome, CHANGELOG, and a `bun.lock`. Among the multi-agent orchestrators in this catalog, very few ship this much actual engineering.
- **Adversarial separation is the right idea.** Using a *different* agent to review and a *different* one to test, behind a critic gate, directly attacks the "same model grading its own homework" failure mode that sinks most single-loop tools. The phase/drift/completion gates make "done" a verifiable state, not a model assertion.
- **Genuinely defense-in-depth safety.** Scope enforcement that handles array-based path args (a real bypass vector), AST-based shell-write detection across POSIX and Windows shells, fail-closed scope files with symlink guards, and a provenance-checked external-skill pipeline are the most serious safety surface of any orchestrator we have inspected. This is the standout feature.
- **Resumable by design.** Externalizing all plan/evidence/knowledge state to `.swarm/` and resuming via RESUME→EXECUTE is the correct pattern for long, multi-session work — most orchestrators lose the thread on restart.
- **Active and free-tier friendly.** Pushed the day of inspection, 30 releases, works with OpenCode Zen's free model roster, and every agent's model/guardrails are config-overridable.

## What didn't work or surprised us

- **OpenCode-only.** This is a hard scope limit: it is not a Claude Code plugin and not portable. If you are not on OpenCode it is a non-starter, which separates it cleanly from the Claude-Code-native neighbors (KARIMO, superpowers).
- **The install is invasive.** It *disables* OpenCode's native `explore` and `general` agents and rewrites `opencode.json`. The README itself warns that if the active agent is not a Swarm architect, the gates/reviewers/tests are silently bypassed — a confusing failure mode where you think you have QA and don't.
- **Heavy ceremony and token cost.** A council of generalist/skeptic/domain-expert plus four critic-verifier roles plus per-task SAST is a lot of agents and passes per task. For a small change this is enormous overhead; the value only amortizes on substantial, multi-phase work.
- **Single-author velocity, unverifiable claims.** Contributors are one human plus Copilot/claude/codex bots. The "6000+ tests" and "production trust" badges are self-reported; nothing here measures outcome quality, and the breakneck v7.79.7 versioning at five months old suggests churn, not stability.
- **The catalog one-liner undersells it.** "Architect-centric swarm plugin for OpenCode" reads like a thin persona wrapper; it is actually a heavyweight gated-QA harness with serious guardrail engineering.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Separate reviewer + test_engineer + critic gates and a regression sweep attack self-grading directly; phase/drift verifiers make "done" gated, not asserted. Strongest correctness story among the orchestrators inspected. |
| Speed | − | Multi-agent council + critic verifiers + per-task scans add many passes per task; clear overhead on small changes, amortized only on large multi-phase work. |
| Maintainability | + | Forces phased plans, docs/retrospective updates per phase, and durable `.swarm/` evidence/knowledge — process discipline that outlasts the session. No effect on your repo's code structure directly. |
| Safety | + | AST shell-write detection, fail-closed scope enforcement (incl. array-path bypass handling), per-task SAST/secrets/deps, provenance-gated external skills. The deepest safety surface of any catalog orchestrator. |
| Cost Efficiency | − / neutral | Many agents and gates burn tokens per task; offset by free-tier model support and config to disable agents. Net cost depends heavily on task size. |

## Verdict

**CONDITIONAL — adopt if you live in OpenCode and do substantial, multi-phase work; otherwise it does not apply.** opencode-swarm is the most seriously engineered multi-agent orchestrator we have inspected: a real ~2,000-file TypeScript npm package whose gated coder/reviewer/tester separation and AST-grade scope/shell guardrails directly target the failure modes that make single-loop AI coding untrustworthy. The blockers are scope and weight — it is OpenCode-only, the install is invasive (disabling native agents), and the council-plus-critics ceremony is overkill for small changes. The conditions: you are on OpenCode, you have multi-phase features (not one-line fixes), and you accept the token overhead in exchange for gated QA.

Compared to neighbors: **claude-squad** and **gastown** just run multiple agents in parallel with visibility — they have no gates, no QA pipeline, and no safety surface, so they are coordination shells where Swarm is a coordination *and verification* engine. **agent-orchestrator** automates spawn + CI-fix + merge but is far thinner on adversarial review and guardrails. **KARIMO** is the closest peer in ambition (PRD-driven, wave-orchestrated, gated review) but is Claude-Code-native and markdown-based rather than a compiled TypeScript plugin — choose by which host you run. For OpenCode users wanting real QA gates, Swarm is the strongest option in the catalog; for everyone else it is simply out of host.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opencode-swarm](https://github.com/ZaxbyHub/opencode-swarm) | plugin | Architect-led gated agent swarm for OpenCode (~2K-file TS plugin): separate coder/reviewer/tester/critic roles, AST scope+shell guardrails, resumable `.swarm/` state | One model writing and grading its own code misses too much; need adversarial review/test gates and real write-scope safety before anything ships | claude-squad, gastown (parallel agents, no gates); agent-orchestrator (thinner QA); KARIMO (Claude-Code-native gated peer) |
