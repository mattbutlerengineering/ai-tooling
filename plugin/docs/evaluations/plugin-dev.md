# Evaluation: plugin-dev

**Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev)
**Stars:** 30,444 (monorepo) | **Last updated:** 2025-12-18 (plugin author: Daisy Hollman, daisy@anthropic.com) | **License:** MIT (per plugin README); monorepo is Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (meta: building the tools you implement *with*)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Plugin development framework with agent, command, and hook support." plugin-dev is the first-party Anthropic meta-toolkit for *authoring* Claude Code plugins — a plugin whose entire job is to help you build other plugins. It is v0.1.0 ("Initial release"), shipped inside the 30k-star `claude-plugins-official` marketplace monorepo.

It contributes three kinds of components:

- **7 skills** that auto-load on relevant prompts and front-load Claude with the Claude Code plugin authoring spec: `plugin-structure` (manifest, `${CLAUDE_PLUGIN_ROOT}`, auto-discovery), `command-development` (slash-command frontmatter, arguments, bash context), `agent-development` (agent frontmatter, `<example>` triggering blocks, system-prompt design), `skill-development` (progressive disclosure, trigger phrasing — explicitly "based on skill-creator methodology"), `hook-development` (all hook events, JSON schemas, security), `mcp-integration` (stdio/SSE/HTTP server config, auth), and `plugin-settings` (`.local.md` config files). Each skill is ~1,200-1,700 words of core SKILL.md plus `references/`, `examples/`, and in several cases `scripts/` (e.g. `validate-hook-schema.sh`, `test-hook.sh`, `hook-linter.sh`, `validate-agent.sh`, `parse-frontmatter.sh`).
- **3 agents**: `agent-creator` (Write/Read — generates a new agent file from a description, using Claude Code's own agent-creation prompt), `plugin-validator` (Read/Grep/Glob/Bash — checks `.claude-plugin/plugin.json` syntax, required `name` field, kebab-case naming, component file structure, anti-patterns), and `skill-reviewer` (Read/Grep/Glob — reviews skill description triggering quality and progressive disclosure).
- **1 guided command** `/plugin-dev:create-plugin` (415-line workflow) — an 8-phase end-to-end flow (Discovery → Component Planning → Detailed Design → Structure Creation → Component Implementation → Validation → Testing → Documentation) that asks clarifying questions per phase, auto-loads the relevant skills, calls `agent-creator` for AI-assisted generation, and runs the validation scripts.

Mechanically it is prompt scaffolding plus a handful of deterministic bash validators — there is no runtime/binary. Its value is encoding the (otherwise scattered, fast-moving) Claude Code plugin spec as triggerable context so you don't author plugins from memory.

## How we tested it

**Evidence:** REVIEW

Source review of the plugin **as checked out on this machine**. It is present at `~/.claude/plugins/repos/claude-plugins-official/plugins/plugin-dev/` (git remote → `anthropics/claude-plugins-official.git`), and its skills/agents are **active in this very session** — the environment's available-skills and available-agent-types lists include `plugin-dev:create-plugin`, `plugin-dev:plugin-structure`, `plugin-dev:skill-development`, etc., and the agents `plugin-dev:agent-creator`, `plugin-dev:plugin-validator`, `plugin-dev:skill-reviewer`. So this is the real shipped artifact, not a README paraphrase. I read the README, the `plugin-validator` agent, the create-plugin command size, and the skill inventory directly. I did **not** run `/plugin-dev:create-plugin` to scaffold a throwaway plugin in this session, nor execute the validator agent against a target — behavioral claims rest on reading the (transparent, short) component definitions.

```bash
gh api repos/anthropics/claude-plugins-official -q '{full_name,stars:.stargazers_count,desc:.description}'  # 30444 stars, official
find ~/.claude/plugins -ipath '*plugin-dev*'                  # plugin checked out locally
git -C ~/.claude/plugins/repos/claude-plugins-official remote -v   # -> anthropics/claude-plugins-official.git
git -C ~/.claude/plugins/repos/claude-plugins-official log -1 --format='%ci'   # 2025-12-18
# Read the actual files:
~/.claude/plugins/repos/claude-plugins-official/plugins/plugin-dev/README.md
~/.claude/plugins/repos/claude-plugins-official/plugins/plugin-dev/agents/plugin-validator.md
~/.claude/plugins/repos/claude-plugins-official/plugins/plugin-dev/commands/create-plugin.md   # 415 lines
~/.claude/plugins/repos/claude-plugins-official/plugins/plugin-dev/skills/*/SKILL.md           # 7 skills
```

Repo verification: confirmed. The catalog entry was UNLINKED; the plugin ships from `anthropics/claude-plugins-official` under `plugins/plugin-dev/`. (Marketplace install id is `plugin-dev@claude-code-marketplace` per the README; the repo itself is the verified source.)

## What worked

- **Impeccable provenance.** First-party Anthropic, MIT-licensed, inside the 30k-star official marketplace monorepo, authored by a named Anthropic engineer. For a meta-tool that *encodes the plugin spec*, having the spec come from the vendor that owns the spec is the strongest possible authority — third-party plugin-authoring guides go stale the moment Claude Code changes its manifest/hook format.
- **Genuinely comprehensive coverage of the full plugin surface.** Seven skills span every component type (commands, agents, skills, hooks, MCP, settings, structure) — this is the only catalog entry that covers *hooks* and *MCP server config* authoring, not just skills.
- **Deterministic validators, not just prose.** It ships real bash scripts (`validate-hook-schema.sh`, `validate-agent.sh`, `hook-linter.sh`, `test-hook.sh`) and a `plugin-validator` agent scoped to Read/Grep/Glob/Bash. That converts "did I get the manifest right?" from model guesswork into a checkable step — directly useful for this repo, which itself ships a `plugin/` marketplace package.
- **Progressive disclosure done right.** Lean SKILL.md (~1.2-1.7k words) + on-demand `references/`/`examples/` keeps context cost low until a relevant trigger fires; the skills only load when you're actually authoring.
- **Auto-triggering with strong phrase lists.** Each skill declares specific trigger phrases ("create a hook", "add MCP server", `${CLAUDE_PLUGIN_ROOT}`), so guidance appears exactly when you ask plugin-authoring questions — no manual invocation needed.

## What didn't work or surprised us

- **v0.1.0, "Initial release."** Self-described initial version; the plugin spec it documents is itself a moving target. The value depends entirely on Anthropic keeping it synced with Claude Code — a lag risk inherent to all spec-documenting tools.
- **Pure meta-niche.** Zero value to anyone not authoring Claude Code plugins. Most catalog consumers ship application code, not plugins — this is audience-gated in a way `commit-commands` or a review plugin is not.
- **Overlaps and is broader than skill-creator.** Its own `skill-development` skill says it is "based on skill-creator methodology." So for *skill* authoring specifically, the two cover the same ground; plugin-dev wins when you also need commands/agents/hooks/MCP, skill-creator wins if you only ever write standalone skills and want its eval/benchmark tooling (variance analysis), which plugin-dev does not have.
- **No enforcement beyond the validators.** The skills are prompt scaffolding; correctness of generated commands/agents still inherits model variance. The bash validators check structure, not behavior.
- **Did not execute the scaffolding workflow.** `/plugin-dev:create-plugin` is an 8-phase guided flow; I reviewed its definition but did not run it end-to-end, so claims about its interactive quality are from reading, not from a built artifact.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Encodes the authoritative plugin spec + ships `plugin-validator` and schema/agent validators that catch manifest/structure errors deterministically |
| Speed | + | `/create-plugin` + `agent-creator` scaffold a complete plugin from a description instead of hand-writing manifest, frontmatter, and component files from memory |
| Maintainability | + | Generated plugins follow consistent official conventions (`${CLAUDE_PLUGIN_ROOT}`, kebab-case, progressive disclosure), reducing per-plugin drift |
| Safety | + | hook-development skill is security-first (input validation, least privilege, HTTPS/WSS for MCP); validator scoped to read-only + Bash |
| Cost Efficiency | neutral | Progressive disclosure keeps idle context cost near zero; loads only on plugin-authoring triggers |

## Verdict

**CONDITIONAL (ADOPT for plugin authors; KEEP/installed already)**

For anyone authoring Claude Code plugins, skills, agents, hooks, or MCP integrations, this is the default tool — adopt it. It is the only first-party, comprehensive, auto-triggering authoring toolkit, it ships deterministic validators, and its provenance means it tracks the spec it documents better than any third-party alternative. This repo specifically maintains a `plugin/` marketplace package, so plugin-dev is directly applicable here for validating that package's structure and authoring new components.

It is CONDITIONAL rather than blanket-ADOPT only because the value is fully audience-gated: it does nothing for consumers who never author plugins, and it is v0.1.0 with a spec-lag risk. Versus **skill-creator**: keep both in the catalog and treat them as complementary, not duplicate — plugin-dev is the broader meta-toolkit (commands/agents/hooks/MCP + a guided scaffolder + validators), while skill-creator is the focused choice for standalone skill authoring with eval/benchmark/variance tooling that plugin-dev lacks. Reach for plugin-dev when building a multi-component plugin; reach for skill-creator when you only need one skill and want to measure its trigger accuracy. It is already installed/active in this environment, so the practical recommendation is KEEP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [plugin-dev](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev) | plugin | Official Anthropic meta-toolkit for authoring Claude Code plugins — 7 skills, 3 agents (agent-creator, plugin-validator, skill-reviewer), `/create-plugin` workflow | Building Claude Code plugins (commands/agents/skills/hooks/MCP) without hand-writing manifests and frontmatter from memory | skill-creator (complementary: plugin-dev = broad multi-component scaffolder + validators; skill-creator = focused skill authoring + evals) |
