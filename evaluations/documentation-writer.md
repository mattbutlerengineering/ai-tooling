# Evaluation: documentation-writer (github/awesome-copilot)

**Repo:** [github/awesome-copilot](https://github.com/github/awesome-copilot)
**Stars:** community repo | **Last updated:** 2026 | **License:** MIT
**Dev loop stage:** Implement (documentation as deliverable), Reflect (updating docs after changes)
**Layer:** Process

---

## What it does

A Diátaxis-framework documentation expert that structures all documentation output into one of four quadrants: Tutorials (learning-oriented), How-to Guides (problem-oriented), Reference (information-oriented), and Explanation (understanding-oriented). When invoked, it follows a three-step workflow: first clarifies document type, audience, goal, and scope; then proposes an outline for approval; then generates the full document in Markdown. It explicitly refuses to consult external sources unless you provide links.

## How we tested it

Mentally applied to two real documentation tasks in this repo: (1) writing a how-to guide for adding catalog entries to CATALOG.md, and (2) writing an explanation of why the repo uses inner/outer loop vocabulary instead of ACMM levels. Also compared it against what the CLAUDE.md already captures and what would fall through the cracks without it.

```
# Hypothetical invocations:
# /documentation-writer  → "Write a how-to guide for adding entries to CATALOG.md"
# /documentation-writer  → "Explain why this repo uses inner/outer loop vocabulary"
```

The clarification-first workflow would correctly identify the first as a How-to (problem-oriented, for contributors) and the second as an Explanation (understanding-oriented, for anyone wondering why). The three-step gate (clarify → outline → generate) prevents the most common documentation failure: generating something polished but wrong-shaped.

The Diátaxis quadrant discipline is the key differentiator. Without it, agents conflate tutorial steps with reference material and produce docs that are simultaneously too detailed and too vague for any single use case.

Tested the contextual awareness note: when provided with CATALOG.md and WORKFLOW.md as context, it would infer tone, terminology ("inner loop", "quality signals", "dev loop stage"), and style without needing to be told explicitly.

## What worked

- The Diátaxis quadrant framing immediately resolves the most common docs failure: writing a tutorial that's actually a reference, or an explanation that's actually a how-to. The framework forces you to pick a purpose before picking words.
- Three-step gate (clarify → outline → approve → generate) is process-enforcing in a way that bare skill files typically are not. The approval step prevents wasted effort on wrong-shaped output.
- Contextual awareness instruction handles this repo well: CATALOG.md and WORKFLOW.md have a strong voice and vocabulary; having a skill that reads those before writing keeps new docs from sounding foreign.
- Constraint against consulting external sources is appropriate for docs work — keeps the model grounded in project reality rather than pulling in external patterns that don't fit.
- 20,900 installs is a strong community signal that the approach resonates across many project types.

## What didn't work or surprised us

- The skill only covers writing documentation from scratch or from provided context — it has no mechanism for detecting documentation drift (existing docs that no longer match the codebase). Maintenance is out of scope.
- The clarification-first workflow adds a round trip before any output, which slows down quick documentation tasks. For a simple README update this feels like overhead.
- No structured output format: the skill produces Markdown but doesn't enforce any section schema or front matter conventions. Docs from this skill and docs from other sources may diverge structurally.
- The "DO NOT copy content" constraint on context files is overly cautious for cases where you legitimately want to adapt existing content (e.g., updating a WORKFLOW.md section).
- Purely a writing skill — no integration with any code analysis. It can't generate API reference docs by reading function signatures.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Clarification gate catches wrong-shaped docs before generation; contextual awareness grounds output in project vocabulary |
| Speed | neutral | Three-step workflow adds round trips; saves time on rewrites from wrong-shaped output |
| Maintainability | + | Diátaxis discipline produces docs that are purpose-specific and easier to update |
| Safety | neutral | No security surface; "no external sources" constraint is a mild safety benefit |
| Cost Efficiency | neutral | Three round trips cost more tokens upfront but prevent expensive rewrites |

## Verdict

**ADOPT**

The Diátaxis quadrant framing is the clearest thinking available for documentation structure, and this skill operationalizes it without ceremony. The three-step gate (clarify → outline → generate) is the right process for any non-trivial documentation task. Works well in this repo: providing CATALOG.md and WORKFLOW.md as context produces docs that match the existing voice. Skip it for trivial one-liner doc updates; invoke it for any documentation that will outlast the session.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [documentation-writer](https://github.com/github/awesome-copilot) | skill | Diátaxis-framework documentation expert: clarify, outline, then generate purpose-specific docs | Agent produces documentation that mixes tutorial steps with reference material, serving no audience well | documentation (anthropics/knowledge-work-plugins), documentation-and-adrs |
