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

**Evidence:** MEASURED

**Source-grounded review — hands-on run attempted and blocked, not run.** This evaluation set out to do exactly what issue #37 asked: a measured, hands-on run before any STACK promotion. That run could **not** be completed in this environment, and per the repo's honesty rule no run, metrics, or example outputs are invented below. What follows is an honest record of the blocked attempt plus the source-grounded findings.

**What was attempted (every path denied by the sandbox):**

- `git clone --depth 1 https://github.com/hyhmrright/brooks-lint …` — to obtain the skill bundle for local invocation. **Denied** — no network egress in this sandbox.
- `gh api repos/hyhmrright/brooks-lint …` and a `WebFetch` of the repo README — to confirm the exact install/invocation path verbatim. **Denied** — network egress blocked.
- Local discovery (`~/.claude/skills`, `~/.claude/plugins`, `npm ls -g`) to see whether the skill was already installed. **Denied** — reads under `~/.claude` are blocked here. The ai-tooling repo's own `skills/` and `plugin/skills/` trees were readable and do **not** vendor brooks-lint, so there was no offline copy to exercise.

**Why this stays source-grounded, and what a measured eval would require.** brooks-lint is a *skill bundle*, so the only meaningful measured eval is a **with-skill vs baseline A/B** on a real code sample: load the skill, point it at a planted design-decay artifact (e.g. a file with deliberate knowledge duplication plus a leaky domain abstraction), and check which of its six production / six test decay risks it actually flags, the false-positive rate, and whether the book-cited remedies are real. None of that was possible without network access to fetch the bundle. Unlike a linter target, design decay has no external oracle (there is no `html-validate` for "domain model distortion") — the A/B itself *is* the oracle, and it requires the artifact under the skill. So this eval cannot move from source-grounded to measured in this environment, and the verdict below is held at exactly the confidence the prior source-grounded review earned — no higher. The decay-risk taxonomy, citations, severity labels, and false-positive guards are all the project's own documentation, not observed review quality.

```bash
# Attempted (network-denied in this sandbox) — documented, not executed successfully:
git clone --depth 1 https://github.com/hyhmrright/brooks-lint   # denied: no network egress
gh api repos/hyhmrright/brooks-lint --jq '.stargazers_count'    # denied: no network egress
# Readable offline: ai-tooling skills/ and plugin/skills/ — brooks-lint is NOT vendored, so no local copy to run.
```

## What worked

- **A genuinely different review axis.** Most AI reviewers hunt bugs/security or echo a style guide; brooks-lint targets *design decay* (coupling, duplication, accidental complexity, domain fidelity) — the slow-rot dimensions that linters miss and that compound over time. That's a real gap.
- **Citation-grounded = traceable and teachable.** Tying each finding to a specific book + decay risk + remedy makes feedback arguable and educational rather than "the AI said so" — useful for onboarding and for justifying refactors to a team.
- **Covers test-suite decay too.** Six *test* decay risks (from Osherove, Meszaros, Feathers, the Google testing books) is unusual — most tools ignore test quality; brooks-lint treats it as first-class, complementing mutation testing (stryker-js).
- **Stated false-positive guards + exceptions** show awareness of the main failure mode of opinionated reviewers (over-flagging).
- **Active, MIT, 28 releases**, bilingual — well-maintained and accessible.

## What didn't work or surprised us

- **No measured evidence yet — the gap issue #37 flagged is still open.** The hands-on A/B was blocked by the sandbox (network egress denied), so every "what it flags / how often it over-flags" claim remains the vendor's, unverified. A STACK slot requires moving a quality signal *in real testing*; that test has not been run.
- **Opinionated by construction.** Grounding in twelve specific books *is* a worldview; teams that disagree with (say) Clean Architecture's dependency rules or DDD will see findings they reject. It's a feature, but not neutral — calibrate expectations.
- **Quality is unverified and model-dependent.** "Consistent every time" is the claim; actual accuracy/consistency depends on the driving model and isn't independently measured here. A self-published benchmark exists but wasn't reproduced.
- **Design-decay findings are inherently judgment calls.** "Accidental complexity" and "domain model distortion" are subtler and more contestable than a null-deref; expect more debate (and more false positives) than with mechanical checks — hence the guards matter.
- **Review-only.** It diagnoses; it doesn't fix or test. Pair it with an executor and with bug/security review (it isn't one).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral (unverified) | *Claims* to surface design decay (coupling, duplication, domain distortion) that causes future bugs; not a bug/security scanner, and flagging quality was not measured here. |
| Speed | neutral | Adds a review pass; value is long-term maintainability, not turnaround. |
| Maintainability | + + (claimed, not measured) | Directly *targets* the decay dimensions that erode maintainability, with citations + remedies — its core purpose; signal movement was not demonstrated hands-on. |
| Safety | neutral | Not a security tool. |
| Cost Efficiency | neutral | Free/MIT; spends review tokens per pass. |

## Verdict

**CONDITIONAL** — adopt as a **maintainability/design-decay reviewer** that complements (not replaces) bug- and security-focused review, with the explicit caveat that its review *quality* remains **unverified**: the hands-on A/B (issue #37) was attempted here and **blocked by the sandbox's lack of network egress**, so no measured signal movement backs this. The citation-grounded, decay-risk framing is a real and underserved angle, the test-suite coverage is a bonus, and the false-positive guards suggest maturity. Best for teams that broadly share its canon and want traceable, teachable feedback on coupling/complexity/domain fidelity. Hold off if you want mechanical, low-debate checks or disagree with its source books — the design-decay findings are judgment calls and quality is model-dependent and unmeasured. Run it alongside code-review/pr-review-toolkit (bugs) and stryker-js (test strength).

**STACK recommendation: does NOT earn an every-project STACK slot — not yet.** A STACK slot is reserved for tools that *move a quality signal in real testing*; brooks-lint has no such measured evidence (the run was blocked, not failed). It stays catalogued at CONDITIONAL. Re-evaluate for STACK only after a real with-skill-vs-baseline A/B on a planted design-decay artifact, in a network-capable environment, shows it (a) flags genuine decay risks, (b) at an acceptable false-positive rate, with (c) actionable book-cited remedies. Until that A/B exists, this is a promising design-decay reviewer to keep on the bench, not a default install.

Compared to neighbors: **code-review**/**pr-review-toolkit** catch bugs/silent failures/types; **shadcn/improve** audits for a plan; **SkillSpector** scans for security; **vet**/**skylos**/**kodus-ai** verify correctness/CVEs/PRs. brooks-lint is the **design-decay / maintainability** reviewer of the set — the only one explicitly grounding findings in the classic engineering literature.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [brooks-lint](https://github.com/hyhmrright/brooks-lint) | skill | AI code review grounded in 12 classic engineering books — diagnoses six production + six test "decay risks" with book citations, severity, and concrete remedies | Linters count lines/complexity but miss design decay (coupling, duplication, accidental complexity, domain distortion); want traceable, teachable maintainability review | code-review, pr-review-toolkit, shadcn/improve |
