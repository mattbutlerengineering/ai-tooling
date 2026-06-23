# Evaluation: documentation-writer (github/awesome-copilot)

**Repo:** [github/awesome-copilot](https://github.com/github/awesome-copilot)
**Stars:** 35,544 | **Last updated:** 2026-06-23 | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Implement (documentation as deliverable), Reflect (updating docs after changes)
**Layer:** Process

---

## What it does

A Diátaxis-framework documentation expert that structures all documentation output into one of four quadrants: Tutorials (learning-oriented), How-to Guides (problem-oriented), Reference (information-oriented), and Explanation (understanding-oriented). When invoked, it follows a three-step workflow: first clarifies document type, audience, goal, and scope; then proposes an outline for approval; then generates the full document in Markdown. It explicitly refuses to consult external sources unless you provide links.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured** on 2026-06-22 (macOS arm64, git/gh/Python available). The skill is a prose ruleset, so — per the skill-eval guidance in `TEMPLATE.md` (issue #38) — we evaluated it the way `skill-creator` does: by *verifying the real source*, *applying* it to a real ai-tooling subject, and mechanically scoring the artifact against the skill's own mandated structure (a repeatable conformance check that discriminates conforming output from a non-conforming control), rather than paraphrasing the README.

**1. Verified the real skill source (not the README paraphrase).** The skill is installed locally at `~/.claude/skills/documentation-writer` → symlinked to `~/.agents/skills/documentation-writer/SKILL.md` (a single file, **2,748 bytes / 45 lines**). It is byte-identical to upstream: `gh api repos/github/awesome-copilot/contents/skills/documentation-writer/SKILL.md --jq '.size'` returns **2748** and `diff` against the decoded upstream content reports IDENTICAL (upstream sha `93e3fbf`). The SKILL.md frontmatter is `name: documentation-writer` with the trigger `description: 'Diátaxis Documentation Expert. An expert technical writer specializing in creating high-quality software documentation, guided by the principles and structure of the Diátaxis technical documentation authoring framework.'` — so its *triggering* surface is documentation-authoring prompts.

   Every component the catalog claims **actually exists in the file**, at these real headings:
   - `## YOUR TASK: The Four Document Types` enumerates all four Diátaxis quadrants with their orientation and a one-word metaphor: **Tutorials** ("A lesson"), **How-to Guides** ("A recipe"), **Reference** ("A dictionary"), **Explanation** ("A discussion").
   - `## WORKFLOW` mandates the three-step process: **(1) Acknowledge & Clarify** — "You MUST determine the following before proceeding: Document Type, Target Audience, User's Goal, Scope"; **(2) Propose a Structure** — "propose a detailed outline … Await my approval before writing"; **(3) Generate Content** — "write the full documentation in well-formatted Markdown."
   - `## CONTEXTUAL AWARENESS` contains the no-external-sources rule verbatim: "You may not consult external websites or other sources unless I provide a link and instruct you to do so," plus "DO NOT copy content from them unless I explicitly ask you to."
   - `## GUIDING PRINCIPLES` (Clarity, Accuracy, User-Centricity, Consistency).

**2. Applied the skill to a real ai-tooling subject and scored conformance.** Picking a concrete Reference subject from this repo — *the four `**Evidence:**` field values (`MEASURED` / `RUN` / `REVIEW` / `SOURCE-ONLY`)* — we followed the skill's workflow: resolved the four clarify-step facts (Document Type = Reference, Audience = contributors auditing evals, Goal = look up each value's meaning/constraints, Scope = the four values only, excluding how to run audits), then generated `docs/evidence-field-reference.md` (2,932 bytes, information-oriented: a lookup table plus one descriptive section per value). Written into a temp dir (`mktemp -d`, **not** this repo's tree).

   We then ran a **repeatable Python conformance check** (`check_diataxis.py`) scoring the doc against the skill's three actual mandates: (1) the four workflow clarify-facts resolved, (2) commits to exactly ONE declared quadrant, (3) follows that quadrant's shape (Reference = descriptive lookup structure) with **no cross-quadrant bleed** — no Tutorial smells ("let's get started", "Step N:", "congratulations") and no Explanation smells ("deeper philosophy", "epistemology"). Result:

   **CONFORMANCE: 5/5 mandated checks pass — exit 0.**

   To prove the check discriminates rather than rubber-stamping, a **control** run on a deliberately mixed-quadrant doc (same subject, but blending a Tutorial "Let's get started / Step 5: celebrate" narrative and an Explanation "deeper philosophy / epistemology" discussion into a doc claiming to be Reference, and omitting the workflow metadata) scored **0/5 — exit 1**: the checker flagged the unresolved workflow facts, the absent quadrant declaration, the broken Reference shape, and both quadrant bleeds.

```bash
# 1. Verify real source == upstream
wc -c ~/.agents/skills/documentation-writer/SKILL.md   # 2748
gh api repos/github/awesome-copilot/contents/skills/documentation-writer/SKILL.md --jq '.size'  # 2748
gh api repos/github/awesome-copilot/contents/skills/documentation-writer/SKILL.md --jq '.content' \
  | base64 -d | diff - ~/.agents/skills/documentation-writer/SKILL.md   # IDENTICAL (sha 93e3fbf)

# 2. Apply the skill's Reference quadrant + workflow to an ai-tooling subject (temp dir), then check:
TMP=$(mktemp -d)
#   ...resolved Document Type/Audience/Goal/Scope, then generated docs/evidence-field-reference.md...
python3 check_diataxis.py "$TMP/docs/evidence-field-reference.md"
#   → CONFORMANCE: 5/5 mandated checks pass (exit 0)
python3 check_diataxis.py "$TMP/docs/evidence-field-mixed.md"
#   → CONFORMANCE: 0/5 (exit 1) — control with mixed quadrants + missing workflow facts
```

The quadrant discipline plus the mandatory clarify step is exactly what the conformance check exercises: a doc that doesn't commit to one quadrant, or skips the Document-Type/Audience/Goal/Scope resolution, fails mechanically.

## What worked

- **Source matches upstream exactly and the claimed components are all real.** The four Diátaxis quadrants, the three-step `## WORKFLOW` (clarify → propose outline → generate), and the no-external-sources rule are present at concrete headings — verified by byte-identical `diff` against the live upstream file (sha `93e3fbf`), not the README.
- **The skill's structure is genuinely followable and produces a conforming artifact.** Applying its Reference quadrant + workflow to a real ai-tooling subject (the Evidence field values) yielded a doc that passed a 5/5 conformance check on the first pass — the quadrant shape and the four clarify facts are unambiguous enough to follow mechanically.
- The Diátaxis quadrant framing immediately resolves the most common docs failure: writing a tutorial that's actually a reference, or an explanation that's actually a how-to. The control doc that violated this scored 0/5, confirming the framework's discipline is checkable, not aspirational.
- The three-step gate (clarify → outline → approve → generate) is process-enforcing in a way that bare skill files typically are not. The "MUST determine Document Type / Audience / Goal / Scope before proceeding" line is an explicit precondition the conformance check can assert.
- Constraint against consulting external sources is appropriate for docs work — keeps the model grounded in project reality rather than pulling in external patterns that don't fit. Part of `github/awesome-copilot` (35.5K stars, MIT, actively pushed 2026-06-23).

## What didn't work or surprised us

- The skill only covers writing documentation from scratch or from provided context — it has no mechanism for detecting documentation drift (existing docs that no longer match the codebase). Maintenance is out of scope. (This is where `documentation-and-adrs` complements it.)
- The clarification-first workflow adds a round trip before any output, which slows down quick documentation tasks. For a simple README update this feels like overhead.
- No structured output format: the skill mandates a *quadrant* and a Markdown deliverable but enforces no section schema or front matter conventions. Two Reference docs from this skill could still diverge in their internal heading layout — our conformance check had to define "Reference shape" itself rather than read it from the skill.
- The "DO NOT copy content" constraint on context files is overly cautious for cases where you legitimately want to adapt existing content (e.g., updating a WORKFLOW.md section).
- Purely a writing skill — no integration with any code analysis. It can't generate API reference docs by reading function signatures.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Clarification gate (Document Type/Audience/Goal/Scope) catches wrong-shaped docs before generation; the applied Reference doc passed a 5/5 quadrant-conformance check while a mixed-quadrant control scored 0/5, so the discipline is mechanically verifiable. |
| Speed | neutral | Three-step workflow adds round trips; saves time on rewrites from wrong-shaped output. |
| Maintainability | + | Diátaxis discipline produces docs that commit to a single purpose and are easier to update; verified the Reference quadrant yields a clean lookup-shaped artifact. |
| Safety | neutral | No security surface; "no external sources" constraint is a mild safety benefit. |
| Cost Efficiency | neutral | Three round trips cost more tokens upfront but prevent expensive rewrites. |

## Verdict

**ADOPT**

Verified hands-on: the skill source is byte-identical to upstream (`github/awesome-copilot`, sha `93e3fbf`, 2,748 bytes), every claimed component (the four Diátaxis quadrants, the clarify → outline → generate workflow with its four mandated clarify facts, the no-external-sources rule) actually exists in the 45-line SKILL.md, and applying its Reference quadrant + workflow to a real ai-tooling subject (the Evidence field values) produced a doc that passed a 5/5 repeatable conformance check (a mixed-quadrant control scored 0/5, so the check discriminates). The Diátaxis quadrant framing is the clearest thinking available for documentation structure, and this skill operationalizes it without ceremony. Skip it for trivial one-liner doc updates; invoke it for any documentation that will outlast the session. Use alongside `documentation-and-adrs`, which governs *what/when* to document while this skill governs *how* to shape it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [documentation-writer](https://github.com/github/awesome-copilot) | skill | Diátaxis-framework documentation expert: clarify, outline, then generate purpose-specific docs | Agent produces documentation that mixes tutorial steps with reference material, serving no audience well | documentation (anthropics/knowledge-work-plugins), documentation-and-adrs |
