# Evaluation: stele

**Repo:** [johnwangwyx/stele](https://github.com/johnwangwyx/stele)
**Stars:** 2 | **Last updated:** 2026-09-02 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

Keeps write-ahead task state so work resumes in any coding-agent harness with nothing to
re-explain — aimed at rate-limit or harness-switch scenarios.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata from the daily discovery scan.

## Triage note

No STACK-pick overlap detected (P3 backlog). Conceptually close to `handoff-skill`,
`portable-handoff`, and `jiaojie-skill` (cross-session/cross-harness handoff), none of
which are STACK picks, so no redundancy claim applies. Very early (2★, 1 day old); left at
`discovery-log` rather than a first-time hands-on eval.

_Triaged 2026-09-02 by the P3 backlog band (daily discovery-and-triage routine, bulk,
eliminate-only)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [stele](https://github.com/johnwangwyx/stele) | tool | Keeps write-ahead task state (MIT) so work resumes in any coding-agent harness with nothing to re-explain | Hitting a rate limit or switching coding agents loses in-flight task state and forces re-explaining the task from scratch | handoff-skill, portable-handoff, jiaojie-skill |
