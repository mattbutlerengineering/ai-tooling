# Evaluation: Claude-Code-Game-Studios

**Repo:** [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
**Stars:** 21,922 | **Last updated:** 2026-05-21 (pushed; created 2026-02-12) | **License:** MIT
**Dev loop stage:** Spans the whole loop *for one domain* — Plan (brainstorm, GDD, epics/stories), Implement (engine specialists), Verify/Review (QA, design review, director gates), Ship (release-manager), Reflect (sprint retrospective hook). It is a full game-studio workflow scaffold, not a single-stage tool.
**Layer:** Process + Tooling — a `.claude/` directory you copy into a game project: agent personas + slash-command skills + lifecycle hooks + path-scoped rules + document templates, all wired into a studio hierarchy. No runtime of its own.

---

## What it does

A domain pack that, per its tagline, turns "a single Claude Code session into a full game development studio." It ships **49 agents, 73 skills (slash commands), 12 hooks, 11 rules, and 41 document templates** as a drop-in `.claude/` directory. The premise: a lone chat session has no structure — nothing stops you hardcoding magic numbers, skipping design docs, or shipping unreviewed spaghetti — so this imposes the structure of a real studio.

The 49 agents are organized into a **three-tier hierarchy**: Tier-1 Directors on Opus (`creative-director`, `technical-director`, `producer`) who guard vision and own quality gates; Tier-2 Department Leads on Sonnet (`game-designer`, `lead-programmer`, `art-director`, `audio-director`, `narrative-director`, `qa-lead`, `release-manager`, `localization-lead`); and Tier-3 Specialists on Sonnet/Haiku (gameplay/engine/ai/network/tools/ui programmers, designers, technical-artist, sound-designer, writer, world-builder, ux, prototyper, performance-analyst, devops, analytics, security, qa-tester, accessibility, live-ops, community). It additionally ships **per-engine specialist sets** for Godot 4 (GDScript/shader/GDExtension), Unity (DOTS, shaders/VFX, addressables, UI Toolkit), and Unreal 5 (GAS, Blueprints, replication, UMG). The 73 skills are workflow slash commands (`/start`, `/design-system`, `/create-epics`, `/create-stories`, `/dev-story`, `/story-done`, `/adopt`, `/setup-engine`, etc.) covering brainstorm → GDD → epics/stories → dev → QA → release. Unlike most persona packs, it backs the roster with **executable hooks** (`validate-commit.sh`, `validate-push.sh`, `validate-assets.sh`, `detect-gaps.sh`, `session-start/stop.sh`, agent audit logging) and **path-scoped rules** that enforce coding standards on gameplay/engine/AI/UI/network code, plus extensive `docs/` (coordination map, director gates, review workflow) and `templates/` (GDD, art-bible, economy-model, ADR, post-mortem).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `.claude/` directory was copied into a project, no agent activated, no slash command or hook executed, and no game engine was present. The "coordinated AI team" and quality-gate behavior are the README's design claims; the hooks are real shell scripts but were not executed. Every statement comes from repository metadata, README, and the full recursive file tree.

```bash
gh api repos/Donchitos/Claude-Code-Game-Studios --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/Donchitos/Claude-Code-Game-Studios/readme --jq '.content' | base64 -d | head -120
gh api "repos/Donchitos/Claude-Code-Game-Studios/git/trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|test("\\.claude/agents/.+\\.md"))]|length'   # 49 agents
gh api "repos/Donchitos/Claude-Code-Game-Studios/git/trees/HEAD?recursive=1" --jq '.tree[].path' | grep -c '\.claude/skills/.*SKILL.md'    # 73 skills
gh api "repos/Donchitos/Claude-Code-Game-Studios/git/trees/HEAD?recursive=1" --jq '.tree[].path' | grep '\.claude/hooks/'   # 12 hooks
gh api repos/Donchitos/Claude-Code-Game-Studios/commits  --jq 'length'    # 30 (page-1 cap)
gh api repos/Donchitos/Claude-Code-Game-Studios/releases --jq 'length'    # 5
```

## What worked

- **Real orchestration, not just a roster.** Unlike agency-agents (a flat persona menu), this has an explicit Director→Lead→Specialist hierarchy with documented escalation paths, director gates, a coordination map, and a `/adopt` flow for existing projects. The structure is the product, and it is genuinely designed for hand-off between tiers.
- **Backed by enforcement, not vibes.** It ships 12 actual hooks (commit/push/asset validation, gap detection, agent audit logging, session lifecycle) and 11 path-scoped rules. Quality gates are wired into git and session events, which is far more than markdown personas promising "success metrics."
- **Sensible model tiering.** Directors on Opus, leads on Sonnet, specialists on Sonnet/Haiku is a cost-aware allocation that matches Anthropic's own guidance (reserve Opus for the few high-leverage reasoning roles).
- **Broad, coherent engine coverage.** First-class agent sets for Godot, Unity, and Unreal — the three engines that actually matter — with sub-specialists for the gnarly bits (GAS, DOTS, shaders, replication).
- **Strong artifact scaffolding.** 41 templates (GDD, art-bible, economy-model, ADRs, post-mortems) plus an `/adopt` command make it usable on a real project, not just greenfield.
- **Massive traction.** 21.9K stars and 3.1K forks in ~3 months signals strong resonance with solo/indie game devs.

## What didn't work or surprised us

- **Single domain, single use case.** This is exclusively for game development. Outside that domain it is irrelevant — there is no general-purpose value to lift the way you might cherry-pick an "engineering" persona from a broad pack.
- **49 agents + 73 skills is a lot of surface to install whole.** A studio scaffold this large risks polluting the agent namespace and the model's choice space (the same per-host agent-limit and discovery problems that plague big rosters). It is a commitment, not a sprinkle.
- **Single-maintainer, donation-funded, only 5 releases.** Buy-Me-a-Coffee / GitHub Sponsors badges and one primary author (Donchitos) mean sustainability rests on one person. The star count vastly outruns demonstrated production game shipments.
- **Process theater risk.** Imposing directors, gates, GDDs, and sprint retrospectives on a solo project can be heavyweight for small games — the structure that helps a 6-month project may smother a game-jam prototype. There's a `/project-stage-detect` to scale it, but the default ceremony is high.
- **Effectiveness unverified.** "Catches mistakes early," "guards the vision," and the quality of 49 personas were not observed; star count is virality among indie devs, not evidence of better-shipped games.
- **Last push 2026-05-21** — roughly a month stale at time of writing, modest for a fast-moving ecosystem (though not alarming for a stable scaffold).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (game dev only) | Path-scoped rules, design/QA review agents, and director gates push back on hardcoded values and unreviewed code — real correctness pressure, but only within game projects. |
| Speed | + / − | Pre-built studio workflow and engine specialists skip a huge amount of setup; offset by the ceremony overhead (GDDs, gates, sprint rituals) that can slow small projects. |
| Maintainability | + | Templates (ADRs, GDDs, art-bible), coding-standards rules, and structured docs actively push a game project toward maintainable artifacts and recorded decisions. |
| Safety | − (review hooks) | 12 shell hooks run on commit/push/session events and execute on the host; benign by inspection but unverified — review the scripts before enabling, as with any hook pack. |
| Cost Efficiency | + / − | Opus-only-for-directors tiering is cost-aware; offset by the token weight of 49 agents + 73 skills + templates loaded into a session and multi-tier hand-offs. |

## Verdict

**CONDITIONAL — adopt as a whole if you are building a non-trivial game with Claude Code; otherwise SKIP.** Claude-Code-Game-Studios is the most *complete* domain workflow pack in this catalog: it is the rare collection that pairs a real orchestration hierarchy with executable enforcement (hooks + path-scoped rules), cost-aware model tiering, engine-specific specialists, and document scaffolding. For a serious game project it is close to ADOPT and clearly beats wiring this up by hand. But it is single-domain and single-maintainer, the ceremony is heavy for tiny projects, and the 49-agent/73-skill surface is an all-in commitment with the usual hook-review caveat — so it earns CONDITIONAL, gated on (a) you're actually shipping a game and (b) you've reviewed the hooks and right-sized the process via `/project-stage-detect`.

Compared to neighbors: it is the structural opposite of **agency-agents** (a flat 271-persona menu with *no* coordinator) — Game Studios actually orchestrates via a Director→Lead→Specialist hierarchy with gates and hooks, which is the teamwork agency-agents only gestures at. Against the **harness** meta-skill (which *generates* a domain team on demand), Game Studios is the pre-built, opinionated, battle-coherent alternative for the specific domain it covers. Against general/role packs like **mattpocock/skills** or **alirezarezvani/claude-skills**, it trades cross-domain breadth for end-to-end depth in one vertical. As a domain collection it is best-in-class; its weakness is simply that the domain is narrow.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | harness | Drop-in `.claude/` game studio: 49 hierarchical agents (Director→Lead→Specialist), 73 workflow skills, 12 enforcement hooks, 11 rules, 41 templates, with Godot/Unity/Unreal specialist sets | Want an orchestrated, quality-gated game-dev workflow in Claude Code instead of an unstructured single chat session | agency-agents (flat persona menu, no orchestration), harness (generates domain teams), pm-skills / marketingskills (single-domain packs) |
