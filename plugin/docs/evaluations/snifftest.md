# Evaluation: snifftest

**Repo:** [DanRWilloughby/snifftest](https://github.com/DanRWilloughby/snifftest)
**Stars:** 24 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-20
**Last triaged:** 2026-09-20  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A zero-dependency prose linter — countable rules plus one judgment-model call — that
sniffs out AI writing tells in coding-agent output.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (sloptrim, nopus, jev-review). That is
sufficient to place the lead and note none of its named overlaps is a STACK incumbent,
not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: sloptrim and nopus are both purely structural/stdlib detectors
with no model call; snifftest's hybrid design (deterministic rules plus one judgment-model
pass) is a real design difference worth a first-time look rather than a mechanical SKIP.
Left for the P0/eval-runner lane.

_Triaged 2026-09-20 by today's discovery lead._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [snifftest](https://github.com/DanRWilloughby/snifftest) | tool | Zero-dependency prose linter sniffing out AI writing tells — countable rules plus one judgment-model call | Agent-written prose reads as generic AI writing with nothing catching it before it ships | sloptrim, nopus, jev-review |
