# Evaluation: fast-anything

**Repo:** [EL4CTEO/fast-anything](https://github.com/EL4CTEO/fast-anything)
**Stars:** 957 | **Last updated:** 2026-11-22 (pushed) | **License:** MIT
**Last verified:** 2026-11-22
**Last triaged:** 2026-11-22  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A workflow (not a framework or CLI) for speeding up slow Python/Node/Ruby code without a
full language port: profile the app, identify the hot 5%, have a coding agent port only
those functions to a faster implementation, and prove the ported functions behave
identically to the originals before replacing them. A sibling concept to `rust-anything`
(same README family/sibling-repo naming convention), but targeted at performance rather
than a full-app rewrite.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, the repo's own description, and the CATALOG "Overlaps with" cell. That
is sufficient to check whether a named incumbent genuinely covers the same job — the
question this triage pass turns on — not to assess the tool's own behaviour. It would not
support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — brand-new lead (found in today's discovery pass),
never exercised.

## Triage note

The P2 challenger band flagged this lead against `stryker-js` (cited in its CATALOG
"Overlaps with" cell, inherited from `rust-anything`'s row). Reading both one-liners
side by side: `stryker-js` is a JavaScript mutation-testing tool — it checks whether an
*existing* test suite actually catches injected bugs. `fast-anything` is about *porting*
hot functions to a faster implementation and proving behavioural equivalence against the
original. These are different jobs (test-suite-quality verification vs. performance
porting-and-proof), so `stryker-js` does not dominate this lead the way the band's
disposition assumes. SKIPping it as "redundant with stryker-js" would be an
evidence-free verdict this repo's eliminate-only rule exists to prevent. Left at
`discovery-log` for a real hands-on eval later — the overlap citation may be worth
narrowing in `CATALOG.md` at that point, since it was inherited wholesale from
`rust-anything`'s row rather than written for this tool specifically.

_Triaged 2026-11-22 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [fast-anything](https://github.com/EL4CTEO/fast-anything) | tool | Profiles slow Python/Node/Ruby apps and ports only the hot functions with your coding agent (MIT), proving they behave the same | Rewriting a whole app for speed is overkill; want to find and safely port only the slow 5% | rust-anything, openrewrite, stryker-js |
