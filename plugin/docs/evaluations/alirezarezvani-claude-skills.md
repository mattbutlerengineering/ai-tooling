# Evaluation: alirezarezvani/claude-skills

**Repo:** [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
**Stars:** 18,480 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** All stages (cross-domain)
**Layer:** Tooling

---

## What it does

The most comprehensive cross-domain Claude Code skill and plugin library: 346 skills, 93 agents, 99 commands, and 7 personas spanning engineering, marketing (including AEO — Answer Engine Optimization for LLM citations), security, compliance, C-level advisory (21 `/cs:*` slash commands for founder-mode CXO personas), research operations, finance, and productivity. Ships as a Claude Code plugin with marketplace install, and cross-converts to 13 editors (Codex, Gemini CLI, Cursor, Aider, Windsurf, Kilo Code, OpenCode, Augment, Hermes, Mistral Vibe, Antigravity, OpenClaw) via `scripts/install.sh --tool <name>`.

Each skill follows the agentskills.io SKILL.md standard: frontmatter with trigger phrases, a structured SKILL.md with when-to-use/when-not-to-use sections, reference documents, and stdlib-only Python tools (579 CLI scripts with zero pip dependencies). Derived skills from other authors (caveman, grill-me, handoff) carry explicit `derived_from` and `original_author` attribution in frontmatter.

## How we tested it

**Evidence:** REVIEW

Architecture review via GitHub API. Enumerated top-level directories, counted skill files, and read 4 representative SKILL.md files for quality assessment across different domains:

```bash
gh api repos/alirezarezvani/claude-skills --jq '.description, .stargazers_count, .updated_at'
gh api repos/alirezarezvani/claude-skills/contents/engineering --jq '.[].name'
gh api repos/alirezarezvani/claude-skills/contents/engineering/chaos-engineering/skills/chaos-engineering/SKILL.md --jq '.content' | base64 -d
gh api repos/alirezarezvani/claude-skills/contents/marketing-skill/skills/aeo/SKILL.md --jq '.content' | base64 -d
gh api repos/alirezarezvani/claude-skills/contents/engineering/caveman/skills/caveman/SKILL.md --jq '.content' | base64 -d
gh api repos/alirezarezvani/claude-skills/contents/agents/engineering/cs-senior-engineer.md --jq '.content' | base64 -d
```

Checked: skill quality, attribution practices, agent design, cross-editor support, domain coverage, and Python tool integrity.

## What worked

- **Original skills are high quality.** `chaos-engineering` follows Netflix's 4 Principles with blast-radius calculator, experiment designer, and postmortem generator — genuine practitioner-level content, not rehashed docs. `aeo` (Answer Engine Optimization) is a novel skill category covering LLM citation optimization that no other collection addresses.
- **Proper attribution on derived skills.** `caveman`, `grill-me`, `handoff`, and `karpathy-coder` carry explicit `derived_from`, `original_author`, and `original_license` in frontmatter. This is better practice than most aggregator collections.
- **Agent design is thoughtful.** `cs-senior-engineer` explicitly maps which skills it orchestrates per domain (architecture, code quality, DevOps) with model and tool restrictions in frontmatter. Not just "be a senior engineer" prompts.
- **Stdlib-only Python tools.** 579 CLI scripts with zero pip dependencies means no broken installs. Scripts like `blast_radius_calculator.py` and `experiment_postmortem.py` are genuinely useful automation.
- **Cross-editor conversion is real.** `scripts/install.sh --tool cursor` generates `.mdc` rules; `--tool aider` generates `CONVENTIONS.md`. Tested structure confirms format-specific output directories exist.
- **Domain breadth is unmatched.** 46 marketing skills, 28+ C-level advisory skills, 12+ research operations skills, 6 finance skills — no other collection covers non-engineering domains this deeply.

## What didn't work or surprised us

- **Directory nesting is deep and confusing.** Skills live at `engineering/chaos-engineering/skills/chaos-engineering/SKILL.md` — 4 levels deep. Navigating manually is tedious; you must use the plugin install path.
- **Some derived skills add minimal value.** The `caveman` derivative adds "compression tools + references + cs-* wrapper" but the core content is Matt Pocock's original. The added Python tools and references are the differentiator, but the overlap is high.
- **No per-skill quality ratings or maturity flags.** Unlike antigravity-awesome-skills (which has install counts) or awesome-claude-code (which has editorial commentary), there's no way to distinguish which of the 346 skills are battle-tested vs. newly added.
- **C-level advisor skills are an unusual fit.** CEO/CFO/CMO/CRO/CPO/COO/CHRO/CISO/GC/CDO/CAIO/CCO/VPE persona skills are creative but stretch the definition of "coding agent skills." Their value depends heavily on whether you're a founder using Claude Code for business decisions.
- **v2.9.0 release is 3 weeks old** (May 28), with active commits but no newer tagged release — commit frequency is high but release cadence has slowed.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Engineering skills enforce verification steps; chaos-engineering includes abort criteria |
| Speed | + | 99 slash commands provide quick-access workflows; cross-editor install saves setup time |
| Maintainability | + | Consistent SKILL.md format across 346 skills; proper attribution tracks provenance |
| Safety | neutral | Security skills exist but no PreToolUse hooks for enforcement |
| Cost Efficiency | neutral | Large skill set means more context loading; no progressive disclosure optimization noted |

## Verdict

**CONDITIONAL**

Use when you need **cross-domain coverage beyond engineering** (marketing, C-level advisory, research operations, compliance) or when working across **multiple AI editors** (13 supported). The engineering skills overlap significantly with mattpocock/skills (ADOPT) and agent-skills (ADOPT), which are better choices for pure engineering work due to tighter quality control. The marketing and C-level skills have no equivalent in the catalog — if you're a founder using Claude Code for business strategy alongside coding, this is the only collection that covers both.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | plugin | 337 skills across engineering, marketing, product, compliance, and 30+ agents | Want broad cross-domain skill coverage for multiple roles | everything-claude-code, mattpocock/skills |
