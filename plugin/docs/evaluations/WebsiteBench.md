# Evaluation: WebsiteBench

**Repo:** [TIGER-AI-Lab/WebsiteBench](https://github.com/TIGER-AI-Lab/WebsiteBench)
**Stars:** 787 | **Last updated:** 2026-11-17 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-26
**Last triaged:** 2026-11-26  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A benchmark testing whether AI agents can rebuild real websites purely through browser
exploration (no source access) — scores reconstruction fidelity against the original site.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this benchmark. This evaluation is source-grounded only: the
CATALOG one-liner and the "Overlaps with" cell.

## Triage note

Left at `discovery-log` — a standalone benchmark with no catalogued incumbent testing this
exact capability (agent-driven website reconstruction from exploration alone, as opposed to
`harbor`/`swe-sweep`'s bug-fixing/environment-eval focus). Worth a real look once someone
wants to compare coding-agent browser-exploration fidelity, not a mechanical SKIP.

_Triaged 2026-11-26 by the daily discovery routine (new lead, same-day triage)._
