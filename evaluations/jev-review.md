# Evaluation: jev-review

**Repo:** [NiazMorshed2007/jev-review](https://github.com/NiazMorshed2007/jev-review)
**Stars:** 38 | **Last updated:** 2026-09-17 (pushed) | **License:** MIT
**Last verified:** 2026-09-17
**Last triaged:** 2026-09-17  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

Local-first MCP plugin providing continuous software-quality review for AI coding agents —
scores correctness, complexity, security, and maintainability as the agent edits, powered by
TypeSafe.ai's Jev, rather than as a separate one-off review pass.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (vet, kodus-ai, code-review). That is sufficient to place
the lead, not to judge the tool's behaviour hands-on.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `code-review`. The catalog's existing
review tools (`code-review`, `kodus-ai`, `vet`) run as a discrete pass — on a PR, on demand, or
after changes land. This tool's stated model is continuous, local, in-the-loop scoring during
editing itself, which is a different point in the workflow, not the same job under a new name. A
real redundancy call needs a look at whether that "continuous" claim holds up in practice, not a
mechanical SKIP on the overlap token alone.

_Triaged 2026-09-17 by the P2 challenger band._
