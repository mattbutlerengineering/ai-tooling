# Skills Collections

Evaluation of curated skill sets for AI coding agents. All aim to make agents more effective by providing structured workflows, quality gates, and engineering best practices.

## Evaluation Criteria

- **Skill quality** — are skills well-written, specific, and actionable?
- **Engineering philosophy** — does it enforce good practices or just add features?
- **Composability** — can you pick individual skills, or is it all-or-nothing?
- **Scope discipline** — focused on what matters, or kitchen-sink?
- **Active maintenance** — is it still being developed?
- **Agent compatibility** — Claude Code only, or multi-agent?

## Tool Comparisons

### mattpocock/skills

**Stars:** 136,418 | **Last updated:** 2026-06-18 | **Latest release:** v1.0.1 (2026-06-17) | **License:** MIT

**What it actually does:** A small, composable set of engineering skills built from daily use by a senior TypeScript developer. Reached a tagged **v1** and is now a proper installable Claude Code plugin (`.claude-plugin/plugin.json` registers 17 skills). Key skills: `/grill-me` and `/grill-with-docs` (alignment before coding), `/triage` (issue workflow), `/prototype` (throwaway prototypes), `/implement` (end-to-end implementation flow), `/ask-matt` (router that points you at the right skill). v1 adds shared design skills — `codebase-design` (deep-module vocabulary) and `domain-modeling` — that other skills now build on, plus `resolving-merge-conflicts` and `writing-great-skills`; it removed `caveman` and `zoom-out`, renamed `diagnose` → `diagnosing-bugs`, and split the taxonomy into user-invoked vs model-invoked skills. Domain modeling uses `CONTEXT.md` to build shared vocabulary between human and agent. Installable via `npx skills@latest add mattpocock/skills`.

**Strengths:**
- Philosophy-driven: "small, easy to adapt, and composable" — explicitly rejects monolithic approaches
- `/grill-me` and `/grill-with-docs` are the standout skills — solve the #1 agent failure mode (misalignment)
- `CONTEXT.md` approach creates a shared language, reducing AI verbosity dramatically
- Domain-driven design influence — the only skills collection that addresses the communication problem
- Most popular skills repo (136k stars) — massively validated by the community
- Each skill is independent — pick what you need, skip the rest
- Active maintenance with newsletter updates
- Multi-agent: works with any model, explicitly designed for portability
- Practical focus: "skills for real engineers, not vibe coding"

**Weaknesses:**
- TypeScript-centric author — skills are language-agnostic but examples lean TypeScript
- Fewer skills than competitors — deliberate choice, but means gaps in some areas
- Setup requires `/setup-matt-pocock-skills` which adds configuration overhead
- No built-in security or testing methodology — relies on external tools for those

---

### addyosmani/agent-skills

**Stars:** 60,339 | **Last updated:** 2026-06-16 | **License:** MIT

**What it actually does:** 7 slash commands mapping to the full development lifecycle: `/spec` (define), `/plan` (plan), `/build` (implement), `/test` (verify), `/review` (QA), `/code-simplify` (simplify), `/ship` (deploy). Skills activate automatically based on context — designing an API triggers `api-and-interface-design`, building UI triggers `frontend-ui-engineering`. Includes `/build auto` for autonomous implementation after plan approval. Available as Claude Code plugin and Cursor rules.

**Strengths:**
- Full lifecycle coverage: spec → plan → build → test → review → ship
- Lifecycle mapping is intuitive — 7 commands cover the entire dev process
- `/build auto` enables autonomous implementation with per-task verification
- Auto-activation: skills trigger based on what you're doing, not manual invocation
- Strong engineering pedigree (Addy Osmani, Google Chrome team)
- Plugin-based install for Claude Code, copy-paste for Cursor
- Good balance: more structured than mattpocock, less monolithic than ECC
- Active maintenance (updated today)

**Weaknesses:**
- More prescriptive than mattpocock — the lifecycle is opinionated and may conflict with existing workflows
- Auto-activation can be surprising — skills fire when you don't expect them
- No domain modeling / shared vocabulary approach (no CONTEXT.md equivalent)
- Doesn't address the alignment problem (no grilling/interview skills)
- Less composable: the 7 commands form a pipeline, using just 2-3 feels incomplete

---

### everything-claude-code / ECC (affaan-m/ECC)

**Stars:** 216,191 | **Last updated:** 2026-06-15 | **License:** MIT

**What it actually does:** Massive plugin: 63 agents, 251 skills, 79 legacy command shims, hooks, rules, MCP conventions, and operator workflows. Covers every conceivable domain: architecture, testing, 40+ language/framework patterns, healthcare compliance, finance, networking, marketing, security, and more. Originally "everything-claude-code," now branded as ECC (v2.0.0-rc.1). Won an Anthropic hackathon.

**Strengths:**
- Sheer breadth: if a domain-specific skill exists, ECC probably has it
- Most starred repo in the AI coding space (216k stars)
- 63 specialized agents cover architecture, debugging, database review, security, etc.
- Framework-specific patterns (React, Django, FastAPI, Spring Boot, Laravel, etc.)
- Actively maintained with frequent updates
- Anthropic hackathon winner — external validation

**Weaknesses:**
- Kitchen-sink approach: 251 skills creates context bloat and potential conflicts
- Many skills are shallow — broad coverage but thin depth per skill
- Conflicts with other plugins: 79 command shims can shadow other tools' commands
- No clear philosophy beyond "more is better" — contrast with mattpocock's "composable and small"
- Installing ECC alongside superpowers, mattpocock/skills, or agent-skills creates massive overlap
- Hard to know which skills are actually good vs. filler
- v2.0.0-rc.1 rebrand suggests instability — naming went from everything-claude-code → ECC
- The 251 skills are ALWAYS loaded into context awareness — even skills you never use consume attention

## Verdict

**Recommended: mattpocock/skills**

**Why:** Best philosophy (composable, small, hackable), solves the most impactful problem (agent-human alignment via grilling), and introduces domain modeling via `CONTEXT.md` which no other collection offers. 136k stars and a tagged v1 (now a one-command plugin) validate the approach. The deliberate restraint — fewer skills, each one battle-tested — aligns with the insight that fewer tools with better feedback loops beats more tools with no infrastructure.

**Runner-up: addyosmani/agent-skills** — choose this if you want lifecycle-structured development (spec → plan → build → test → review → ship) with auto-activating skills. It's more prescriptive than mattpocock but less overwhelming than ECC. Good complement to mattpocock/skills since they solve different problems (lifecycle structure vs. alignment and domain modeling). These two can coexist.

**Not recommended: ECC / everything-claude-code** — despite being the most starred (216k), the kitchen-sink approach contradicts the principle that fewer tools with better feedback loops beats more tools. 251 skills creates context pollution, potential conflicts with other plugins, and makes it impossible to know which skills are actually driving value. The WORKFLOW.md recommendation to exclude this and use targeted skills instead is correct. If you need a specific domain skill (e.g., healthcare HIPAA compliance), extract that single skill rather than installing the entire plugin.

**Can mattpocock + agent-skills coexist?** Yes. mattpocock handles alignment and domain modeling (before coding). agent-skills handles the development lifecycle (during coding). They complement each other. The WORKFLOW.md could recommend both — mattpocock at L2 (it's already there) and agent-skills at L3 alongside superpowers.
