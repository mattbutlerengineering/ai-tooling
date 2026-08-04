# Evaluation: sentry

**Repo:** [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp)
**Stars:** 767 | **Last updated:** 2026-07-09 (pushed) | **License:** NOASSERTION
**Dev loop stage:** Reflect (error monitoring)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Official Sentry MCP server — gives an agent access to production error and issue data.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`langfuse`). Enough to place it; not enough for a
positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Bringing production errors into an agent session is one of the cleaner outer-loop
capabilities in the catalog: the Reflect stage is where the loop is supposed to learn what actually broke,
and a stack trace from real traffic is the highest-signal input available for that.

The complement is recorded correctly in the overlaps cell and holds — `sentry` covers application errors,
`langfuse` covers LLM behaviour. Different failure domains; neither substitutes for the other, and both
were left standing.

**The licence needs a human look before promotion, not a SKIP.** `repo-metadata.json` records
`NOASSERTION`, which per CLAUDE.md means GitHub could not parse the LICENSE file — never that one is
absent, and never a disposition on its own. Sentry ships its products under a source-available
Functional Source License, which a parser would plausibly fail on. That is a real question for the
adoption bar and exactly the kind of thing a bulk lane must not guess at: `Memori` in this same slice
reads `NOASSERTION` and is actually Apache-2.0.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sentry](https://github.com/getsentry/sentry-mcp) | MCP server | Error tracking and monitoring integration | Agent needs access to production error data for debugging | langfuse (complementary: sentry = errors, langfuse = LLM behavior) |
