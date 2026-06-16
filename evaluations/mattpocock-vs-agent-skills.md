# mattpocock/skills vs agent-skills: Detailed Comparison

## mattpocock/skills (20 skills)

**Philosophy:** Opinionated, senior-engineer-hard-won-opinions style. Each skill has a strong point of view about what "good" looks like. TDD skill leads with "tests should verify behavior through public interfaces, not implementation details." Diagnose skill's Phase 1 is "build a feedback loop" with 10 creative approaches and the line "spend disproportionate effort here."

**Skills by category:**
- Engineering (10): diagnose, grill-with-docs, improve-codebase-architecture, prototype, tdd, to-issues, to-prd, triage, zoom-out, setup-matt-pocock-skills
- Productivity (6): caveman, grill-me, handoff, teach, write-a-skill
- Misc (4): git-guardrails, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit
- Personal (2): edit-article, obsidian-vault

**Unique strengths:** prototype, handoff, caveman (token reduction), triage (issue state machine), zoom-out, diagnose (10 creative feedback loop strategies), teach, write-a-skill

## agent-skills (24 skills)

**Philosophy:** Structured and procedural. Step-by-step workflows, checklists, and decision trees. TDD skill has a clear RED-GREEN-REFACTOR cycle diagram with code examples. Planning skill has dependency graph visualization and vertical slicing strategies. Reads like a senior engineer's playbook — comprehensive, well-organized, but less opinionated.

**Skills:** api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, code-review-and-quality, code-simplification, context-engineering, debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs, doubt-driven-development, frontend-ui-engineering, git-workflow-and-versioning, idea-refine, incremental-implementation, interview-me, observability-and-instrumentation, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, source-driven-development, spec-driven-development, test-driven-development, using-agent-skills

**Unique strengths:** doubt-driven-development, incremental-implementation, source-driven-development, context-engineering, CI/CD automation, deprecation/migration, observability, security hardening, shipping/launch, browser testing

## Overlap (7 areas)

| Problem | mattpocock | agent-skills |
|---------|-----------|-------------|
| TDD | `tdd` (vertical slices, one test at a time) | `test-driven-development` (structured RED-GREEN-REFACTOR with code examples) |
| Debugging | `diagnose` (creative, 10 feedback loop strategies) | `debugging-and-error-recovery` (procedural) |
| Planning | `to-issues`, `to-prd` | `planning-and-task-breakdown`, `spec-driven-development` |
| Code review | — | `code-review-and-quality` |
| Architecture | `improve-codebase-architecture` | — |
| Grilling/interviewing | `grill-me`, `grill-with-docs` | `interview-me`, `idea-refine` |
| Git workflow | `git-guardrails` | `git-workflow-and-versioning` |

## Conflict risk

**None.** Different `name:` frontmatter, so they register as separate skills. The agent picks whichever matches the trigger better. Having two TDD perspectives is an asset — mattpocock's enforces vertical slices while agent-skills' provides structured code examples.

## Verdict

**Use both.** They're complementary, not redundant:
- **mattpocock/skills** gives the *philosophy* — strong opinions about what good engineering looks like, creative problem-solving (diagnose), and practical productivity tools (caveman, handoff, prototype)
- **agent-skills** gives *lifecycle coverage* — incremental implementation, CI/CD automation, deprecation/migration, shipping/launch, observability, security hardening, doubt-driven development. These are entire workflow phases mattpocock doesn't cover.

## WORKFLOW.md placement

- **mattpocock/skills → L2** (foundational opinions from day one)
- **agent-skills → L3** (lifecycle structure when methodology enforcement begins)
