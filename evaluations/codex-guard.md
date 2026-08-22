# Evaluation: codex-guard

**Repo:** [Akimiya-z/codex-guard](https://github.com/Akimiya-z/codex-guard)
**Stars:** 39 | **Last updated:** 2026-08-21 (pushed) | **License:** MIT
**Last verified:** 2026-08-22
**Last triaged:** 2026-08-22  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A quality gate for AI/Codex-generated pull requests: blocks TODO leftovers, leaked secrets, sloppy commits, and red CI before they reach main.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `codex-proofloop` and `testseal` cover adjacent ground (test-suite integrity, proof-before-commit), but codex-guard's specific bundle — TODO/secret-leak/sloppy-commit/red-CI checks bound together as one PR-facing gate — is a distinct enough combination that redundancy is not a defensible mechanical call from metadata alone. Still very new (created 2026-08-20); worth a real look once it has more history.

_Triaged 2026-08-22 by the P3 backlog band._
