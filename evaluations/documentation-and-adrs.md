# Evaluation: documentation-and-adrs (addyosmani/agent-skills)

**Repo:** [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
**Stars:** 65,447 | **Last updated:** 2026-06-22 | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Implement (inline docs, ADRs during feature work), Reflect (changelogs, retrospective docs)
**Layer:** Process

---

## What it does

A documentation philosophy skill that codifies *when* and *what* to document: inline comments, ADRs (Architecture Decision Records), READMEs, API docs, changelogs, and agent-specific context files (CLAUDE.md, spec files). The core thesis is "document decisions, not code" — the skill provides an ADR template, lifecycle model (PROPOSED → ACCEPTED → SUPERSEDED), commentary guidelines, README structure, and a verification checklist. It's a ruleset and template library, not a generation workflow.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured** on 2026-06-22 (macOS arm64, Node/git/gh available). The skill is a prose ruleset, so — per the skill-eval guidance in `TEMPLATE.md` (issue #38) — we evaluated it the way `skill-creator` does: by *applying* it to a real decision and mechanically lint-scoring the artifact against the skill's own mandated structure (a repeatable structural conformance check), rather than paraphrasing the README.

**1. Verified the real skill source (not the README paraphrase).** The skill is installed locally at `~/.claude/skills/documentation-and-adrs` → `~/.agents/skills/documentation-and-adrs/SKILL.md` (a single file, **8,734 bytes / 279 lines**). We confirmed it is byte-identical to upstream: `gh api repos/addyosmani/agent-skills/contents/skills/documentation-and-adrs/SKILL.md --jq '.size'` returns **8734** (sha `061c5e1…`). The SKILL.md frontmatter is `name: documentation-and-adrs` with the trigger `description: Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase.` — so its *triggering* surface is architectural-decision / API-change / feature-ship prompts.

   Every component the catalog claims **actually exists in the file**, at these real headings:
   - `## Architecture Decision Records (ADRs)` → `### When to Write an ADR`, `### ADR Template` (stored in `docs/decisions/`, sequential numbering), `### ADR Lifecycle`.
   - The ADR template's real mandated fields: `## Status` (`Accepted | Superseded by ADR-XXX | Deprecated`), `## Date`, `## Context`, `## Decision`, `## Alternatives Considered` (each alternative as a `###` with **Pros / Cons / Rejected**), `## Consequences`.
   - The lifecycle line is literally `PROPOSED → ACCEPTED → (SUPERSEDED or DEPRECATED)` with the rule "Don't delete old ADRs."
   - `## Inline Documentation` (When to / not to comment, "Document Known Gotchas"), `## API Documentation`, `## README Structure`, `## Changelog Maintenance`, `## Documentation for Agents` (CLAUDE.md / spec files / ADRs / inline gotchas), `## Common Rationalizations` (table), `## Red Flags`, and a final `## Verification` checklist (7 items).

**2. Applied the skill to a real decision from this repo and lint-scored conformance.** Picking an actual architectural decision in ai-tooling — *"derive STACK.md from verdict data + an exclusion ledger instead of hand-maintaining it"* (the #64/#70 drift-gate work) — we wrote an ADR following the skill's exact template into a temp dir (`mktemp -d`, **not** this repo's tree): `docs/decisions/ADR-001-stack-derived-from-verdicts.md` (2,353 bytes, three alternatives each with Pros/Cons/Rejected).

   We then ran a **repeatable Python structural lint** of that ADR against the 13 fields/rules the skill mandates (title `ADR-NNN:`, `## Status` with a valid lifecycle value, ISO `## Date`, `## Context`, `## Decision`, `## Alternatives Considered`, `## Consequences`, ≥2 alternatives, a `Rejected:` rationale per alternative, Pros/Cons present, no stray TODO/commented-out code). Result:

   **CONFORMANCE: 13/13 mandated structural checks pass — assertion passed (lint exit 0).**

   To prove the lint discriminates rather than rubber-stamping, a **control** run on a deliberately deficient ADR (no Status / Alternatives / Consequences) scored **4/7** — the checker correctly flagged the missing mandated sections.

```bash
# 1. Verify real source == upstream
wc -c ~/.agents/skills/documentation-and-adrs/SKILL.md          # 8734
gh api repos/addyosmani/agent-skills/contents/skills/documentation-and-adrs/SKILL.md --jq '.size'  # 8734

# 2. Apply skill template to a real ai-tooling decision (temp dir), then lint:
TMP=$(mktemp -d); mkdir -p "$TMP/docs/decisions"
#   ...wrote ADR-001 following the skill's Status/Date/Context/Decision/
#   Alternatives(Pros/Cons/Rejected)/Consequences template...
python3 lint_adr.py "$TMP/docs/decisions/ADR-001-...md"
#   → CONFORMANCE: 13/13 mandated structural checks pass — assertion passed (exit 0)
#   control on a deficient ADR → 4/7 (checker discriminates)
```

The `## Verification` checklist at the end is the most practically useful part — it's a pre-commit gate for documentation completeness that an agent (or a lint like the one above) can mechanically execute.

## What worked

- **Source matches upstream exactly and the claimed components are all real.** The ADR template, the `PROPOSED → ACCEPTED → (SUPERSEDED or DEPRECATED)` lifecycle, inline-comment guidelines, README structure, and the 7-item `## Verification` checklist are present at concrete headings — verified against the live file, not the README.
- **The template is genuinely fillable and produces a conforming artifact.** Applying it to a real ai-tooling decision yielded an ADR that passed a 13/13 structural lint on the first pass — the field set (Status / Date / Context / Decision / Alternatives-with-Pros-Cons-Rejected / Consequences) is complete and unambiguous enough to follow mechanically.
- The lifecycle model handles the "don't delete old ADRs" problem explicitly (supersede, don't delete).
- "Document the *why*, not the *what*" is stated plainly enough for an agent to internalize, and the `## Documentation for Agents` section is the only documentation skill here that treats CLAUDE.md and spec files as first-class artifacts.
- The `## Common Rationalizations` table ("the code is self-documenting" → "code shows what, not why") gives an agent ready counter-arguments for skipping docs.
- Part of `addyosmani/agent-skills` (65.4K stars, MIT, active — pushed 2026-06-22), already installed and evaluated positively in this repo (see skills-collections.md).

## What didn't work or surprised us

- This is a philosophy/guidelines + template skill, not a generation workflow. It tells the agent *when* to document and *what shape* the output takes, but doesn't generate docs itself. Pair it with `documentation-writer` for actual writing.
- The ADR template's worked example is TypeScript/web-stack biased (PostgreSQL, Prisma, REST vs. GraphQL). The *structure* transferred cleanly to a documentation-only repo's decision, but the example prose feels foreign for non-web stacks.
- The trigger `description` fires on "architectural decisions / public APIs / shipping features" — good coverage, but as always-on behavioral guidance it has no invocable command, so it competes with other always-on context rather than being explicitly summoned.
- Changelog-maintenance section is underspecified — it shows the Keep-a-Changelog format but says nothing about *when* to update or how to automate it.
- No guidance on documenting agent skills themselves (how you'd document a skill collection like this one).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | ADR template captures decision context that prevents re-litigating past decisions; the applied ADR-001 passed a 13/13 structural conformance lint, confirming the template is complete and followable. |
| Speed | neutral | Adds documentation work upfront; saves debugging/re-deciding time later when intent is unclear. |
| Maintainability | ++ | ADRs directly address the highest-value documentation gap — *why* decisions were made; verified the template slots into `docs/decisions/` and produces a conforming record. |
| Safety | neutral | No direct security benefit; the "no commented-out code" red flag has mild safety value. |
| Cost Efficiency | + | ADRs prevent agents from re-deciding the same questions across sessions (the skill's own "Documentation for Agents" rationale, borne out by applying it to this repo's STACK-derivation decision). |

## Verdict

**ADOPT**

Verified hands-on: the skill source is byte-identical to upstream, every claimed component (ADR template, lifecycle, inline/README/API guidelines, verification checklist) actually exists in the 279-line SKILL.md, and applying its template to a real ai-tooling architectural decision produced an ADR that passed a 13/13 repeatable structural conformance lint (a deficient control scored 4/7, so the check discriminates). The ADR template alone is worth having — this repo still has no formal `docs/decisions/`, and any non-trivial architectural change (the STACK-derivation drift gate, the Evidence-as-derived-field choice) deserves one. The "Documentation for Agents" section directly addresses how CLAUDE.md, rules files, and spec files should be maintained. Use alongside `documentation-writer` for actual generation: this skill governs *what* to document, `documentation-writer` governs *how* to write it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [documentation-and-adrs](https://github.com/addyosmani/agent-skills) | skill | ADR templates, inline comment philosophy, and agent-context documentation guidelines | Code shows what was built but not why; ADRs capture decision rationale for future engineers and agents | documentation-writer, documentation (anthropics/knowledge-work-plugins) |
