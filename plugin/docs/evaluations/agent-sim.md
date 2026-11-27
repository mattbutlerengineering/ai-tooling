# Evaluation: agent-sim

**Repo:** [Developing-Gamer/agent-sim](https://github.com/Developing-Gamer/agent-sim)
**Stars:** 623 | **Last updated:** 2026-11-27 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-27
**Last triaged:** 2026-11-27  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An agent layer over `x86sim/x86sim` (a project that boots the real iOS Simulator on
a regular Linux PC by translating it on the fly) — gives a coding agent an iOS
Simulator to drive on Linux, with no Mac hardware required.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata from GitHub's search API (this session's
GitHub access is scoped to this repo only, so a direct per-repo metadata fetch was
not available; stars/license/pushed-date come from the search endpoint instead).

## Triage note

Left at `discovery-log` — cites no STACK pick in its "Overlaps with" cell
(`mobile-agent-testers`, `dsh-ios`, `simfleet` are catalogued peers but none is
installed in STACK today), so no mechanical P2 redundancy SKIP applies. Differentiated
from `mobile-agent-testers` (which runs across 20 parallel simulators/emulators via
GitHub Actions) by being a local, Linux-native simulator layer rather than a parallel
CI test-running harness — a different point in the same problem space. Notably high
star count (623, brand new) worth a real hands-on eval rather than a mechanical
disposition.

_Triaged 2026-11-27 by the daily discovery routine (new lead, same-day triage)._
