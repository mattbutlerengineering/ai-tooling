# Spike: my own skills / agents / workflow for software development

**Issue:** #181 · **Date:** 2026-06-29 · **Outcome:** assessment + prioritized follow-ups below (no live-config changes made)

Takes stock of **my personal AI-assisted software-development setup** — the skills, agents, rules, and workflow scaffolding I actually run with — and maps it onto this repo's [dev-loop model](../WORKFLOW.md) and five quality signals (Correctness, Speed, Maintainability, Safety, Cost Efficiency). The subject is *my* configuration, not an external tool. Findings are read-only; concrete changes are listed as optional follow-ups.

## What was inventoried

Sources walked on 2026-06-29 (host: this machine):

| Source | Location | Count |
|--------|----------|-------|
| Global skills | `~/.claude/skills/` | 55 |
| Global agents | `~/.claude/agents/` | **0** (empty — all subagents come from plugins) |
| Global rules | `~/.claude/rules/common/` | 10 |
| Repo skills | `.claude/skills/` + `.agents/skills/` | 3 (`add-catalog-entry`, `find-catalog-gaps`, `find-skills`) |
| Installed plugins | `~/.claude/plugins/` | 40 |
| Workflow scaffolding | global `CLAUDE.md`, slash-commands (`/loop`, `/implement-issue`, `/to-issues`, `/review`, `/tdd`, …) | — |

The 10 rules (`coding-style`, `testing`, `git-workflow`, `development-workflow`, `implementation-discipline`, `security`, `performance`, `agents`, `patterns`, `hooks`) are the *process spine* — they encode HOW work is done; the skills are the verbs.

## Inventory mapped to the dev loop

Each skill/cluster placed at the dev-loop stage it serves, with the quality signal(s) it moves. (C=Correctness, S=Speed, M=Maintainability, Sf=Safety, $=Cost.)

### Inner loop

| Stage | Skills / agents / plugins | Signals |
|-------|---------------------------|---------|
| **Plan** | `to-prd`, `grill-me`, `grill-with-docs`, `prototype`, `zoom-out`, superpowers `brainstorming` | C, M |
| **Implement** | `implement-issue`, `implement`, `tdd`, `agent-browser`, `typescript-mcp-server-generator`, `skill-creator`/`write-a-skill`, `feature-dev` (agents) | C, S |
| **Verify** | `tdd`, `diagnose`/`diagnosing-bugs`, `web-quality-audit` (+ `accessibility`, `core-web-vitals`, `performance`, `seo`, `best-practices`, `web-design-guidelines`), `playwright`, `semgrep`, `*-lsp` plugins | C, Sf |
| **Review** | `review`, `caveman-review`, `code-review`/`pr-review-toolkit`/`code-simplifier` (agents), `greptile` | C, M, Sf |
| **Ship** | `caveman-commit`, `resolving-merge-conflicts`, `commit-commands` | S, Sf |
| **Reflect** | `handoff`, `learned`, `graphify`, `documentation`/`documentation-and-adrs`/`documentation-writer`/`oo-component-documentation`, `claude-mem`, `claude-reflect` | M, $ |

### Outer loop

| Stage | Skills / agents / plugins | Signals |
|-------|---------------------------|---------|
| **Discover** | `find-skills`, `last30days`, `find-catalog-gaps` (repo), `context7` | C, S |
| **Architect** | `domain-modeling`, `codebase-design`, `improve`, `improve-codebase-architecture` | M |
| **Decompose** | `to-issues`, `triage` | S, M |
| **Integrate** | *(thin — see gaps)*; `github` plugin, CI gates | Sf |
| **Retrospect** | `claude-reflect`, `last30days`, `graphify` | M, $ |

### Cross-cutting

| Concern | Tooling | Signals |
|---------|---------|---------|
| **Cost / token** | `caveman` family (5: `caveman`, `-commit`, `-review`, `-compress`, `-help`), `handoff` | $ |
| **Autonomy** | `/loop`, `ralph-loop`, `implement-issue`, `triage` | S, $ |
| **Security** | `security-best-practices`, `security-guidance`, `semgrep`, `auth0` | Sf |
| **Observability** | `sentry` plugin only | Sf |
| **Non-dev (comms/writing)** | `teach`, `pitch-deck`, `powerpoint`/`powerpoint-ppt`, `slidev`, `writing-beats`/`-fragments`/`-shape` | — |

## Gaps

Stages and signals with thin or no personal tooling:

