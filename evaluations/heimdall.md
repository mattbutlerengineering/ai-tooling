# Evaluation: heimdall

**Repo:** [ArihantDeva/heimdall](https://github.com/ArihantDeva/heimdall)
**Stars:** 29 | **Last updated:** 2026-08-23 (pushed) | **License:** MIT
**Last verified:** 2026-08-23
**Last triaged:** 2026-08-23  <!-- triaged: bulk -->
**Dev loop stage:** Cross-cutting (Memory & Context)
**Layer:** Tooling

---

## What it does

Persistent memory for AI coding agents — one verified `kb_search` call is meant to replace the grep/find/ls orientation loop an agent otherwise repeats every task. Cross-repo, CPU-only (no GPU/embedding-service dependency claimed), and pitched as zero additional token spend.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. Memory & Context is the catalog's most crowded category, but "replace the grep/find/ls orientation loop with one verified lookup" is a specific, testable claim distinct from the generic persistent-memory pitch most neighbors make (lean-ctx and engram are the closer comparisons). Brand new (created 2026-08-20) and unproven — the "zero token spend" and "CPU-only" claims are exactly what a hands-on run would need to verify before any redundancy call.

_Triaged 2026-08-23 by the P3 backlog band (daily discovery routine)._
