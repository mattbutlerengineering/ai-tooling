# Evaluation: mini-harness

**Repo:** [mini-harness/mini-harness](https://github.com/mini-harness/mini-harness)
**Stars:** 20 | **Last updated:** 2026-09-05 (pushed) | **⚠️ no license**
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A small, complete Python agent harness — tools, compaction, retries, and a single-file TUI — built explicitly to be read end-to-end and used as a reference baseline.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. Positioned explicitly as a minimal reference implementation to learn from or fork rather than a production harness competing with gptme/aster on features, so a redundancy SKIP against either would mischaracterize its purpose. No LICENSE file is recorded (Type `harness`, not vendored, so this doesn't trigger a P4 mechanical-skip — a harness is executed, not copied in).

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mini-harness](https://github.com/mini-harness/mini-harness) | harness | Small, complete Python agent harness (⚠️ no license) — tools, compaction, retries, and a single-file TUI, built to learn from and use as a baseline | Production harnesses are too large to read end-to-end; want a minimal, complete reference implementation to learn from or fork | gptme, GenericAgent, aster |
