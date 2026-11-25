# Evaluation: shrink-anything

**Repo:** [EL4CTEO/shrink-anything](https://github.com/EL4CTEO/shrink-anything)
**Stars:** 254 | **Last updated:** 2026-11-23 (pushed) | **License:** MIT
**Last verified:** 2026-11-25
**Last triaged:** 2026-11-25  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An agent skill that deletes dead code, files, dependencies, and assets from a
codebase, keeping each cut only if the project's own tests still pass.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this
eval offers none.

## Triage note

Newly discovered and catalogued today via the daily discovery pass. No STACK pick is
cited in "Overlaps with" (pressure 0), so there is no redundancy claim to make and no
license/vendoring issue to mechanically SKIP on — it is MIT and run locally, not
vendored. Overlaps with `skylos` (dead-code detection) and its own author's sibling
`fast-anything` (same test-gated-cut pattern, applied to speed instead of size), but
neither is a STACK pick, so this does not band P2. Left at `discovery-log` for a real
hands-on eval rather than a first-day guess.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [shrink-anything](https://github.com/EL4CTEO/shrink-anything) | tool | Agent skill (MIT) that deletes dead code, files, dependencies, and assets, keeping each cut only if tests still pass | Removing unused code/deps/assets by hand is tedious and risks silent breakage with no mechanical check | fast-anything, skylos, ai-agent-skill-router |
