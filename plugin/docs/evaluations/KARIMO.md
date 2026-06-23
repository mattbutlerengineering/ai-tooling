# Evaluation: KARIMO

**Repo:** [opensesh/KARIMO](https://github.com/opensesh/KARIMO)
**Stars:** 225 | **Last updated:** 2026-05-11 (pushed; created 2026-02-15) | **License:** Apache-2.0
**Dev loop stage:** Spans the loop as a workflow — Plan (research → PRD interview → task briefs → brief review), Implement/Verify (wave-ordered parallel agent execution with implementer/tester roles), Review (Greptile or Claude Code Review), Ship (merge to main), Reflect (`/karimo:feedback` captures learnings). A PRD-to-merge pipeline, not a single-stage tool.
**Layer:** Process + Tooling — a Claude Code marketplace plugin (~206 files, mostly markdown agent/command/skill definitions plus bash hooks/scripts) that adds a coordination layer on top of Claude Code's native worktrees, sub-agents, and hooks.

---

## What it does

KARIMO is a **PRD-driven autonomous agent orchestration harness plug-in for Claude Code** — "you are the architect, agents are the builders." The model is a three-loop pipeline: **Foundation** (Research → Plan), **Decomposition** (Tasks → Review), **Orchestration** (Orchestrate → Inspect). You drive it through slash commands: `/karimo:research "feature"` creates a PRD folder and discovers patterns/libraries/gaps; `/karimo:plan --prd {slug}` runs a structured interview to capture requirements; `/karimo:run --prd {slug}` generates task briefs from research + PRD, validates them against the codebase, then executes tasks in **waves** (parallel tasks within a wave, sequential waves); `/karimo:merge` opens the final PR to main. Supporting commands cover `dashboard` (velocity metrics), `feedback` (capture learnings), and `doctor` (diagnose).

It positions itself explicitly as a *layer on top of* Claude Code rather than a replacement. The README's own comparison table claims the deltas: native worktree-per-agent **+ branch identity verification**; native task spawning **+ wave-ordered parallelism**; static `model:` param **+ complexity routing and escalation**; worktree persistence **+ git state reconciliation** for crash recovery; and a net-new **+ semantic loop detection** for quality. The repo ships 22 agent definitions (interviewer, pm, researcher, implementer/-opus, tester/-opus, reviewer, brief-writer/-reviewer/-corrector, coverage-reviewer, greptile-remediator, documenter, feedback-auditor, etc.), 11 commands, and skills (bash-utilities, code/doc standards). Adoption is phased: Phase 1 (PRD interviews, agent execution, worktrees, PRs) works out of the box; Phase 2 adds automated review via Greptile (~$30/mo) or Claude Code Review; Phase 3 adds a CLI velocity dashboard.

Distribution is the modern Claude Code path: `/plugin marketplace add opensesh/KARIMO` then `/plugin install karimo@karimo` (with a legacy `install.sh` still available), and the README notes it is in review for the official Anthropic marketplace.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No plugin was installed, no `/karimo:*` command was executed, and no wave orchestration was observed. Every claim is from the repository (GitHub metadata, README, recursive file tree, `plugin.json`), not from measured behavior. The capability deltas ("+ branch identity verification," "+ semantic loop detection," etc.) are the authors' README claims, not verified here; the demo GIF and hosted overview site were not opened.

```bash
gh api repos/opensesh/KARIMO --jq '{desc,stars:.stargazers_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id}'
gh api repos/opensesh/KARIMO/readme --jq '.content' | base64 -d | head -130
gh api "repos/opensesh/KARIMO/git/trees/HEAD?recursive=1" --jq '.tree | length'   # 206 entries
gh api "repos/opensesh/KARIMO/git/trees/HEAD?recursive=1" --jq '[.tree[].path|select(test("agents/.*\\.md$"))]|length'  # 22 agents
gh api "repos/opensesh/KARIMO/git/trees/HEAD?recursive=1" --jq '[.tree[].path|select(test("\\.(js|ts|sh|py)$"))]|length'  # 25 scripts (mostly bash)
gh api repos/opensesh/KARIMO/contents/.claude/plugins/karimo/.claude-plugin/plugin.json --jq '.content' | base64 -d  # v9.10.1
gh api repos/opensesh/KARIMO/releases --jq 'length'   # 30 (page-1 cap)
gh api repos/opensesh/KARIMO/contributors --jq '[.[].login]'  # ["opensesh"] — single author
```

## What worked

- **PRD-first is the right entry point.** Forcing a research pass and a structured interview *before* task generation, then reviewing briefs against the actual codebase before any code is written, front-loads the planning rigor that ad-hoc agent runs skip. The Research→Plan→Tasks→Review→Orchestrate→Inspect spine maps cleanly onto the dev loop.
- **Wave-ordered parallelism with dependencies.** "Parallel within a wave, sequential between waves" is a genuinely better model than fire-all-agents-at-once — it respects task dependencies that naive parallel spawners (claude-squad, gastown) leave to the human.
- **Honest about what's native vs. custom.** The comparison table explicitly credits Claude Code for worktrees, sub-agents, and hooks, and scopes KARIMO's additions to coordination (branch verification, git state reconciliation, loop detection). This is unusually candid framing for a harness and makes the value proposition checkable.
- **Real recovery and resumption thinking.** Git state reconciliation for crash recovery and `/karimo:doctor` for diagnosis show the authors designed for long runs failing midway, not just the happy path. Native cleanup hooks (session/subagent/worktree) are present.
- **Clean distribution and shipped maturity.** Marketplace install, plugin.json at v9.10.1, in review for the official Anthropic marketplace, and verify-scripts (bash-syntax, commit-format, manifest-consistency, template-safety) show repo hygiene.

## What didn't work or surprised us

- **Single author, no external contributors.** The contributor list is `["opensesh"]` alone. For a v9.x harness that orchestrates autonomous code changes across your repo, the bus factor is one — a real adoption risk versus the multi-contributor neighbors.
- **The headline differentiators are unverified prose.** "Branch identity verification," "semantic loop detection," "complexity routing + escalation," "git state reconciliation" are exactly the hard parts — and they are claimed in a README table, not demonstrated. Loop detection and crash recovery in particular are easy to assert and hard to get right.
- **Markdown-and-bash implementation, not compiled logic.** The orchestration lives in 22 agent markdown files and ~25 bash scripts. That is the Claude Code idiom, but it means the "custom coordination layer" is prompt instructions and shell glue, not tested program logic — the opposite end of the engineering spectrum from opencode-swarm's ~2,000-file TypeScript plugin.
- **Real review costs money.** The differentiated quality story (Phase 2) leans on Greptile at ~$30/mo or Claude Code Review; Phase 1 alone gives you orchestration but leaves review to you.
- **Aggressive version number, young repo.** v9.10.1 at under four months old signals fast iteration / churn, not settled stability.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | PRD interview + research + brief-review-against-codebase before coding, plus tester/reviewer/coverage-reviewer agents and optional Greptile/Claude review. Front-loaded rigor; but loop-detection/verification quality is unverified. |
| Speed | + | Wave-ordered parallelism executes independent tasks concurrently while respecting dependencies — faster than serial agent runs, smarter than naive fire-all spawners. |
| Maintainability | + | PRD artifacts, task briefs, learnings capture (`/karimo:feedback`), and dashboards leave a durable paper trail of intent and decisions across a feature. |
| Safety | neutral | Relies on Claude Code's native worktree isolation plus cleanup hooks and template-safety verify scripts; adds branch identity verification (claimed) but no standalone guardrail/scope-enforcement engine of its own. |
| Cost Efficiency | − / neutral | Claims complexity-based model routing/escalation to control cost, but multi-agent waves and the -opus agent variants plus optional $30/mo Greptile push spend up; net effect unverified. |

## Verdict

**CONDITIONAL — strong fit for Claude Code users who want PRD-to-merge structure on real features, with single-maintainer risk noted.** KARIMO's PRD-first, wave-ordered, brief-reviewed pipeline is a coherent and well-framed methodology that maps the whole dev loop onto Claude Code's native primitives, and it is refreshingly honest about which capabilities are native versus its own. The reservations are that its headline differentiators (loop detection, git reconciliation, branch verification) are README claims over markdown/bash rather than verified tested logic, and that it has exactly one contributor on a fast-churning v9.x. Adopt it if you do substantial features (not one-off fixes), live in Claude Code, and want enforced planning before code; pilot on a low-stakes feature first to validate the recovery and loop-detection claims.

Compared to neighbors: against **claude-squad** and **gastown** (parallel-agent shells with no planning or dependency awareness), KARIMO adds the entire PRD→brief→wave→review→merge spine they lack. **agent-orchestrator** is the closest in ambition (plans, spawns parallel agents, handles CI/merge) but is less explicit about PRD discipline and wave dependencies. The sharpest comparison is **opencode-swarm**: both are gated PRD/plan-driven multi-agent harnesses, but Swarm is an OpenCode-only ~2,000-file TypeScript plugin with deep safety guardrails, while KARIMO is Claude-Code-native, markdown-based, and lighter-weight — pick by host (Claude Code → KARIMO, OpenCode → Swarm) and by whether you need Swarm's compiled guardrail engine or KARIMO's leaner PRD methodology.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [KARIMO](https://github.com/opensesh/KARIMO) | plugin | PRD-driven Claude Code harness: research → interview → task briefs → wave-ordered parallel agent execution → review → merge, on native worktrees/sub-agents | Ad-hoc agent runs skip planning and ignore task dependencies; want enforced PRD-to-merge structure with dependency-aware parallelism on Claude Code | claude-squad, gastown (parallel shells, no planning); agent-orchestrator (closest ambition); opencode-swarm (OpenCode-native gated peer) |
