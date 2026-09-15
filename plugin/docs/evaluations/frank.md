# Evaluation: frank

**Repo:** [HimanshuJ16/frank](https://github.com/HimanshuJ16/frank)
**Stars:** 7 | **Last updated:** 2026-09-14 (pushed) | **License:** MIT
**Last verified:** 2026-09-15
**Last triaged:** 2026-09-15  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An anti-sycophancy skill stopping a coding agent from caving on correct code when pushed back on, and from claiming work "done" without running a command that proves it. Claims compatibility with 20 agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. It overlaps `vet`, `prove-it`, and `old-coder` on making agents prove completion rather than assert it, but none is a STACK pick, and its specific angle — anti-sycophancy (not caving on correct code under pushback) — is a narrower behavioral claim than those verification tools make. Worth a real look at whether the claim holds up, rather than a mechanical SKIP. 7★ and 1 day old.

_Triaged 2026-09-15 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [frank](https://github.com/HimanshuJ16/frank) | skill | Anti-sycophancy skill (MIT) stopping a coding agent from caving on correct code or claiming "done" without a proving command | Agents agree with pushback on correct code and claim completion with no verification; want a skill that holds the line | vet, prove-it, old-coder |
