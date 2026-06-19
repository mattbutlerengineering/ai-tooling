# Evaluation: agent-rules-books

**Repo:** [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books)
**Stars:** 1,902 | **Last updated:** 2026-05-22 | **License:** MIT
**Dev loop stage:** Plan, Implement
**Layer:** Process

---

## What it does

Thirteen classic software-engineering books (Clean Code, Refactoring, DDD/IDDD/DDD Distilled, Clean Architecture, A Philosophy of Software Design, Code Complete, DDIA, PoEAA, Release It!, The Pragmatic Programmer, Working Effectively with Legacy Code, plus Refactoring.Guru) distilled into tool-agnostic Markdown rule sets you drop into an agent's context as `AGENTS.md` / `CLAUDE.md` rules or load as on-demand skills. The mechanism is pure context injection: each rule set is a list of concrete, imperative engineering rules ("counted with the deterministic release convention") that prime the agent to apply that book's principles during planning, implementation, and refactoring.

The distinguishing feature is **tiered token budgets**. Every book ships in three versions: `nano` (~17-26 rules, ~1.2-2.8 KB — compact fallback for tight context), `mini` (~28-47 rules, ~3.8-8 KB — the recommended default), and `full` (~158-523 rules, ~11-62 KB — canonical reference). This lets you pay only the context cost you can afford per task. USAGE.md documents always-on vs on-demand patterns, scoped rules, and editor-specific setup for Codex, Cursor, and Claude Code; COMPATIBILITY.md covers combining multiple books.

## How we tested it

Method: repository and documentation inspection via the GitHub API. I did **not** install the rule sets or run an agent task against them. Findings below come from the repo metadata, the full README (release matrix, validation experiment, copyright note), and cross-reference against the catalog's calibration evals (andrej-karpathy-skills, domain-modeling). No metrics here are mine — the validation numbers are the author's own self-reported experiment, flagged as such.

```bash
gh api repos/ciembor/agent-rules-books --jq '{stars,license,description,pushed_at}'
gh api repos/ciembor/agent-rules-books/readme --jq '.content' | base64 -d
```

## What worked

- **Tiered token budgets are the genuinely novel contribution.** nano/mini/full lets you tune context spend per task — a feature absent from karpathy-skills (monolithic ~60 lines) and most rule-dump repos. The README explicitly recommends `mini` for real use and `nano` for tight budgets.
- **Concrete imperative rules, not book naming.** The author's own experiment is the strongest signal: a refactor using `mini` rules scored ~74/100 vs ~46/100 for a branch that merely instructed "OBEY A Philosophy of Software Design." This is exactly the catalog's thesis — listing the principles beats invoking the title, because it forces the latent knowledge into active context.
- **Broad, well-chosen canon.** Covers planning/architecture (Clean Arch, PoEAA, DDIA), implementation (Clean Code, Code Complete, Pragmatic Programmer), and refactoring/legacy (Refactoring, Refactoring.Guru, WEWLC) — the inner-loop stages where these tools intervene.
- **Clean copyright posture.** README is explicit: rules are *inspired by* the books, are not official materials, "intentionally avoid reproducing book text," and are "not a substitute for reading the books." Distilled imperatives rather than copied prose — a defensible derivative stance, MIT licensed.
- **Tool-agnostic and actively maintained.** v0.5, plain Markdown, works in Codex/Cursor/Claude Code; pushed within the last month; low open-issue count.

## What didn't work or surprised us

- **The model already knows these books.** Opus/Sonnet have deep latent knowledge of Clean Code, DDD, Refactoring, etc. The rule sets do not teach new content; they raise the *activation* of principles the model already holds. Value is real but bounded — it is priming, not new knowledge.
- **Author's own validation is honest about its limits.** A secondary Reek code-smell check showed almost no difference (1083 vs 1077 smells); the gain was visible only in architectural judgment, and the author calls it "an early qualitative signal, not a benchmark." No equivalent experiments for the other 12 books.
- **Token cost adds up if used naively.** Loading several `full` rule sets always-on (DDD full is 42 KB, Refactoring.Guru 62 KB) would consume serious context. The tiering mitigates this only if the user disciplines themselves to `nano`/`mini` and loads on demand rather than always-on.
- **Risk of conflicting/over-prescriptive rules.** Combining DDD + Clean Architecture + PoEAA can push an agent toward ceremony (aggregates, repositories, unit-of-work) on tasks that don't need it — directly counter to the catalog's Simplicity-First / karpathy discipline. COMPATIBILITY.md exists precisely because of this tension.
- **Overlaps the user's existing setup.** The user already runs `coding-style.md`, `implementation-discipline.md`, and the domain-modeling skill. Layering full book rule sets on top risks redundancy and rule conflict rather than additive value.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Author's experiment: mini-rules refactor scored 74 vs 46 for naming the book alone; concrete rules activate principles the model applies. |
| Speed | neutral/- | Pure context priming, no automation; DDD/architecture rules can bias toward more ceremony and larger refactors. |
| Maintainability | + | Distilled canon (Clean Code, Refactoring, A Philosophy of Software Design) targets readability, module depth, and responsibility boundaries — the catalog's core maintainability signal. |
| Safety | neutral | No security-specific content (Release It! touches reliability/resilience, not security). |
| Cost Efficiency | neutral/- | nano/mini tiers explicitly control token spend, but always-on `full` sets are expensive; net depends entirely on usage discipline. |

## Verdict

**CONDITIONAL**

Adopt selectively, never wholesale. The tiered token-budget design is a real innovation and the author's own A/B experiment supports the catalog thesis that concrete rules beat naming a book. But the model already holds this knowledge, so the rule sets are priming rather than teaching, and loading many `full` sets always-on burns context and risks over-prescriptive, conflicting guidance against the user's existing Simplicity-First discipline. Recommended pattern: pick one or two `mini` sets matched to the task at hand (e.g., the Refactoring or A Philosophy of Software Design `mini` during a cleanup, a DDD `mini` when modeling a domain) and load them on demand, not as standing rules. Overlaps mattpocock/skills and andrej-karpathy-skills (both CONDITIONAL) on the behavioral-rules axis, and the domain-modeling skill on the DDD axis; this repo's edge is breadth of canon plus the nano/mini/full budgeting that the others lack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-rules-books](https://github.com/ciembor/agent-rules-books) | skill | 13 classic engineering books distilled into CLAUDE.md rule sets with tiered token budgets | Want canonical software engineering principles (DDD, Clean Architecture, DDIA) as agent rules | mattpocock/skills, andrej-karpathy-skills |
