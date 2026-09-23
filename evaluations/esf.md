# Evaluation: esf

**Repo:** [mitkox/esf](https://github.com/mitkox/esf)
**Stars:** 95 | **Last updated:** 2026-09-23 (pushed) | **License:** MIT
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A self-hosted "engineering software factory" (Go, MIT) — a fork of Machinist relicensed MIT — that
orchestrates "CubeSandbox" coding agents via Temporal, with deterministic verification steps and a
durable evidence trail for each run.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the Temporal/CubeSandbox/verification pipeline. That is sufficient to
catalog it and place it relative to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog. Same durable-Temporal-orchestration shape as `flow (Aixle)`, which is also an
un-evaluated discovery-log lead, so there's no settled STACK incumbent to call this redundant with.
Being a fork of an existing tool (Machinist) relicensed to MIT is itself notable and worth a human
look rather than a mechanical disposition. Left at `discovery-log`.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [esf](https://github.com/mitkox/esf) | platform | Self-hosted engineering software factory (MIT, Machinist fork) — Temporal-orchestrated CubeSandbox agents with deterministic verification and durable evidence trails | Running agents in production needs durable orchestration and an auditable evidence trail, not a hand-rolled script | flow (Aixle), software-factory-harness, 8090 Software Factory |  |
