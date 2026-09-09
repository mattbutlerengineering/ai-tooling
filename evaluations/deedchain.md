# Evaluation: deedchain

**Repo:** [PillCrew/deedchain](https://github.com/PillCrew/deedchain)
**Stars:** 47 | **Last updated:** 2026-09-04 (pushed) | **License:** MIT
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A benchmark scoring whether a browser agent's final report actually matches what it did —
report-fidelity/truthfulness evaluation for web/browser agents, rather than a general agent
verifier.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on
redundancy with a catalogued incumbent, not on the tool's behaviour — a question the overlap
answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`: no structural disposition applies. vet/prove-it/AgentSeed verify
coding-agent work generally (diffs, done-claims); deedchain is scoped specifically to browser
agents' self-reported actions vs. actual behavior — a narrower, domain-specific benchmark
rather than a competing general verifier. None of the three cited peers are STACK picks.

_Triaged 2026-09-09 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deedchain](https://github.com/PillCrew/deedchain) | tool | Benchmark (MIT) scoring whether a browser agent's final report actually matches what it did | Agents can report success while quietly failing or skipping steps; want a repeatable check on report-to-action fidelity | vet, prove-it, AgentSeed |
