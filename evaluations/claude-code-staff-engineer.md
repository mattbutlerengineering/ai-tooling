# Evaluation: claude-code-staff-engineer

**Repo:** [FareedKhan-dev/claude-code-staff-engineer](https://github.com/FareedKhan-dev/claude-code-staff-engineer)
**Stars:** 69 | **Last updated:** 2026-06-12 | **License:** MIT
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Presents a "Staff Engineer with Sub-Agent Teams" concept: a hierarchical agent system where a Staff Engineer orchestrates specialized sub-agents through Discovery & Design, Planning & Review, Execution Engine, and Quality Gates phases. The README is a detailed educational blog post (~113KB) explaining the organizational metaphor.

The implementation is 14 skills, 1 agent, 3 commands, and 1 hook. The skill files cover brainstorming, planning, delegation/sub-agent dispatch, execution, evidence-based verification, TDD discipline, forensic debugging, review requesting/reception, worktree management, release engineering, and a meta "skill academy" for creating new skills.

## How we tested it

Examined the full repo structure and diffed skill files against the installed superpowers plugin (v6.0.0, obra/superpowers from claude-plugins-official).

```bash
gh api "repos/FareedKhan-dev/claude-code-staff-engineer/git/trees/main?recursive=1" --jq '.tree[].path'
# Read each core skill file and compared against superpowers
diff <(gh api ".../evidence-verification_skill.md" | base64 -d) \
     <(cat ~/.claude/plugins/.../superpowers/6.0.0/skills/verification-before-completion/SKILL.md)
# Result: identical (zero diff)
```

Compared 4 skill files:
- `evidence-verification_skill.md` vs superpowers `verification-before-completion/SKILL.md` — **identical** (zero diff)
- `design-and-discovery_skill.md` vs superpowers `brainstorming/SKILL.md` — **near-identical** (1 line differs in visual companion timing)
- `orchestration_skill.md` vs superpowers `dispatching-parallel-agents/SKILL.md` — **identical frontmatter `name:` field**
- `delegation_skill.md` vs superpowers `subagent-driven-development/SKILL.md` — **identical frontmatter `name:` field**

## What worked

- The README is an excellent educational resource explaining *why* multi-agent hierarchies work, with clear organizational metaphors (team roster, employee handbook, management layer)
- Cross-platform hook support (Windows batch + Unix bash polyglot) is a thoughtful detail
- The directory structure maps cleanly to organizational roles, making it intuitive to navigate

## What didn't work or surprised us

- **The skills are superpowers** — the skill files are copies (some byte-identical) of obra/superpowers v6.0.0 with renamed directories. The `name:` frontmatter values match exactly (`brainstorming`, `verification-before-completion`, `subagent-driven-development`, `executing-plans`, `dispatching-parallel-agents`). This means installing this repo gives you superpowers under a different folder structure.
- 69 stars vs superpowers' established presence and ongoing maintenance — superpowers is the canonical source with the active maintainer.
- Last updated June 12 vs superpowers receiving continuous updates — this fork will drift.
- No attribution to superpowers in the README or LICENSE beyond MIT compliance.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Same skills as superpowers — identical quality |
| Speed | neutral | No speed advantage over installing superpowers directly |
| Maintainability | - | Fork will drift from upstream superpowers; no sync mechanism |
| Safety | neutral | Same verification gates as superpowers |
| Cost Efficiency | neutral | Same token footprint as superpowers |

## Verdict

**SKIP**

This is a repackaged copy of superpowers (ADOPT) with renamed directories and a blog-post README. The educational value of the README is real — it's a well-written explanation of multi-agent hierarchies — but as an installable tool it provides nothing that superpowers doesn't already provide with better maintenance and upstream support. Install superpowers instead; read this README for the conceptual framework if helpful.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-staff-engineer](https://github.com/FareedKhan-dev/claude-code-staff-engineer) | harness | Staff engineer with sub-agent teams in Claude Code | Want hierarchical agent teams with a lead engineer coordinating specialists | superpowers (identical skills), gstack, agency-agents |
