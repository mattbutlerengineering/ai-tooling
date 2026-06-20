# Evaluation: brooks-lint

**Repo:** [hyhmrright/brooks-lint](https://github.com/hyhmrright/brooks-lint)
**Stars:** 1,118 | **Last updated:** 2026-06-18 (pushed; active) | **License:** MIT | **Releases:** 28
**Dev loop stage:** Review (code-quality diagnosis of changes/codebase)
**Layer:** Process/Tooling (a skill bundle — JavaScript, installable skills)

---

## What it does

brooks-lint is **AI code review grounded in twelve classic software-engineering books.** Where most quality tools count lines and cyclomatic complexity, brooks-lint diagnoses code against **six production-code "decay risks"** and **six test-suite decay risks** synthesized from canonical sources — *The Mythical Man-Month*, *Code Complete*, *Refactoring*, *Clean Architecture*, *The Pragmatic Programmer*, *Domain-Driven Design*, *A Philosophy of Software Design*, *Software Engineering at Google*, *The Art of Unit Testing*, *How Google Tests Software*, *Working Effectively with Legacy Code*, and *xUnit Test Patterns*.

The six production decay risks: **Cognitive Overload** (mental effort to understand), **Change Propagation** (how many unrelated things break on one change), **Knowledge Duplication** (same decision in multiple places), **Accidental Complexity** (more complex than the problem), **Dependency Disorder** (do dependencies flow consistently), and **Domain Model Distortion** (does code faithfully represent the domain). Each finding is "consistent, traceable, actionable" — it carries **book citations**, **severity labels**, and **concrete remedies**, every time, with a documented source-to-skill mapping (`skills/_shared/source-coverage.md`) including exceptions and false-positive guards. It ships as skills (with a website, a benchmark, and English/中文 docs).

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill installed, no codebase reviewed. Claims come from the repository (GitHub metadata, README's book/decay-risk tables, example output, 28 releases) — the project's own documentation, not observed review quality.

```bash
gh api repos/hyhmrright/brooks-lint --jq '{stars,pushed_at,license:.license.spdx_id}'
gh api repos/hyhmrright/brooks-lint/readme --jq '.content' | base64 -d   # twelve books, six decay risks, example
gh api repos/hyhmrright/brooks-lint/releases --jq 'length'              # 28
```

## What worked

- **A genuinely different review axis.** Most AI reviewers hunt bugs/security or echo a style guide; brooks-lint targets *design decay* (coupling, duplication, accidental complexity, domain fidelity) — the slow-rot dimensions that linters miss and that compound over time. That's a real gap.
- **Citation-grounded = traceable and teachable.** Tying each finding to a specific book + decay risk + remedy makes feedback arguable and educational rather than "the AI said so" — useful for onboarding and for justifying refactors to a team.
- **Covers test-suite decay too.** Six *test* decay risks (from Osherove, Meszaros, Feathers, the Google testing books) is unusual — most tools ignore test quality; brooks-lint treats it as first-class, complementing mutation testing (stryker-js).
- **Stated false-positive guards + exceptions** show awareness of the main failure mode of opinionated reviewers (over-flagging).
- **Active, MIT, 28 releases**, bilingual — well-maintained and accessible.

## What didn't work or surprised us

- **Opinionated by construction.** Grounding in twelve specific books *is* a worldview; teams that disagree with (say) Clean Architecture's dependency rules or DDD will see findings they reject. It's a feature, but not neutral — calibrate expectations.
- **Quality is unverified and model-dependent.** "Consistent every time" is the claim; actual accuracy/consistency depends on the driving model and isn't independently measured here. A self-published benchmark exists but wasn't reproduced.
- **Design-decay findings are inherently judgment calls.** "Accidental complexity" and "domain model distortion" are subtler and more contestable than a null-deref; expect more debate (and more false positives) than with mechanical checks — hence the guards matter.
- **Review-only.** It diagnoses; it doesn't fix or test. Pair it with an executor and with bug/security review (it isn't one).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Surfaces design decay (coupling, duplication, domain distortion) that causes future bugs; not a bug/security scanner itself. |
| Speed | neutral | Adds a review pass; value is long-term maintainability, not turnaround. |
| Maintainability | + + | Directly targets the decay dimensions that erode maintainability, with citations + remedies — its core purpose. |
| Safety | neutral | Not a security tool. |
| Cost Efficiency | neutral | Free/MIT; spends review tokens per pass. |

## Verdict

**CONDITIONAL** — adopt as a **maintainability/design-decay reviewer** that complements (not replaces) bug- and security-focused review. The citation-grounded, decay-risk framing is a real and underserved angle, the test-suite coverage is a bonus, and the false-positive guards suggest maturity. Best for teams that broadly share its canon and want traceable, teachable feedback on coupling/complexity/domain fidelity. Hold off if you want mechanical, low-debate checks or disagree with its source books — the design-decay findings are judgment calls and quality is model-dependent and unverified. Run it alongside code-review/pr-review-toolkit (bugs) and stryker-js (test strength).

Compared to neighbors: **code-review**/**pr-review-toolkit** catch bugs/silent failures/types; **shadcn/improve** audits for a plan; **SkillSpector** scans for security. brooks-lint is the **design-decay / maintainability** reviewer of the set — the only one explicitly grounding findings in the classic engineering literature.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [brooks-lint](https://github.com/hyhmrright/brooks-lint) | skill | AI code review grounded in 12 classic engineering books — diagnoses six production + six test "decay risks" with book citations, severity, and concrete remedies | Linters count lines/complexity but miss design decay (coupling, duplication, accidental complexity, domain distortion); want traceable, teachable maintainability review | code-review, pr-review-toolkit, shadcn/improve |
