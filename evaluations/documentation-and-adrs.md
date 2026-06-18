# Evaluation: documentation-and-adrs (addyosmani/agent-skills)

**Repo:** [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
**Stars:** 60,339 | **Last updated:** 2026-06-16 | **License:** MIT
**Dev loop stage:** Implement (inline docs, ADRs during feature work), Reflect (changelogs, retrospective docs)
**Layer:** Process

---

## What it does

A documentation philosophy skill that codifies *when* and *what* to document: inline comments, ADRs (Architecture Decision Records), READMEs, API docs, changelogs, and agent-specific context files (CLAUDE.md, spec files). The core thesis is "document decisions, not code" — the skill provides an ADR template, lifecycle model (PROPOSED → ACCEPTED → SUPERSEDED), commentary guidelines, README structure, and a verification checklist. It's a ruleset and template library, not a generation workflow.

## How we tested it

Applied against this repo's actual documentation situation. The repo has CLAUDE.md (agent context), WORKFLOW.md (architecture rationale), CATALOG.md (structured inventory), and `evaluations/` (decision records by a different name). Tested how well the skill maps to real work:

1. Would an ADR have helped when the repo switched from ACMM levels to inner/outer loop vocabulary? Yes — ADR-001 "Use inner/outer loop vocabulary instead of ACMM maturity levels" would have documented the decision, context, and alternatives considered. Currently that context lives in observation 14310 in OMEGA, not in the repo.

2. Checked the ADR template against the needs of this repo: the template is complete (Status, Date, Context, Decision, Alternatives Considered, Consequences) and would slot directly into a `docs/decisions/` folder.

3. Verified the "documentation for agents" section against what this repo does: CLAUDE.md for conventions, spec files for behavior, inline gotchas to prevent known traps. The skill formalizes what this repo does informally.

```
# This skill surfaces as behavioral guidance, not a command.
# It activates automatically when agent-skills is installed and you're
# in contexts matching: architectural decisions, API changes, feature shipping.
```

The verification checklist at the end is the most practically useful part — it's a pre-commit gate for documentation completeness that agents can mechanically execute.

## What worked

- The ADR template is the clearest, most complete one available as a skill. The lifecycle model (PROPOSED → ACCEPTED → SUPERSEDED) handles the "don't delete old ADRs" problem explicitly.
- "Document the *why*, not the *what*" is the right philosophy and stated plainly enough for an agent to internalize.
- The "documentation for agents" section is the only documentation skill that addresses CLAUDE.md and spec files directly — it treats agent-context files as first-class documentation artifacts.
- The verification checklist (ADRs for architectural decisions, README covers quick start, API functions documented, etc.) is mechanically executable by an agent before commit.
- Common rationalizations table ("the code is self-documenting" → "code shows what, not why") is useful for explaining to agents why skipping docs is wrong.
- Part of `addyosmani/agent-skills`, which is already installed and evaluated positively in this repo (see skills-collections.md).

## What didn't work or surprised us

- This is a philosophy/guidelines skill, not a generation workflow. It tells the agent *when* to document and *what shape* the output should take, but doesn't generate docs itself. You need `documentation-writer` or `documentation` for actual writing.
- The ADR template is TypeScript/web-stack biased (PostgreSQL, Prisma, REST vs. GraphQL examples). For a documentation-only repo like ai-tooling, the examples feel slightly foreign.
- No trigger conditions in the skill definition — it's behavioral guidance, not an invocable command. The agent must internalize it as always-on context, which means it competes with other always-on context.
- Changelog maintenance section is underspecified — it describes the format but says nothing about when to update or how to automate it.
- No handling of documentation for agent skills themselves (how do you document a skill collection like this one?).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | ADR template captures decision context that prevents re-litigating past decisions; "document the why" reduces future misinterpretation |
| Speed | neutral | Adds documentation work upfront; saves debugging time later when intent is unclear |
| Maintainability | ++ | ADRs directly address the highest-value documentation gap in codebases — *why* decisions were made | 
| Safety | neutral | No direct security benefit; "no commented-out code" rule has mild safety value |
| Cost Efficiency | + | ADRs prevent agents from re-deciding the same questions across sessions (expensive) |

## Verdict

**ADOPT**

This skill ships with `addyosmani/agent-skills`, which is already installed. The ADR template alone is worth having — this repo currently has no formal decision records, and any non-trivial architectural change (like the ACMM-to-inner/outer-loop reframe) deserves one. The "documentation for agents" section directly addresses how CLAUDE.md, rules files, and spec files should be maintained. Use alongside `documentation-writer` for actual generation: this skill governs *what* to document, `documentation-writer` governs *how* to write it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [documentation-and-adrs](https://github.com/addyosmani/agent-skills) | skill | ADR templates, inline comment philosophy, and agent-context documentation guidelines | Code shows what was built but not why; ADRs capture decision rationale for future engineers and agents | documentation-writer, documentation (anthropics/knowledge-work-plugins) |
