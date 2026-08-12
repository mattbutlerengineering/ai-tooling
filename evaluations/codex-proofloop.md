# Evaluation: codex-proofloop

**Repo:** [regenrek/codex-proofloop](https://github.com/regenrek/codex-proofloop)
**Stars:** 28 | **Last updated:** 2026-08-11 (pushed) | **License:** MIT
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Git-based test distillation for Codex agents — "catch aggressively, commit reluctantly": a gate
that distills and proves tests before letting a commit land.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: repo metadata plus the CATALOG
"Overlaps with" cell. Enough to place it against the STACK incumbent it was banded against, not
enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped, despite being banded P2 against `stryker-js`. `stryker-js` is
JS/TS mutation testing — it grades whether existing tests catch injected bugs. `codex-proofloop`'s
stated job is different: a git-based commit gate that distills and proves tests *before* a commit is
allowed to land, agent-agnostic rather than JS/TS-specific. Different mechanism, different scope;
not a defensible redundancy claim, so left for a real read.

_Triaged 2026-08-12 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codex-proofloop](https://github.com/regenrek/codex-proofloop) | tool | Git-based test distillation (MIT) for Codex agents — catch failures aggressively, commit only once proven | Agents commit code that merely looks tested; want a gate that distills and proves tests before a commit lands | stryker-js, tdd-guard, keploy |
