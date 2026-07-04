# Evaluation: documentation (anthropics/knowledge-work-plugins)

**Repo:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
**Stars:** N/A (official Anthropic plugin) | **Last updated:** 2026 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (README, API docs, runbooks), Reflect (architecture docs, onboarding guides)
**Layer:** Process

---

## What it does

A minimal, principles-first documentation skill from Anthropic's official knowledge-work-plugins collection. Covers five document types (README, API docs, Runbook, Architecture Doc, Onboarding Guide) with structure templates for each, and five writing principles (write for the reader, most useful information first, show don't tell, keep it current, link don't duplicate). The skill is notably lightweight — 50 lines total. Its trigger description is the most explicit of the four candidates: "write docs for", "document this", "create a README", "write a runbook".

## How we tested it

**Evidence:** REVIEW

Applied to three documentation tasks relevant to this repo:

1. **README update** — the skill's README template covers the right sections (what it is, quick start, commands, architecture overview). Applied to this repo's README.md structure, it aligns well. No gaps.

2. **Runbook** — tested mentally against a hypothetical "how to add a catalog entry" runbook. The template (when to use, prerequisites, step-by-step, rollback, escalation) is operational-focused. For this documentation-only repo, the runbook template is slightly heavy — there's no rollback or escalation for adding a markdown row.

3. **Architecture doc** — the template (context/goals, high-level design, key decisions/trade-offs, data flow) maps directly to what WORKFLOW.md already does, validating the template's utility.

```
# Trigger phrases (from skill description):
# "write docs for X"
# "document this"
# "create a README"
# "write a runbook"
# "onboarding guide"
```

The skill's brevity is both its strength and its limitation. There's no workflow gate, no approval step, no clarification round trip. It goes straight to generation based on document type. For a quick README, this is ideal. For complex architecture documentation, the lack of a clarification step risks producing something plausible but wrong-shaped.

## What worked

- Trigger description is the most explicit and specific of the four candidates — clear activation conditions prevent ambiguity about when to use it.
- Five document types cover the practical range of documentation work without overspecifying. The runbook template in particular is the only one among the four candidates that addresses operational documentation.
- "Link, don't duplicate" principle is underrated — agents often copy-paste content between docs, creating drift. This principle directly addresses that failure mode.
- "Keep it current" principle treats documentation maintenance as a first-class concern, not an afterthought.
- Lightweight footprint: 50 lines means minimal context cost and no framework overhead. This is a skill you can leave always-on.
- Official Anthropic provenance: this reflects how Anthropic thinks agents should handle documentation, which is directly relevant for Claude Code users.

## What didn't work or surprised us

- No ADR support — decision records are entirely absent from this skill's vocabulary. For any codebase making significant architectural choices, ADRs are the highest-value documentation type, and this skill misses them entirely.
- No workflow gate: the skill goes directly to generation without clarification or outline approval. For complex documentation this risks confident wrong output.
- The principles are correct but underdeveloped — "write for the reader" is stated but not operationalized with any questions to ask, personas to consider, or failure examples to avoid.
- No Diátaxis awareness: the skill doesn't distinguish between tutorial, how-to, reference, and explanation. This leads to the most common documentation failure (mixing document types).
- At 50 lines, this skill is essentially a brief memo. It lacks the depth needed to produce consistently high-quality output across diverse documentation tasks.
- 5,500 installs is notably lower than `documentation-writer` (20,900) despite Anthropic provenance — the community has voted for more structured approaches.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Principles are sound but no clarification gate; output shape depends on how well the agent interprets the request |
| Speed | + | No round trips — quickest path to documentation output of the four candidates |
| Maintainability | neutral | "Keep it current" and "link don't duplicate" principles help, but no structural enforcement |
| Safety | neutral | No security surface; low risk skill |
| Cost Efficiency | + | Minimal token footprint; no multi-step workflow overhead |

## Verdict

**CONDITIONAL**

Use when you need fast, low-ceremony documentation for well-understood document types (READMEs, runbooks, onboarding guides). Skip for ADRs (use `documentation-and-adrs` instead) and skip for complex documentation requiring Diátaxis discipline (use `documentation-writer`). This skill fills the gap for quick operational documentation where a three-step workflow would be overkill. Worth keeping installed for its lightweight trigger coverage; not worth relying on as the primary documentation skill.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [documentation (anthropics)](https://github.com/anthropics/knowledge-work-plugins) | skill | Lightweight documentation skill covering READMEs, API docs, runbooks, and onboarding guides | Agent needs quick, low-ceremony documentation generation without multi-step workflow overhead | documentation-writer, documentation-and-adrs |
