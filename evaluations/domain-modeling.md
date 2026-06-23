# Evaluation: domain-modeling

**Repo:** [mattpocock/skills](https://github.com/mattpocock/skills)
**Stars:** 136,514 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan (design; touches Reflect when ADRs are recorded after a decision)
**Layer:** Process

---

## What it does

Build CONTEXT.md glossaries and ADRs — pin down ubiquitous language as designs evolve. It is a Claude Code skill at `skills/engineering/domain-modeling/SKILL.md` inside Matt Pocock's "Skills for Real Engineers" marketplace, with two bundled reference files (`CONTEXT-FORMAT.md`, `ADR-FORMAT.md`). It triggers when the user wants to pin down domain terminology / a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.

The skill is explicit that it is the *active* discipline of changing the model, not the passive habit of reading it: "Merely reading `CONTEXT.md` for vocabulary is not this skill — that's a one-line habit any skill can do." The mechanism is two artifacts plus five in-session behaviours:

- **`CONTEXT.md`** — a project glossary of the ubiquitous language. The format is opinionated: for each term, a one-to-two-sentence definition of what it IS (not what it does), plus an `_Avoid_` line listing synonyms to reject (e.g. *Order* — `_Avoid_: Purchase, transaction`). Hard rule: it is a glossary and *nothing else* — "totally devoid of implementation details," not a spec or scratch pad. Only project-specific domain terms belong; general programming concepts (timeouts, error types) are explicitly excluded. Multi-context repos use a `CONTEXT-MAP.md` at the root that points to per-context `CONTEXT.md` files and records relationships between contexts (DDD-style bounded contexts).
- **`docs/adr/NNNN-slug.md`** — sequentially numbered Architecture Decision Records. The template is deliberately minimal: an ADR can be a single paragraph ("what's the context, what did we decide, why"); optional Status/Considered-Options/Consequences sections only when they add value. The decisive contribution is the **gate**: offer an ADR only when all three are true — (1) hard to reverse, (2) surprising without context, (3) the result of a real trade-off. If any is missing, skip it.
- **Five in-session behaviours:** challenge terms that conflict with the glossary; sharpen fuzzy/overloaded language ("account" → Customer or User?); stress-test relationships with invented edge-case scenarios; cross-reference claims against the actual code and surface contradictions; and update `CONTEXT.md` *inline* the moment a term resolves rather than batching.

Files are created lazily — no `CONTEXT.md` until the first term resolves, no `docs/adr/` until the first ADR is warranted.

## How we tested it

**Evidence:** REVIEW

Skill-mechanism review. Method: read the full `SKILL.md` and both bundled reference files (`CONTEXT-FORMAT.md`, `ADR-FORMAT.md`) pulled from the repo via the GitHub API; read the peer skill `codebase-design/SKILL.md` from the same repo; and mapped the surrounding mattpocock skill ecosystem (`grill-with-docs`, `improve-codebase-architecture`) and the catalog's overlap target (`documentation-and-adrs`). I did **not** run it end-to-end against a live design session on a throwaway repo — the artifact under test is a prompt-only process skill, so the thing being evaluated *is* the procedure and the two artifact formats, all of which are reproduced above. Note: this skill is already present in the running session's skill list as `domain-modeling` with the exact frontmatter shown, because the user has `mattpocock/skills` cloned locally — so the practical question is "does it earn shelf space," not "should I install it."

```bash
gh api repos/mattpocock/skills --jq '{stars,license:.license.spdx_id,description}'
gh api "repos/mattpocock/skills/git/trees/main?recursive=1" --jq '.tree[] | select(.path | test("domain|context|adr|codebase-design";"i")) | .path'
gh api repos/mattpocock/skills/contents/skills/engineering/domain-modeling/SKILL.md --jq '.content' | base64 -d
gh api repos/mattpocock/skills/contents/skills/engineering/domain-modeling/CONTEXT-FORMAT.md --jq '.content' | base64 -d
gh api repos/mattpocock/skills/contents/skills/engineering/domain-modeling/ADR-FORMAT.md --jq '.content' | base64 -d
gh api repos/mattpocock/skills/contents/skills/engineering/codebase-design/SKILL.md --jq '.content' | base64 -d
# Catalog overlap scan:
grep -inE "domain-model|CONTEXT.md|ubiquitous|codebase-design|ADR|documentation-and-adrs" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **The ADR gate is the load-bearing idea, and it is sharp.** The three-part test (hard to reverse + surprising + real trade-off) directly attacks the failure mode of both humans and agents asked to "document decisions": producing ceremony for every trivial choice until ADRs become noise nobody reads. By making the *default* "skip the ADR," the skill keeps the record high-signal. This is materially better-specified than the catalog's incumbent `documentation-and-adrs`, which supplies templates but not a discipline for *when not to* write one.
- **"Glossary and nothing else" is an unusually strong invariant.** The hardest part of keeping a ubiquitous-language doc alive is that it silently rots into a spec/scratch-pad. The skill's flat prohibition on implementation details, plus the "is this a project-specific concept or a general programming concept?" filter, is exactly the constraint that keeps `CONTEXT.md` small enough to stay current.
- **`_Avoid_` is a genuinely good mechanism for shared vocabulary.** Listing rejected synonyms (not just the canonical term) is what lets an agent *enforce* the language: it can flag "you said 'client', the glossary says Customer" instead of merely defining terms. This is the difference between a passive glossary and an active linter for language.
- **In-session "challenge / sharpen / cross-reference with code" is the agent-native part.** Inventing edge-case scenarios to force boundary precision, and checking stated behaviour against the actual code ("your code cancels entire Orders but you said partial cancellation is possible — which is right?"), are things an agent with repo access can do cheaply and a solo human usually skips. This is where the skill adds capability rather than just structure.
- **Lazy file creation + minimal ADR template = low adoption cost.** Nothing is created until there's something to write, and an ADR can be one paragraph. The skill is unlikely to generate the busywork that kills documentation disciplines.
- **Strong provenance and ecosystem fit.** 136K-star MIT repo, pushed today, Matt Pocock. It is the shared substrate for a coherent family — `grill-with-docs` (stress-test a plan against the documented language), `improve-codebase-architecture` (refactor "informed by the domain language in CONTEXT.md"), and `codebase-design` all read these same artifacts. Adopting domain-modeling is what makes those siblings useful.

## What didn't work or surprised us

- **It only pays off if the artifacts are actually maintained.** A `CONTEXT.md` that drifts from the code is worse than none — it actively misleads the next agent. The skill's value is entirely conditional on the inline-update discipline being honoured across many sessions; a single session that adds terms and never revisits them starts the rot. This is a real adoption risk, not a hypothetical.
- **Overlap with `documentation-and-adrs` is partial, and the catalog's stated overlap undersells the difference.** The catalog pairs them, but they are not interchangeable: `documentation-and-adrs` (addyosmani) is template-and-philosophy heavy; domain-modeling is gate-and-glossary heavy and adds the ubiquitous-language half entirely. They could be run together, but the ADR halves would compete — domain-modeling's "skip unless all three" gate is the better default and should win.
- **DDD-flavoured and opinionated.** The whole model (bounded contexts, context maps, ubiquitous language, event-driven inter-context relationships in the examples) is Domain-Driven Design vocabulary. On a small CRUD app or a script, the multi-context machinery is overkill and the single `CONTEXT.md` may collect only a handful of terms — fine, but the ceiling on value scales with domain complexity.
- **Couples best as a set, not a singleton.** Unlike `resolving-merge-conflicts` (fully self-contained, drop anywhere), domain-modeling's full value is realised alongside its siblings. Adopting it alone gets you the glossary/ADR habit; the bigger leverage (grill-against-docs, architecture refactors informed by the language) requires adopting the family.
- **No enforcement outside a triggered session.** The skill challenges language only while it's active. Nothing keeps a future PR or a different agent from reintroducing "client" — there's no hook or CI check. It's a discipline, not a guardrail. (Illustrative: a teammate's PR using a banned synonym would pass untouched unless an agent running this skill happens to review it.)

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Cross-referencing stated behaviour against code, and stress-testing relationships with edge-case scenarios, surfaces model/code contradictions before they become bugs |
| Speed | neutral | Adds upfront design/recording time per session; pays back over the project's life via faster onboarding and less re-litigation, but no per-session speedup |
| Maintainability | + | A maintained ubiquitous-language glossary + high-signal ADRs are precisely the artifacts that keep a codebase navigable for future engineers and agents; the "glossary only" and ADR-gate invariants keep them from rotting |
| Safety | neutral | Process/docs skill; no new permissions, tools, or attack surface |
| Cost Efficiency | + | A shared vocabulary reduces repeated clarification turns ("which 'account' do you mean?") and gives future agents grounded context, cutting re-discovery token spend across sessions |

## Verdict

**CONDITIONAL**

domain-modeling is a high-quality, well-authored Plan-stage process skill whose load-bearing contributions — the three-part ADR gate, the "glossary and nothing else" invariant, and the `_Avoid_`-synonym mechanism that lets an agent *enforce* language rather than merely define it — are genuinely better-specified than the catalog's incumbent `documentation-and-adrs`. Shared-vocabulary modeling is a real dev-loop lever: it improves Maintainability and Correctness by grounding every later session in consistent terms and recorded rationale, and it is the substrate that makes the sibling skills (`grill-with-docs`, `improve-codebase-architecture`) work.

It is CONDITIONAL rather than ADOPT for two reasons. First, its value is entirely contingent on the artifacts being *maintained* — an abandoned or drifting `CONTEXT.md` is worse than none — so it earns its keep only on projects with enough domain complexity and longevity to justify the upkeep (multi-context systems, long-lived products, multi-agent teams), not scripts or short-lived CRUD apps. Second, it couples best as a set, not a singleton. Adopt it on domain-rich, long-lived projects — ideally alongside its mattpocock siblings — and run its ADR discipline *instead of*, not in addition to, `documentation-and-adrs`. (Contrast with `resolving-merge-conflicts` from the same repo, which is ADOPT precisely because it is self-contained and unconditionally better than the agent default; domain-modeling's payoff is real but project-dependent.)

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [domain-modeling](https://github.com/mattpocock/skills) | skill | Build CONTEXT.md glossaries and ADRs — pin down ubiquitous language as designs evolve | Teams use inconsistent terminology; decisions aren't recorded for future agents | documentation-and-adrs, codebase-design |