- **Integrate (outer loop) is the weakest stage.** No personal skill for release/CHANGELOG/versioning or CI/CD orchestration — relies entirely on `implement-issue`'s per-PR merge and the `github` plugin. The cross-repo "integrate many slices into a coherent release" job has no owner.
- **Observability is plugin-only.** `sentry` covers errors; there is no personal skill closing the loop from production signal → Reflect → a rule or backlog item. The dev loop's feedback arc is manual.
- **Cost Efficiency is compressed but not *measured*.** The `caveman` family *reduces* tokens; nothing *reports* tokens-per-session or flags redundant tool calls, so the `$` signal can't be tracked over time. (This repo's own `token-savings-protocol.md` is the kind of instrument missing globally.)
- **Ship beyond commit.** `caveman-commit` writes the commit; PR description / changelog generation lives only inside `implement-issue`. No standalone Ship skill for non-pipeline work.
- **No personal subagents.** `~/.claude/agents/` is empty — every subagent type is plugin-supplied. Recurring personal patterns (e.g. an eval-runner-style worker, a triage worker) are re-described inline each time rather than captured.

## Overlaps & redundancy

Clusters where multiple skills cover the same job — candidates to consolidate or pick a default:

- **Documentation ×4:** `documentation`, `documentation-and-adrs`, `documentation-writer`, `oo-component-documentation`. Overlapping triggers; no clear "use X for Y" boundary. Likely collapse to `documentation-and-adrs` (decisions) + one writing skill.
- **Debug ×2:** `diagnose` and `diagnosing-bugs` are near-duplicates (same reproduce→minimise→fix loop). One supersedes the other — pick one, retire the other.
- **Web quality ×7:** `web-quality-audit` is the umbrella over `accessibility`, `core-web-vitals`, `performance`, `seo`, `best-practices`, `web-design-guidelines`. Fine *if* the umbrella delegates; redundant if all seven trigger independently. Confirm the umbrella pattern.
- **Review ×2:** `review` (two-axis) vs `caveman-review` (compressed). Complementary (verbosity), but two `/review` triggers can collide.
- **Implement ×2:** `implement` (PRD/issue-set) vs `implement-issue` (single issue). Boundary is real but easily confused — document which to reach for.
- **Skill authoring ×2:** `skill-creator` vs `write-a-skill`. Same job.
- **Plan-grilling ×2:** `grill-me` vs `grill-with-docs` (the latter adds doc updates — keep both only if the doc-update path earns it).
- **Presentations ×4 / Writing ×3:** `pitch-deck`/`powerpoint`/`powerpoint-ppt`/`slidev` and `writing-beats`/`-fragments`/`-shape`. Out of the dev loop, but heavy; the writing trio is a deliberate pipeline, the presentation four are substitutable.

## Stale / unused

- **`everything-claude-code` + `everything-claude-code-conventions`** share an identical generic description ("Development conventions … JavaScript project with conventional commits") — look auto-generated and possibly stale; verify they still reflect a real project.
- **`caveman-help`** (and arguably `caveman-compress`) — the caveman family is 5 skills; confirm the long tail is actually invoked.
- **Empty `~/.claude/agents/`** — not stale so much as an unused capability (see gaps).

## Recommendation

The setup is **strong on the inner loop and Plan/Architect, weak on Integrate, Observability, and cost *measurement*** — and carries a consolidation debt in the documentation, debug, and web clusters. Prioritized, each as its own optional follow-up (none done here):

1. **Consolidate the obvious duplicates first (cheapest, highest clarity win):** retire one of `diagnose`/`diagnosing-bugs` and one of `skill-creator`/`write-a-skill`; verify the `everything-claude-code*` pair isn't dead. Pure pruning, reversible.
2. **Pick defaults for the doc and web clusters** — document a one-line "use X for Y" routing in the relevant rule so the 4 doc / 7 web skills don't all fire. No deletion required.
3. **Close the Integrate gap:** a small Ship/release skill (CHANGELOG + version + PR-description) usable outside `implement-issue`. Moves S and Sf.
4. **Instrument Cost Efficiency:** adopt a tokens-per-session report (the global analogue of this repo's `token-savings-protocol.md`) so `$` becomes trackable, not just compressible.
5. **Capture recurring subagents:** author 1–2 personal agents in `~/.claude/agents/` for patterns currently re-described inline (e.g. an eval/triage worker), per the global-`CLAUDE.md` note that the registry is snapshotted at session start.
6. **Defer** the presentation/writing-cluster cleanup — out of the dev loop; low leverage on code quality.

Each numbered item is independently grabbable as a `ready-for-agent` issue if you want them tracked.

## Sources

- Local inventory: `~/.claude/skills/` (55), `~/.claude/rules/common/` (10), `~/.claude/plugins/installed_plugins.json` (40 plugins), `~/.claude/agents/` (empty), this repo's `.claude/skills/` + `.agents/skills/`, global `~/.claude/CLAUDE.md`.
- Mapping frame: [`WORKFLOW.md`](../WORKFLOW.md) dev-loop stages + Quality Signals; [`STACK.md`](../STACK.md); [`evaluations/token-savings-protocol.md`](../evaluations/token-savings-protocol.md).
