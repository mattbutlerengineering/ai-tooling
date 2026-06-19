# Evaluation: gastown

**Repo:** [gastownhall/gastown](https://github.com/gastownhall/gastown)
**Stars:** 15,976 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Implement + Ship (also Plan/Review — convoys, merge queue, escalation)
**Layer:** Infrastructure (a full coordination substrate, not a single tool)

---

## What it does

Catalog one-liner: "Multi-agent workspace manager." Gas Town (by Steve Yegge) is a Go-based orchestration *system* for running many AI coding agents — Claude Code (the default runtime), Codex, Gemini, GitHub Copilot — against one or more git repos, with work state persisted in a git-backed ledger so agents survive restarts and crashes.

The mechanism is a small civic-themed object model layered on git + tmux + a database. A **Town** (`~/gt/`) is your workspace. A **Rig** wraps one git repository. **Polecats** are worker agents with persistent identity but ephemeral sessions. Each agent gets a **Hook** — a dedicated **git worktree** — so concurrent agents have filesystem isolation and never touch each other's working trees (this is the conflict-prevention primitive, same as dmux/worktrunk). Work itself is tracked as **Beads** (Yegge's git-backed issue ledger, also in the catalog) bundled into **Convoys**. You drive it through **the Mayor**, a Claude Code coordinator session you `gt mayor attach` to and tell what to build; the Mayor creates convoys, `gt sling`s beads to agents, and reports progress.

Beyond isolation, Gas Town adds an autonomous operations layer most peers lack: a **Refinery** per-rig merge queue (Bors-style bisecting queue — polecats never push to main directly; completed work is batched, verification-gated, and merged, with failing MRs isolated by bisection); a three-tier watchdog (**Witness** per-rig lifecycle manager, **Deacon** background supervisor, **Dogs** maintenance workers) for stuck-agent detection and recovery; severity-routed **Escalation** (`gt escalate`); a config-driven **Scheduler** to cap concurrency and avoid API rate-limit exhaustion; **Seance** for session discovery/continuation across predecessor agents; **Molecules** (TOML workflow templates); and **Wasteland**, a federated cross-town work network over DoltHub. The stated scaling claim is 20–30 agents, vs. the "4–10 becomes chaos" baseline. It ships Claude Code skills (`crew-commit`, `pr-sheriff`, etc.), slash commands, an `AGENTS.md`, and 13 internal plugins (compactor-dog, github-sheriff, quality-review, …).

## How we tested it

Inspected the repo metadata, full README, repository tree, release/tag history, contributor count, open-issue stream, and the `.claude/` (skills + commands) and `plugins/` directories via the GitHub API. **Did not install or run it.** Running it meaningfully requires Go 1.25+, Dolt, beads, tmux, sqlite3, and at least one agent CLI, then provisioning a multi-agent town — an interactive, stateful, long-running setup rather than a scriptable one-shot command. This is a repo/README/structure review, not hands-on usage. No timing, throughput, or "scales to 20–30 agents" numbers are claimed here; those are the project's.

