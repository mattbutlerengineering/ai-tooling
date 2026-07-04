# Evaluation: addyosmani/agent-skills

**Repo:** [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
**Stars:** 62,906 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** All (full lifecycle: Spec → Plan → Build → Test → Review → Ship)
**Layer:** Tooling

---

## What it does

24 engineering skills organized around a 6-phase development lifecycle, with 7 slash commands (`/spec`, `/plan`, `/build`, `/test`, `/review`, `/code-simplify`, `/ship`) that activate the right skills automatically. Ships as a Claude Code plugin with 4 specialist agents (code-reviewer, security-auditor, test-engineer, web-performance-auditor), a SessionStart hook that injects a meta-skill discovery flowchart, and 5 shared reference documents (accessibility, performance, security checklists, testing patterns, orchestration patterns).

The key mechanism is `/build auto` — approve a plan once, and the agent implements every task autonomously with per-task test-driven verification and individual commits. Skills also auto-activate based on context: designing an API triggers `api-and-interface-design`, building UI triggers `frontend-ui-engineering`.

Standout skills beyond the standard lifecycle:
- **doubt-driven-development** — spawns a fresh-context adversarial reviewer for non-trivial decisions mid-flight (not post-hoc like `/review`)
- **context-engineering** — structured 5-level context hierarchy with concrete CLAUDE.md templates
- **source-driven-development** — read source code instead of trusting docs, with a verification protocol

## How we tested it

**Evidence:** REVIEW

Read the full SKILL.md content for 4 representative skills (spec-driven-development, incremental-implementation, doubt-driven-development, context-engineering) via the GitHub API. Examined the plugin.json, hooks.json, session-start hook, commands directory, agents directory, and references directory. Cross-referenced with the existing evaluation in evaluations/skills-collections.md which covers the collection at a higher level.

```bash
gh api repos/addyosmani/agent-skills/contents/skills --jq '.[].name'
gh api repos/addyosmani/agent-skills/contents/skills/spec-driven-development/SKILL.md --jq '.content' | base64 -d
gh api repos/addyosmani/agent-skills/contents/skills/doubt-driven-development/SKILL.md --jq '.content' | base64 -d
gh api repos/addyosmani/agent-skills/contents/hooks/hooks.json --jq '.content' | base64 -d
```

## What worked

- **Skill quality is genuinely high.** spec-driven-development has a concrete 4-phase gated workflow with explicit assumption surfacing. doubt-driven-development has a rigorous 5-step claim/extract/doubt/reconcile/stop cycle with degraded-mode guidance for subagent contexts.
- **Full lifecycle coverage in 7 commands.** The mapping from development phases to slash commands is intuitive and complete. Each command activates 2-4 relevant skills, so the user doesn't need to know which skills exist.
- **`/build auto` is a real productivity tool.** Autonomous implementation with per-task TDD verification, individual commits, and pause-on-failure creates a practical "approve plan, come back later" workflow.
- **Shared reference documents.** 5 checklists (accessibility, performance, security, testing patterns, orchestration) that multiple skills can reference avoids duplication and keeps each skill focused.
- **Cross-editor support.** Plugin for Claude Code, documented setup for Cursor, Gemini CLI, Antigravity, Windsurf, Codex, and OpenCode.

## What didn't work or surprised us

- **More prescriptive than mattpocock/skills.** The 7-command lifecycle is opinionated — using just 2-3 commands feels incomplete, and the auto-activation can surprise users who don't want spec-driven-development triggered on every feature.
- **No domain modeling vocabulary.** Unlike mattpocock's `codebase-design` and `domain-modeling`, there's no CONTEXT.md or ubiquitous language concept. Architecture decisions flow through ADRs (via documentation-and-adrs) but there's no shared vocabulary mechanism.
- **No alignment/grilling skills.** mattpocock has `grill-me` and `grill-with-docs` for stress-testing plans. agent-skills has `interview-me` but it's lighter — no systematic decision-tree exhaustion.
- **SessionStart hook requires jq.** The meta-skill injection fails silently without jq installed, which can confuse users who install the plugin and see no effect.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Gated workflows prevent advancing without verification; doubt-driven catches non-obvious errors mid-flight |
| Speed | + | `/build auto` enables autonomous multi-task implementation; lifecycle commands reduce decision overhead |
| Maintainability | + | Documentation-and-adrs skill (already ADOPT) enforces ADR discipline; code-simplification removes complexity |
| Safety | + | Security-auditor agent + security checklist reference + security-and-hardening skill cover multiple angles |
| Cost Efficiency | neutral | No token optimization features; skills are moderate-sized (~200-400 lines each) |

## Verdict

**ADOPT**

The highest-quality full-lifecycle skill collection in the catalog. 24 skills with genuinely deep content (not checklists), 7 intuitive slash commands, `/build auto` for autonomous implementation, and cross-editor support. The doubt-driven-development and source-driven-development skills are unique innovations not found in competing collections. Choose this over mattpocock/skills when you want a structured lifecycle pipeline rather than à la carte engineering conventions; use both together for maximum coverage (agent-skills provides the lifecycle, mattpocock provides the vocabulary and grilling).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-skills](https://github.com/addyosmani/agent-skills) | skill | Production-grade engineering skills for AI coding agents — full lifecycle with gated workflows | Need battle-tested skills from a senior engineer's perspective | mattpocock/skills, everything-claude-code |
