# Evaluation: jev-use

**Repo:** [shitianfang/jev-use](https://github.com/shitianfang/jev-use)
**Stars:** 9 | **Last updated:** 2026-09-19 (pushed) | **License:** MIT
**Last verified:** 2026-09-20
**Last triaged:** 2026-09-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code/Codex/pi plugin handing agent steps that need no text output to Jev, a
cheap judgment model, instead of the LLM — measured p50 ~230ms and ~$0.02 per 1,000
judgments, with typed escalation back to the LLM.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (deadeye-cc, cachebeat, skillranker). That
is sufficient to place the lead and note none of its named overlaps is a STACK incumbent,
not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: deadeye-cc fits model/effort to a whole *task*, while jev-use
routes individual no-text-output *steps* within a task to a cheap judgment model — a
narrower, complementary job rather than a duplicate. Not a mechanical SKIP. Left for the
P0/eval-runner lane.

_Triaged 2026-09-20 by today's discovery lead._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jev-use](https://github.com/shitianfang/jev-use) | plugin | Claude Code/Codex/pi plugin handing agent steps needing no text output to Jev's cheap judgment model instead of the LLM | Every agent step burns a full LLM call even when the step is a binary decision that needs no prose | deadeye-cc, cachebeat, skillranker |
