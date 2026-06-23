# Evaluation: agency-agents

**Repo:** [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
**Stars:** 114,550 | **Last updated:** 2026-06-18 (pushed; created 2025-10-13) | **License:** MIT
**Dev loop stage:** Spans the loop by *role*, not by stage — it ships personas for Plan (software-architect), Implement (frontend/backend/mobile/senior-dev), Review (code-reviewer), and outer-loop Architect/Decompose (multi-agent-systems-architect). It is a persona library, not a workflow.
**Layer:** Process (a portable collection of agent-definition markdown files installed into each tool's agent directory; no runtime, no code that executes)

---

## What it does

The catalog one-liner: "Complete AI agency with specialized expert agents (frontend, marketing, QA, etc.)." Born from a Reddit thread, **The Agency** is a large, growing library of single-file agent *personas* — each a markdown file with identity, personality, workflow, technical deliverables, and success metrics. As inspected, it ships **271 agent markdown files across 16 "divisions"** (engineering, design, finance, game-development, gis, marketing, paid-media, product, project-management, sales, security, spatial-computing, specialized, support, testing, academic). The catalog's one-liner is now stale — this is far past "frontend, marketing, QA."

The mechanism is install-and-activate, not orchestration. `scripts/install.sh` copies the persona files into your tool's agent directory (`~/.claude/agents/` for Claude Code, with `scripts/convert.sh` generating integration files for Antigravity, Gemini CLI, OpenCode, Copilot, Cursor, Aider, Windsurf, Kimi, Codex). You then activate one in-session ("activate Frontend Developer mode"). There is no coordinator, no task router, no shared memory — "agency" is a metaphor for the *roster*, not a running team. A `divisions.json` is the source of truth for the division set, and CI (`check-divisions.yml`, `lint-agents.yml`) enforces that directories, install/convert scripts, and that manifest stay in sync — a notably disciplined repo-hygiene setup for a persona collection.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No persona was installed, no `install.sh`/`convert.sh` was executed, and no agent was activated in any tool. Every claim below comes from the repository (GitHub metadata, README, full recursive file tree, `divisions.json`, commit/contributor counts), not from observed agent behavior. The "battle-tested / proven deliverables / success metrics" language is the authors' README framing, not anything I measured.

```bash
gh api repos/msitarzewski/agency-agents --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id}'
gh api repos/msitarzewski/agency-agents/readme --jq '.content' | base64 -d
gh api "repos/msitarzewski/agency-agents/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/msitarzewski/agency-agents/contents/divisions.json --jq '.content' | base64 -d   # 16 divisions
gh api "repos/msitarzewski/agency-agents/git/trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|endswith(".md"))|select(.path|test("/"))]|length'  # 271
gh api repos/msitarzewski/agency-agents/commits --jq 'length'        # 30 (page-1 cap)
gh api repos/msitarzewski/agency-agents/releases --jq 'length'       # 0
gh api repos/msitarzewski/agency-agents/contributors --jq '[.[].login]'  # ~30 incl. many one-off PR authors
```

## What worked

- **Breadth and portability.** 271 personas across 16 domains, installable into 10+ tools via one converter. If you want a ready-made "backend architect" or "code reviewer" persona without writing one, the menu is enormous and cross-tool by design.
- **Genuine community traction and contribution flow.** 114K stars, ~18.7K forks, ISSUE_TEMPLATEs (including `new-agent-request.yml`), CONTRIBUTING (EN + zh-CN), and a steady stream of contributor PRs adding agents. This is a living, community-fed roster, not a one-shot dump.
- **Surprisingly disciplined repo hygiene.** `divisions.json` as a single source of truth, plus CI that fails the build if the manifest, on-disk directories, and the install/convert/lint scripts disagree. For a persona collection that could easily rot, this is real maintenance engineering.
- **Each file is self-contained and readable.** A persona is one markdown file with identity, workflow, deliverables, and metrics — easy to read, fork, and adapt even if you never run the installer. Strong as a *reference* for writing your own agents.
- **Some genuinely useful, dev-relevant personas exist** — `engineering-minimal-change-engineer` (minimum-viable diffs, no scope creep), `engineering-code-reviewer`, `engineering-software-architect`, `engineering-codebase-onboarding-engineer` align with real dev-loop needs.

## What didn't work or surprised us

- **"Personality-driven" cuts against quality.** The README sells "whimsy injectors," "Reddit community ninjas," and "unique voice." For software work, persona theater adds tokens and stylistic noise without improving correctness — the opposite of the lean, verifiable instructions our better catalog entries favor.
- **271 agents is a discovery and bloat problem, not a feature.** The README itself notes OpenCode silently drops agents past ~119 and recommends installing only a subset. A roster this large is mostly a menu you must curate down — installing all of it pollutes the agent namespace and the model's choice space.
- **Roster, not orchestration.** There is no coordinator, router, or shared state. "Complete AI agency" overstates it: you get a pile of personas and activate them one at a time by hand. Compared to harness-level orchestration (claude-squad, agent-orchestrator), there is no actual teamwork.
- **Unverifiable "proven / battle-tested / success metrics" claims.** Every persona advertises "measurable outcomes" and "success metrics," but nothing in the repo substantiates them; they are prompt copy, not evidence.
- **Star count is virality, not validation.** 114K stars on an 8-month-old "assemble your dream AI team" persona pack reflects the Reddit-origin meme appeal and forkability far more than demonstrated coding outcomes. Quality varies widely file-to-file given the open-contribution model.
- **No releases / no versioning of the set.** Despite the CI discipline, there are 0 tagged releases — you install whatever `main` is, with no stable, pinned bundle.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A focused persona (e.g. code-reviewer, minimal-change-engineer) can sharpen behavior on a task, but personality framing and unverified "metrics" add no real correctness guarantee. |
| Speed | + / − | Ready-made personas save the time of writing your own; offset by the discovery cost of curating 271 files and the per-tool agent-limit ceilings. |
| Maintainability | neutral | The *repo* is well-maintained (divisions.json + CI), but for your project the personas are just instructions — no effect on your codebase's maintainability. |
| Safety | neutral | Pure markdown agent definitions; no code executes, no network/host reach. Risk is only that a verbose persona steers behavior in unintended ways. |
| Cost Efficiency | − / neutral | Personality-heavy prompts spend extra tokens per activation for stylistic flavor that doesn't move outcomes; installing many agents enlarges the model's choice surface. |

## Verdict

**CONDITIONAL — cherry-pick a handful of engineering personas; do not install the agency.** agency-agents is a large, genuinely community-maintained, cross-tool persona library with better repo hygiene than most of this catalog. But "complete AI agency" is marketing for "271 single-file personas you activate by hand" — there is no orchestration, the personality framing adds token cost and stylistic noise rather than correctness, and the "proven/battle-tested" claims are unsubstantiated. The right move is to lift 3-5 dev-relevant files (code-reviewer, software-architect, minimal-change-engineer, codebase-onboarding-engineer) as reference or starting points, not to bulk-install the roster.

Compared to neighbors: **gstack** is a *curated, opinionated* setup (~53 skills chosen and integrated), and **harness** (revfactory) actually *generates* a tailored team for your domain — both are more useful than a 271-file undifferentiated menu. **claude-code-staff-engineer** at least adds hierarchical coordination (a lead engineer routing specialists), which agency-agents lacks entirely. agency-agents wins only on raw breadth and portability; for shipping code, a small curated set beats a giant uncoordinated roster.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agency-agents](https://github.com/msitarzewski/agency-agents) | harness | 271 single-file "expert" agent personas across 16 divisions, installable into 10+ tools — a roster you activate by hand, not an orchestrated team | Want ready-made specialist agent definitions to copy/adapt rather than writing each persona from scratch | gstack, harness (curated/generated teams); claude-code-staff-engineer (adds coordination agency-agents lacks) |
