# Evaluation: harness-profiler

**Repo:** [afurmanov/harness-profiler](https://github.com/afurmanov/harness-profiler)
**Stars:** 39 | **Last updated:** 2026-11-16 (pushed) | **License:** MIT
**Last verified:** 2026-11-19
**Last triaged:** 2026-11-19  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Records every skill, agent, and tool call of a Claude Code session and shows which
calls share a context and what each one costs in tokens.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient for
a P2 band disposition that turns on redundancy with the named STACK incumbent, not on
the tool's own behavior. It would not support an ADOPT, and this eval offers none.

## Triage note

`triage.py` challenges this against `ccusage` (STACK, MEASURED). ccusage parses local
session logs into daily/monthly/session/model token & cost **reports** — a rollup view
after the fact. This tool's own pitch is call-level tracing: which specific calls
shared a context window and what each one individually cost, closer to `spoor`'s
local trace+cost binary than to a cost-report CLI. That is a different question than
ccusage answers (aggregate spend vs. per-call attribution), not a thinner clone of it.
Left at `discovery-log`, not SKIPped.

_Triaged 2026-11-19 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [harness-profiler](https://github.com/afurmanov/harness-profiler) | tool | Records every skill, agent, and tool call of a Claude Code session (MIT) and shows which calls share a context and what each one costs in tokens | Seeing which calls in a Claude Code session shared context, and what each one cost, means reading raw transcripts by hand | spoor, ccusage, agentpace |
