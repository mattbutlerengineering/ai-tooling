# Evaluation: Tracely

**Repo:** [jwuthri-cloud/Tracely-ai](https://github.com/jwuthri-cloud/Tracely-ai)
**Stars:** 1,073 | **Last updated:** 2026-10-19 (pushed) | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (outer loop: observability and CI regression gating)
**Layer:** Tooling

---

## What it does

Trace-native CI/CD for AI agents. Tracely grades every production agent trace as it lands,
clusters the failures into issues, freezes the bad runs into hermetic replayable test cases,
blocks the pull request that would ship them again, and alerts the moment any of it happens.
Self-hostable, with a PyPI SDK (`tracelyai-sdk`) and ClickHouse-backed storage.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the README,
the CATALOG one-liner, and GitHub repo metadata (stars, license, topics). No hands-on run was
performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

New lead, cataloged today. P3 backlog — its "Overlaps with" peers (`langfuse`, `agent-delivery-gates`,
`gap-trap`) are themselves discovery-log/review-stage entries, not a STACK pick this tool is
redundant with. Distinct mechanism (production-trace-to-regression-test freezing with a CI
gate) from the generic observability platforms it's filed next to. Left at `discovery-log`;
stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [Tracely](https://github.com/jwuthri-cloud/Tracely-ai) | tool | Grades every production agent trace as it lands, clusters failures into issues, and freezes them into replayable regression tests that gate the PR (MIT) | Agent failures in production leave no regression test or CI gate stopping the same failure from shipping again | langfuse, agent-delivery-gates, gap-trap |  |
