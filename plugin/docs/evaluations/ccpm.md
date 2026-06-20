# Evaluation: ccpm

**Repo:** [automazeio/ccpm](https://github.com/automazeio/ccpm)
**Stars:** 8,207 | **Last updated:** 2026-03-18 (pushed; created 2025-08-18) | **License:** MIT
**Dev loop stage:** Plan and Dev Workflow — a spec-driven pipeline that runs the full inner-to-outer arc: Plan (PRD → epic), Decompose (epic → task files), Ship-coordination (sync to GitHub Issues), and Implement (launch parallel agents per work stream), plus a Track/standup loop. It is a workflow, not a single-stage tool.
**Layer:** Process (an Agent Skill — one `SKILL.md` plus markdown reference docs and bash helper scripts; no runtime daemon, no installed binary — that steers an existing harness through a PM discipline using `git` + `gh` as the only external dependencies)

---

## What it does

CCPM ("Claude Code Project Manager," now rebranded "The Project Manager Agent") is a **spec-driven PM workflow packaged as a portable Agent Skill**. Its thesis: every line of code must trace back to a written spec, so it forces a five-phase discipline — **Plan** (guided brainstorm → PRD → technical epic), **Structure** (decompose epic into numbered task files with dependencies and `parallel: true` flags), **Sync** (push epic + tasks to GitHub Issues as the single source of truth, post progress as comments), **Execute** (analyze an issue into independent work streams and launch multiple agents in a shared git worktree), and **Track** (status, standup, what's-next, what's-blocked, validate).

The signature claim is that **issues aren't atomic**: one "implement auth" issue fans out to ~5 agents (DB, service layer, API, UI, tests) running simultaneously in one worktree, with each agent's context isolated so the main conversation stays a clean "conductor." The signature architectural choice is **GitHub Issues as the database** — no Projects API, no separate PM tool; issue state *is* project state and comments *are* the audit trail, which is what makes human/agent handoffs and team visibility work.

As inspected the skill is small and clean: `skill/ccpm/SKILL.md` (a phase router with a strong description field and a "script-first rule"), five reference docs (`plan`, `structure`, `sync`, `execute`, `track`, plus `conventions`), and **13 deterministic bash scripts** (`status.sh`, `standup.sh`, `next.sh`, `blocked.sh`, `validate.sh`, etc.) that read/report state without spending LLM tokens. It follows the [agentskills.io](https://agentskills.io) open standard, so it installs into Claude Code, Codex, OpenCode, Factory, Amp, and Cursor by symlinking `skill/ccpm/` into the harness's skills directory.

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill was symlinked into a harness, no PRD/epic was created, no GitHub Issues were synced, and no parallel agents were launched. Every claim below comes from the repository (GitHub metadata, README, `SKILL.md`, recursive file tree, CHANGELOG, commit/release counts) — not from observed agent behavior. The "Proven Results" numbers below are the authors' README framing, not anything measured here.

```bash
gh api repos/automazeio/ccpm --jq '{stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'  # 8207★, 832 forks, MIT
gh api repos/automazeio/ccpm/readme --jq '.content' | base64 -d | head -230
gh api "repos/automazeio/ccpm/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # skill/ccpm/{SKILL.md, references/*, references/scripts/*.sh}
gh api repos/automazeio/ccpm/contents/skill/ccpm/SKILL.md --jq '.content' | base64 -d   # 5-phase router + script-first rule
gh api repos/automazeio/ccpm/contents/CHANGELOG.md --jq '.content' | base64 -d | head -20  # local-mode, auto-label creation, accuracy safeguards
gh api repos/automazeio/ccpm/commits --jq 'length'    # 30 (page-1 cap)
gh api repos/automazeio/ccpm/releases --jq 'length'   # 0
```

## What worked

- **The spec-as-database insight is genuinely good.** Using GitHub Issues as the source of truth — not the Projects API, not a bespoke DB — means project state is durable, diffable, visible to the whole team, and survives session/context loss. This is the single most defensible idea in the tool and it directly attacks the "context evaporates between sessions" failure that plagues long agent work.
- **Script-first design is token-disciplined.** Thirteen bash scripts handle every deterministic read (status, standup, next, blocked, validate) so the harness shells out instead of reasoning, with explicit guidance to reserve the LLM only for PRD writing, parallelism analysis, and agent launching. Rare and welcome cost-awareness for a "PM agent."
- **Strong, well-scoped skill description.** The `SKILL.md` description enumerates concrete natural-language triggers ("write a PRD," "sync the X epic," "what's blocked") *and* an explicit do-NOT list (debugging, tests, PR review, raw GitHub ops). This is how you keep a broad skill from over-firing.
- **Real maintenance and portability.** Active CHANGELOG showing community issues resolved (local mode, auto-label creation, accuracy safeguards), `agentskills.io`-standard packaging that runs across 6+ harnesses, and a clean repo that's small enough to read end to end.
- **Full traceability is a safety property.** PRD → Epic → Task → Issue → Code → Commit means every change has provenance — valuable for review, audit, and onboarding, and harder to fake than chat-log "memory."

## What didn't work or surprised us

- **"Proven Results" are unsubstantiated marketing.** "89% less time," "75% fewer bugs," "up to 3× faster," "eval score 100%" — none are backed by a methodology, dataset, or reproducible benchmark in the repo. Treat them as the author's claims, not evidence.
- **The parallel-agents math is optimistic.** "5 agents = 1× wall time vs 5× serial" assumes the work decomposes into 5 truly independent, conflict-free streams editing the same worktree. In practice cross-stream coupling, merge contention, and integration bugs erode that ideal; the README presents the best case as the expected case.
- **GitHub-Issues-as-DB is also a hard dependency and a blast radius.** It requires `gh` auth and a repo, couples your PM state to one vendor, and a misbehaving agent can spray real issues/comments into a shared team tracker. Local mode exists (added per CHANGELOG) but the headline workflow is GitHub-coupled.
- **No tagged releases.** Zero releases despite an active CHANGELOG — you symlink whatever `main` is, with no pinned, versioned bundle, which is awkward for a tool you'd want reproducible across a team.
- **Discipline is only as strong as the harness honors it.** "No vibe coding" is a prompt-level convention, not an enforced gate; nothing prevents an agent from skipping the PRD and coding anyway. The structure helps a cooperative model; it doesn't constrain a non-cooperative one.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Spec-before-code and explicit decomposition reduce ambiguity and scope drift; traceability makes review/verification easier. Offset by unverified bug-reduction claims. |
| Speed | + / − | Parallel work streams can cut wall time when work decomposes cleanly; the up-front PRD/epic/decompose ceremony adds latency to small tasks and the "3×" figure is unproven. |
| Maintainability | + | Requirements live in files and issues, not chat; full PRD→commit provenance aids onboarding and future change. The skill itself is small and readable. |
| Safety | + / − | Audit trail and traceability are safety wins; but it writes real issues/comments to a shared GitHub tracker via `gh` and launches multiple concurrent agents in one worktree — supervise it. |
| Cost Efficiency | + | Script-first rule pushes deterministic reads to bash (no tokens) and isolates per-agent context so the conductor conversation stays small. Among the more cost-aware workflow skills. |

## Verdict

**CONDITIONAL — adopt the spec-as-GitHub-Issues discipline; treat the "proven" numbers and the parallel-velocity math as marketing.** CCPM is a well-built, genuinely portable Agent Skill with one strong idea (issue state = project state, durable across sessions), disciplined token usage (script-first), and a tightly-scoped trigger description. It earns "conditional" rather than "adopt" because its headline benefits — 3× velocity, 75% fewer bugs, conflict-free 5-agent parallelism — are unsubstantiated and assume best-case decomposition, and because the core workflow couples your PM state to GitHub and unleashes concurrent agents on a shared worktree. Good fit for teams already on GitHub Issues who want enforced spec-first traceability; overkill for solo throwaway work.

Compared to neighbors: **spec-kit** and **OpenSpec** are spec-first too but stay local/file-based — CCPM's differentiator is making the *tracker* the database and adding parallel-agent execution. **GSD** is a heavier, opinionated milestone/phase planning system with its own state dir; CCPM is lighter and leans on infra you already have. **beads** is a dependency-aware issue *graph/DB* primitive (it could back a workflow), where CCPM is the workflow itself. **BMAD-METHOD** ships a multi-persona "agile agency"; CCPM is leaner and avoids persona theater. CCPM wins on portability and the GitHub-native single-source-of-truth model; it loses to local-first tools when you don't want vendor coupling.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ccpm](https://github.com/automazeio/ccpm) | skill | Spec-driven PM Agent Skill: PRD → epic → GitHub Issues (as the database) → parallel agents → shipped code, with script-first status/standup tracking | AI coding loses context between sessions and drifts from spec; CCPM forces written specs with full PRD→commit traceability and uses GitHub Issues as durable shared project state | spec-kit, OpenSpec (spec-first but local); GSD, BMAD-METHOD (heavier planning workflows); beads (issue-graph DB a workflow could sit on) |

**Target category:** Dev Workflow (cross-stage Plan→Ship workflow skill; also touches Plan)
