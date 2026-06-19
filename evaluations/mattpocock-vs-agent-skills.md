# mattpocock/skills vs agent-skills: Detailed Comparison

> **Re-reviewed 2026-06-19 against v1.0.1** (released 2026-06-17). Matt Pocock's skills hit a tagged v1 and are now an installable plugin — `.claude-plugin/plugin.json` registers 17 skills — installed via `npx skills@latest add mattpocock/skills` rather than copied out of a `.claude` directory. 136K stars (was 130K). Key churn since the prior review: `caveman` and `zoom-out` **removed**; `diagnose` **renamed** to `diagnosing-bugs`; `write-a-skill` **replaced** by `writing-great-skills`; new `ask-matt` (router), `codebase-design`, `domain-modeling`, `grilling` (model-invoked), and `resolving-merge-conflicts` skills added. v1 also renames the taxonomy from Commands/Skills to **user-invoked / model-invoked** (a user-invoked skill orchestrates and may call model-invoked skills, but never another user-invoked one). Verdict unchanged — **use both** — and the case for adopting mattpocock is stronger now that it's a one-command plugin.

## mattpocock/skills (~25 active skills)

**Philosophy:** Opinionated, senior-engineer-hard-won-opinions style. Each skill has a strong point of view about what "good" looks like. TDD skill leads with "tests should verify behavior through public interfaces, not implementation details." The `diagnosing-bugs` skill's Phase 1 is "build a feedback loop" with creative approaches and the line "spend disproportionate effort here."

**Skills by category (v1):**
- Engineering (14): ask-matt, codebase-design, diagnosing-bugs, domain-modeling, grill-with-docs, implement, improve-codebase-architecture, prototype, resolving-merge-conflicts, setup-matt-pocock-skills, tdd, to-issues, to-prd, triage
- Productivity (5): grill-me, grilling, handoff, teach, writing-great-skills
- Misc (4): git-guardrails-claude-code, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit
- Personal (2): edit-article, obsidian-vault
- (Also ships `in-progress/` and `deprecated/` folders not registered in the plugin manifest.)

**Unique strengths:** prototype, handoff, triage (issue state machine), diagnosing-bugs (creative feedback-loop-first strategies), teach, writing-great-skills, ask-matt (routes you to the right skill), and the new shared design vocabulary — `codebase-design` (deep modules: interface/depth/seam/adapter) and `domain-modeling` (CONTEXT.md glossary + ADRs) — that the other skills now build on.

## agent-skills (24 skills)

**Philosophy:** Structured and procedural. Step-by-step workflows, checklists, and decision trees. TDD skill has a clear RED-GREEN-REFACTOR cycle diagram with code examples. Planning skill has dependency graph visualization and vertical slicing strategies. Reads like a senior engineer's playbook — comprehensive, well-organized, but less opinionated.

**Skills:** api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, code-review-and-quality, code-simplification, context-engineering, debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs, doubt-driven-development, frontend-ui-engineering, git-workflow-and-versioning, idea-refine, incremental-implementation, interview-me, observability-and-instrumentation, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, source-driven-development, spec-driven-development, test-driven-development, using-agent-skills

**Unique strengths:** doubt-driven-development, incremental-implementation, source-driven-development, context-engineering, CI/CD automation, deprecation/migration, observability, security hardening, shipping/launch, browser testing

## Overlap (7 areas)

| Problem | mattpocock | agent-skills |
|---------|-----------|-------------|
| TDD | `tdd` (vertical slices, one test at a time) | `test-driven-development` (structured RED-GREEN-REFACTOR with code examples) |
| Debugging | `diagnosing-bugs` (creative, feedback-loop-first strategies) | `debugging-and-error-recovery` (procedural) |
| Planning | `to-issues`, `to-prd` | `planning-and-task-breakdown`, `spec-driven-development` |
| Code review | `review` (in-progress) | `code-review-and-quality` |
| Architecture | `improve-codebase-architecture`, `codebase-design`, `domain-modeling` | `api-and-interface-design` |
| Grilling/interviewing | `grill-me`, `grill-with-docs`, `grilling` | `interview-me`, `idea-refine` |
| Git workflow | `git-guardrails-claude-code` | `git-workflow-and-versioning` |
| Merge conflicts | `resolving-merge-conflicts` | — |

## Conflict risk

**None.** Different `name:` frontmatter, so they register as separate skills. The agent picks whichever matches the trigger better. Having two TDD perspectives is an asset — mattpocock's enforces vertical slices while agent-skills' provides structured code examples.

## Verdict

**Use both.** They're complementary, not redundant:
- **mattpocock/skills** gives the *philosophy* — strong opinions about what good engineering looks like, creative problem-solving (diagnosing-bugs), a shared design/domain vocabulary (codebase-design, domain-modeling), and practical productivity tools (handoff, prototype)
- **agent-skills** gives *lifecycle coverage* — incremental implementation, CI/CD automation, deprecation/migration, shipping/launch, observability, security hardening, doubt-driven development. These are entire workflow phases mattpocock doesn't cover.

## WORKFLOW.md placement

- **mattpocock/skills → L2** (foundational opinions from day one)
- **agent-skills → L3** (lifecycle structure when methodology enforcement begins)
