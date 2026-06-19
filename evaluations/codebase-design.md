# Evaluation: codebase-design

**Repo:** [mattpocock/skills](https://github.com/mattpocock/skills)
**Stars:** 136,535 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan (interface/module design; touches Implement when restructuring code and Reflect when deepening existing modules)
**Layer:** Process

---

## What it does

Deep-module design vocabulary — interfaces, seams, adapters, depth/leverage/locality. It is a Claude Code skill at `skills/engineering/codebase-design/SKILL.md` inside Matt Pocock's "Skills for Real Engineers" marketplace, with two bundled reference files (`DEEPENING.md`, `DESIGN-IT-TWICE.md`). It triggers when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.

The core thesis is John Ousterhout's *A Philosophy of Software Design* idea — **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface — adapted into a precise, opinionated glossary that an agent is told to use *exactly* (don't substitute "component," "service," "API," "boundary"). The mechanism is a controlled vocabulary plus a set of design heuristics, structured for progressive disclosure across three files:

- **The glossary (in `SKILL.md`)** defines eight load-bearing terms, each with an `_Avoid_` line listing rejected synonyms — the same enforce-the-language mechanism domain-modeling uses for `CONTEXT.md`:
  - **Module** (scale-agnostic: function, class, package, or tier-spanning slice; _Avoid_: unit, component, service)
  - **Interface** (everything a caller must know — type signature *plus* invariants, ordering, error modes, config, perf; _Avoid_: API, signature, which are too narrow)
  - **Implementation** vs **Adapter** (substance vs role)
  - **Depth** (defined as *leverage at the interface* — behaviour exercised per unit of interface learned — explicitly **not** Ousterhout's implementation-lines-to-interface-lines ratio, which "rewards padding")
  - **Seam** (Michael Feathers — a place you can alter behaviour without editing in that place; _Avoid_: boundary, which collides with DDD's bounded context)
  - **Leverage** (what callers get) and **Locality** (what maintainers get) as the two payoffs of depth.
- **Design heuristics** in `SKILL.md`: the **deletion test** (delete the module — if complexity vanishes it was a pass-through, if it reappears across N callers it earned its keep); **the interface is the test surface** (callers and tests cross the same seam; testing *past* it means the module is the wrong shape); **one adapter = hypothetical seam, two adapters = real seam** (don't add indirection unless something varies); plus three testability rules (accept dependencies don't create them; return results don't mutate; small surface area). A "Rejected framings" section explicitly names what the skill is *not* (Ousterhout's ratio, the TS `interface` keyword, "boundary").
- **`DEEPENING.md`** — how to safely merge a cluster of shallow modules into one deep module, keyed to four **dependency categories** (in-process / local-substitutable like PGLite / remote-but-owned via ports & adapters / true-external via mocks), each dictating the test strategy across the seam. Plus "replace, don't layer" — delete the old shallow-module unit tests once tests exist at the deepened interface; tests assert observable outcomes through the interface, not internal state.
- **`DESIGN-IT-TWICE.md`** — a parallel sub-agent pattern (also Ousterhout: "your first idea is unlikely to be the best"). Frame the problem space for the user, then spawn 3+ Agent-tool sub-agents, each given a *different* design constraint (minimize interface / maximize flexibility / optimize for the common caller / ports-and-adapters), each emitting an interface + usage + what's hidden + dependency strategy + trade-offs. Present sequentially, compare on depth/locality/seam placement, then give an opinionated recommendation or hybrid.

## How we tested it

Skill-mechanism review. Method: read the full `SKILL.md` and both bundled reference files (`DEEPENING.md`, `DESIGN-IT-TWICE.md`) pulled from the repo via the GitHub API; read the sibling skill `domain-modeling/SKILL.md` and the two calibration evaluations from the same repo (`domain-modeling.md` CONDITIONAL, `resolving-merge-conflicts.md` ADOPT); and mapped the surrounding mattpocock ecosystem (`improve-codebase-architecture`, `domain-modeling`, `prototype`, `grill-with-docs`) plus the catalog's stated overlap. I did **not** run it end-to-end against a live design/refactor session on a throwaway repo — the artifact under test is a prompt-only process skill, so the thing being evaluated *is* the vocabulary, the heuristics, and the two procedures, all of which are reproduced above. Note: this skill is already present in the running session's skill list as `codebase-design` with the exact frontmatter shown, because the user has `mattpocock/skills` cloned locally — so the practical question is "does it earn shelf space," not "should I install it."

```bash
gh api repos/mattpocock/skills --jq '{stars,license:.license.spdx_id,description,updated}'
gh api "repos/mattpocock/skills/git/trees/main?recursive=1" --jq '.tree[] | select(.path | test("codebase-design";"i")) | .path'
gh api repos/mattpocock/skills/contents/skills/engineering/codebase-design/SKILL.md --jq '.content' | base64 -d
gh api repos/mattpocock/skills/contents/skills/engineering/codebase-design/DEEPENING.md --jq '.content' | base64 -d
gh api repos/mattpocock/skills/contents/skills/engineering/codebase-design/DESIGN-IT-TWICE.md --jq '.content' | base64 -d
# Catalog overlap scan:
grep -inE "codebase-design|deep module|seam|improve-codebase-architecture|design.it.twice|Ousterhout|prototype|domain-model" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **A precise shared vocabulary is exactly the right intervention for the named problem.** The catalog's problem statement is "agent designs shallow modules; need a shared vocabulary for meaningful abstraction." An agent's untutored default is to chop code into many small "services" or "components" with wide interfaces (shallow modules) because that *looks* modular. Naming **depth**, **leverage**, and **locality** — and giving the agent the deletion test to catch pass-throughs — directly attacks that failure mode. This is capability, not just structure: the agent now has a criterion for *good* abstraction, not just a habit of abstracting.
- **`_Avoid_`-synonym discipline makes the vocabulary enforceable, not decorative.** Same mechanism as domain-modeling's glossary: by listing rejected words ("don't say API, say interface"; "don't say boundary, say seam"), the skill lets an agent flag inconsistent language rather than merely defining preferred terms. The deliberate collision-avoidance with DDD ("boundary" overloaded with bounded context) shows it was designed to *compose* with domain-modeling rather than fight it.
- **Redefining "depth" as leverage, and explicitly rejecting Ousterhout's line-ratio, is the sharpest idea here.** The line-count ratio is gameable (pad the implementation); leverage-per-unit-of-interface-learned is the property you actually want and the one an agent can reason about when proposing an interface. The "Rejected framings" section is unusually disciplined skill-writing — it tells the agent what *not* to import from training data.
- **The dependency-category-to-test-strategy mapping in `DEEPENING.md` is genuinely operational.** Most "design deep modules" advice stops at the principle. This skill says: classify the dependency (in-process / local-substitutable / remote-owned / true-external), and that classification *determines* whether you need a port and what kind of test adapter. "One adapter = hypothetical seam, two = real seam" is a crisp rule against speculative indirection — the over-abstraction failure mode that's the mirror image of shallow modules. "Replace, don't layer" (delete the old shallow tests) is the bit teams usually skip and end up with redundant test layers.
- **`DESIGN-IT-TWICE.md` is agent-native leverage.** Spawning parallel sub-agents to design the same interface under contradictory constraints, then comparing on depth/locality/seam, is something an agent harness can do cheaply and a solo human almost never does. It turns "design it twice" from aspiration into a concrete fan-out procedure — and it's the part of the family that most clearly needs an agent rather than a doc.
- **Composes cleanly into a coherent family.** It tells `DESIGN-IT-TWICE.md` to include *both* its own vocabulary *and* `CONTEXT.md` domain vocabulary in each sub-agent brief — so architecture language and domain language stay consistent. It is the shared substrate `improve-codebase-architecture` ("find deepening opportunities, informed by CONTEXT.md") builds on. domain-modeling names *what things are*; codebase-design names *how modules are shaped*. They are complementary halves of design vocabulary, not competitors.

## What didn't work or surprised us

- **It's vocabulary + judgement framing, not enforcement.** Like domain-modeling and resolving-merge-conflicts, this only operates inside a triggered session. Nothing stops a later PR or a different agent from reintroducing a shallow module or calling a seam a "boundary." There's no hook or CI check — it's a discipline, not a guardrail.
- **Value scales with codebase size and longevity.** On a small script or a short-lived CRUD app, the deep-module machinery (seams, adapters, dependency categories, design-it-twice fan-out) is overkill — the modules are too few and too simple for the vocabulary to earn its cost. The ceiling on payoff rises with architectural complexity and the number of future readers (human or agent).
- **`DESIGN-IT-TWICE.md` is token-expensive.** Spawning 3–4 parallel design sub-agents per deepening candidate is a real cost. It's the right tool for a high-stakes interface (one paid back across many call sites), but applying it routinely would be wasteful. The skill doesn't gate *when* design-it-twice is worth it as sharply as domain-modeling gates *when* to write an ADR.
- **Opinionated and prescriptive about terms.** "Use these terms exactly" is the whole point, but it means the skill can clash with a team that already has an established (different) architecture vocabulary. Adopting it is partly adopting Pocock's/Ousterhout's/Feathers' naming — a feature for greenfield/solo work, a small friction in a team with entrenched language.
- **Couples best as a set, not a singleton** — the same finding as domain-modeling. Adopted alone you get a better design vocabulary in one-off sessions. The larger leverage (domain-modeling for the *what*, codebase-design for the *how*, `improve-codebase-architecture` to apply both to an existing repo, `prototype` to sanity-check a shape) is realised across the family. Unlike `resolving-merge-conflicts` (self-contained, drop anywhere), this is a family member.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | The "interface is the test surface" rule and the dependency-category test strategies push tests to assert observable behaviour through the interface, catching the bugs that escape when tests reach past it into internal state |
| Speed | neutral | Adds upfront design deliberation (and, for design-it-twice, parallel sub-agent runs) per design decision; pays back over the codebase's life via leverage and locality, but no per-session speedup |
| Maintainability | + | Directly the point: deep modules concentrate change/bugs/knowledge in one place (locality) and give callers more capability per unit of interface (leverage); the deletion test and seam discipline prevent both pass-through bloat and speculative indirection |
| Safety | neutral | Process/vocabulary skill; no new permissions, tools, or attack surface |
| Cost Efficiency | + / mixed | A shared architecture vocabulary cuts re-litigation and gives future agents a navigable mental model (saves re-discovery tokens), but the design-it-twice fan-out spends tokens up front — net positive for high-leverage interfaces, wasteful if applied indiscriminately |

## Verdict

**CONDITIONAL**

codebase-design is a high-quality, well-authored Plan-stage process skill that targets a real and specific agent failure mode named in the catalog — agents producing shallow modules with wide interfaces because that *looks* modular — and replaces it with a precise, enforceable vocabulary (depth-as-leverage, seam, locality) plus operational heuristics (the deletion test, dependency-category test strategies, "two adapters means a real seam," replace-don't-layer). Its strongest ideas — redefining depth as leverage and explicitly rejecting Ousterhout's gameable line-ratio, and the `DESIGN-IT-TWICE.md` parallel-sub-agent fan-out — make it genuinely additive: it improves Maintainability and Correctness by giving the agent a criterion for *good* abstraction, not just a habit of abstracting.

It is CONDITIONAL rather than ADOPT for the same two reasons as its sibling domain-modeling. First, its payoff scales with codebase size and longevity — on scripts and small CRUD apps the deep-module machinery is overkill, and it earns its keep on architecturally non-trivial, long-lived projects. Second, it couples best as a set, not a singleton: it is the *how-modules-are-shaped* half that complements domain-modeling's *what-things-are* half, and it is the substrate `improve-codebase-architecture` builds on. Versus its sibling, the relationship is **additive, best-as-family** — not redundant. Adopt it on design-heavy, long-lived projects, ideally alongside domain-modeling and the rest of the mattpocock engineering family, and reserve the token-expensive design-it-twice fan-out for high-leverage interfaces. (Contrast with `resolving-merge-conflicts` from the same repo, ADOPT precisely because it is self-contained and unconditionally better than the agent default; codebase-design's payoff is real but project-dependent.)

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codebase-design](https://github.com/mattpocock/skills) | skill | Deep module design vocabulary — interfaces, seams, adapters, depth/leverage/locality | Agent designs shallow modules; need a shared vocabulary for meaningful abstraction | improve-codebase-architecture, domain-modeling |
