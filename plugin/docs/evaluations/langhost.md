# Evaluation: langhost

**Repo:** [langhost/langhost](https://github.com/langhost/langhost)
**License:** MIT
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Open-source, self-hosted LangGraph Agent Server — production Postgres + Redis, same SDK, same
Studio, zero code changes versus LangGraph's own hosted Agent Server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (LangGraph, conductor, inngest). That is sufficient to
place the lead and note none of its named overlaps are STACK incumbents, not to support an
ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: LangGraph itself is not in STACK, and langhost is complementary rather
than redundant — it self-hosts LangGraph's own Agent Server/Studio rather than competing with
the framework. Fills a real self-hosting gap; not a mechanical SKIP. Left for the
P0/eval-runner lane.

_Triaged 2026-07-31 by today's discovery lead._
