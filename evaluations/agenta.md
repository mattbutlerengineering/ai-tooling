# Evaluation: agenta

**Repo:** [agenta-ai/agenta](https://github.com/Agenta-AI/agenta)
**Stars:** 4,279 | **Last updated:** 2026-07-10 (pushed) | **License:** NOASSERTION
**Dev loop stage:** Outer Loop (LLMOps platform)
**Layer:** Infrastructure
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An LLMOps platform covering prompt engineering and versioning, evaluation, and observability for
LLM applications.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus the
CATALOG one-liner and "Overlaps with" cell (`langfuse`, `pezzo`, `Helicone`, `opik`, `promptfoo`).
Enough to place it in a crowded cluster; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`, and it is the row that most exposes an unresolved cluster question rather than a
per-tool one.

`pezzo` was SKIPped in this pass as substantially overlapping `langfuse`/`opik`/`Helicone`, and agenta was
named in that same overlap set. It is not disposed here for two reasons: it is actively maintained (pushed
2026-07-10, against pezzo's four-month gap), and it is materially larger (★4.3K). The SKIP over there rested
on overlap **plus** a stalling cadence; only the first applies here.

But the honest position is that five rows — `langfuse`, `opik`, `Helicone`, `agenta`, and `promptfoo` on the
eval axis — answer one question, and two of them are P0 leads. **That is a cluster decision, not five
independent ones**, and making it needs a measured comparison rather than another round of triage. Recording
it here so the next pass does not re-derive the same observation.

The licence is a second unresolved item. `repo-metadata.json` records **`NOASSERTION`**, which per CLAUDE.md
means GitHub could not parse the LICENSE file and never that a grant is absent — the same state `Memori`
(actually Apache-2.0) and `rogue` are in. Needs a human read, not a guess.

How this row was found is worth noting: `audit-evals.py --overlaps` surfaced `agenta` as a token cited by
catalogued rows without being catalogued itself. That detector works.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agenta](https://github.com/Agenta-AI/agenta) | platform | Open-source LLMOps platform combining prompt playground, prompt management, LLM evaluation, and observability in one place | Want prompt iteration, versioned prompt management, eval, and tracing for LLM apps without stitching four separate tools | langfuse, pezzo, Helicone, opik, promptfoo |
