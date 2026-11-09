# Evaluation: ryph

**Repo:** [ryph-hq/ryph](https://github.com/ryph-hq/ryph)
**Stars:** 17 | **Last updated:** 2026-11-09 (pushed) | **License:** MIT
**Last verified:** 2026-11-09
**Last triaged:** 2026-11-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A self-hosted coding-agent platform for a team — agents are on call for incidents, sit in
your chat tool, and operate against your forge (git hosting), rather than living in one
person's terminal.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and its "Overlaps with" cell (`gstack`, `aster`, `agency-agents`). That
is sufficient to check for a named STACK redundancy; it is not sufficient to support an
ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — brand new (created 2026-11-04) at 17 stars. None of
its cited peers is a STACK pick. The team/on-call/chat-native framing is distinct from the
personal-config harnesses (`gstack`, `aster`) it is loosely grouped with, and worth a real
hands-on eval rather than a mechanical SKIP.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-09 by the daily discovery-and-triage routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ryph](https://github.com/ryph-hq/ryph) | platform | Self-hosted coding-agent platform (MIT) on call for your team's incidents, in your chat, and on your forge | On-call incident response and chat-triggered fixes need a human to context-switch into a terminal; want a standing team coding agent reachable from chat, the forge, and incidents directly | gstack, aster, agency-agents |