```bash
gh api repos/gastownhall/gastown --jq '{stars,license,description,pushed_at,created_at,forks,open_issues,language}'
gh api repos/gastownhall/gastown/readme --jq '.content' | base64 -d
gh api "repos/gastownhall/gastown/git/trees/HEAD" --jq '.tree[].path'
gh api repos/gastownhall/gastown/contributors --jq 'length'        # 30
gh api repos/gastownhall/gastown/releases --jq '.[0:5] | .[] | {tag,date: .published_at}'  # v1.2.1 .. v1.0.0
gh api "repos/gastownhall/gastown/contents/.claude/skills" --jq '.[].name'
gh api "repos/gastownhall/gastown/contents/.claude/commands" --jq '.[].name'
gh api "repos/gastownhall/gastown/contents/plugins" --jq '.[].name'
gh api "repos/gastownhall/gastown/issues?state=open&per_page=5" --jq '.[].title'
# Catalog overlap + parallel-agent cluster:
grep -inE "gastown|claude-squad|dmux|worktrunk|beads" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Genuinely mature and active — not a thin repo.** 16K stars, 30 contributors, semver releases through v1.2.1 (v1.0.0 in April 2026, steady cadence), MIT, pushed within 2 days of evaluation. Open issues are detailed bug reports about real subsystems (Dolt connection storms under patrol load, schema migrations, merge-queue internals), which is the signature of a system in real use, not a demo.
- **Conflict prevention is the proven primitive done right.** Hook = git worktree per agent gives true filesystem isolation, the same low-magic approach as dmux/worktrunk — Gas Town doesn't reinvent it, it builds on it.
- **It adds the autonomous-ops layer the lightweight peers deliberately omit.** A Bors-style bisecting merge queue (polecats never push to main), a three-tier watchdog with stuck-agent recovery, severity-routed escalation, and a concurrency scheduler to avoid rate-limit exhaustion. This is the actual differentiator: dmux/claude-squad give you a cockpit to *watch and merge* a handful of agents; Gas Town tries to *autonomously run a fleet* with self-healing and gated merges.
- **First-class Claude Code integration.** Claude Code is the default runtime; ships `.claude/` skills (crew-commit, pr-sheriff, ghi-list, pr-list), slash commands, an `AGENTS.md`, and 13 internal plugins. The Mayor is itself a Claude Code session. This fits the catalog's Claude-Code-centric lens better than agent-agnostic-but-Claude-secondary tools.
- **Persistence is the headline.** Work state lives in the git-backed Beads ledger and worktree hooks, so agent restarts/crashes don't lose context — directly attacking the "work state lost in agent memory" failure mode. Seance lets a new agent interrogate predecessor sessions.

## What didn't work or surprised us

- **Not validated hands-on here.** Everything above is from README/structure/issues. Claims about 20–30-agent scaling, merge-queue reliability, and watchdog recovery are the project's, not observed.
- **Very heavy install and a large conceptual surface.** Go 1.25+, Dolt, beads, sqlite3, tmux, plus an agent CLI — and a glossary of ~15 bespoke concepts (Town/Rig/Polecat/Hook/Convoy/Bead/Molecule/Refinery/Deacon/Witness/Seance/Wasteland…). The civic metaphor is charming but the learning curve and operational footprint are an order of magnitude above dmux or claude-squad.
- **macOS `go install` is broken by design.** Unsigned binaries get SIGKILLed; you must `brew install` or build via `make`. `go install` is Linux-only. A real friction point the README itself flags.
- **Hard external dependency on Dolt + DoltHub.** The ledger and the Wasteland federation ride on Dolt (a versioned SQL database). That's an unusual, non-trivial dependency, and the open issues show Dolt-layer instability (connection storms wedging the sql-server under load).
- **Path inconsistency in the docs.** README install commands reference `github.com/steveyegge/gastown` and `github.com/steveyegge/beads`, but the canonical repo is `gastownhall/gastown` (non-fork, source null) — an org rename/move not fully propagated into the README. Minor, but a maintenance signal and a small friction for `go install`/clone.
- **Overkill for the common case.** For one-to-a-few agents this is enormous machinery. The 20–30-agent target is a real but narrow audience.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Bisecting merge queue with verification gates keeps broken work off main; isolation prevents agents corrupting each other's trees. Correctness of the *code* still depends on the agents + your gates. |
| Speed | + | Many agents run truly in parallel in isolated worktrees; autonomous dispatch/merge removes manual coordination — at the cost of heavy setup before you get there. |
| Maintainability | + | Worktree-per-agent + git-backed Beads ledger + persistent identity keep history and work state clean and recoverable across crashes/restarts. |
| Safety | + | Polecats never push to main (gated merge queue); three-tier watchdog detects/recovers stuck agents; severity-routed escalation surfaces blockers instead of silent stalls. |
| Cost Efficiency | neutral | Free/MIT and the Scheduler caps concurrency to avoid rate-limit waste, but running 20–30 agents multiplies underlying token spend dramatically; this is a throughput play, not a savings play. |

## Verdict

**CONDITIONAL**

Adopt Gas Town when you are deliberately running a **large fleet (10–30) of coding agents** on real repos and need autonomous orchestration — gated merge queue, stuck-agent recovery, persistent crash-survivable work state, and escalation — and you can absorb a heavy install (Go, Dolt, beads, tmux) and a sizable conceptual model. It is a mature, actively developed (v1.2.1, 30 contributors, 16K stars) system with first-class Claude Code integration, and it is the most complete autonomous multi-agent operations substrate in this cluster of the catalog. It is decisively **not** a default: for a single agent, or for the "watch and merge a handful of agents" use case, it is massive overkill — reach for dmux or claude-squad instead. Re-evaluate the Dolt-layer stability (current open issues) and the unsigned-macOS-binary friction before committing a team to it.

**vs. the parallel-agent / worktree cluster.** All four share the worktree-isolation primitive but sit at very different weights:
- **worktrunk** — a thin, scriptable Rust CLI for worktree management. A building block, no orchestration.
- **dmux** — an interactive tmux + Ink/React TUI cockpit to launch, watch, browse, and one-step-merge a handful of agents. Agent-agnostic. CONDITIONAL.
- **claude-squad** — manages multiple Claude/Codex/Amp terminal sessions in parallel; visibility-oriented, lighter than Gas Town.
- **gastown** — the heavyweight: not a cockpit but an **autonomous operations system** (merge queue, watchdogs, scheduler, escalation, federated work network, persistent ledger) aimed at 20–30 agents.

Gas Town is **additive, not a thinner duplicate** — it occupies the "fleet + autonomy + self-healing" end of the spectrum that dmux/claude-squad deliberately leave empty, at the cost of being far heavier. Within the catalog it also overlaps with **agent-orchestrator** (autonomous spawn + conflict resolution) and complements **beads** (its own work ledger, separately cataloged). The existing catalog "overlaps with claude-squad, sandcastle" is accurate but understates that the real distinction is autonomy/scale, not topology.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gastown](https://github.com/gastownhall/gastown) | tool | Multi-agent workspace manager | Need to coordinate multiple agents sharing a workspace without conflicts | claude-squad, sandcastle |
