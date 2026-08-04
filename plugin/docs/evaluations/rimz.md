# Evaluation: rimz

**Repo:** [rimio-ai/rimz](https://github.com/rimio-ai/rimz)
**Stars:** 22 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (multi-agent control)
**Layer:** Tooling

---

## What it does

A realtime dashboard and *control room* for agentic coding, built on tmux and Zellij — it drives
sessions in the multiplexer as well as reporting on them.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04 — the
repo had no record in `repo-metadata.json` before this pass) plus the CATALOG one-liner and
"Overlaps with" cell (`claude-fleet`, `abtop`, `agentsview`, `ping-island`). Enough to place it
against the STACK incumbent; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped, on a category ground — but it is the weakest leave in this
pass and the note should say so.

The banding is against [`abtop`](https://github.com/graykode/abtop) (STACK, `MEASURED`), which
*observes* sessions. rimz is a control room: it launches and steers agents inside tmux/Zellij. Its
actual peers are the session *managers* (`claude-squad`, `agent-of-empires`), and those are not
STACK picks — so the challenger frame this band applies does not reach it, and "redundant with
abtop" would be a claim about the wrong tool.

What argues the other way is adoption: ★22, and the record was missing from the metadata cache
entirely, which is why it reached this pass unbanded on facts. At that size the question is not
whether it beats an incumbent but whether it exists in six months.

Practical disposition: leave the row, do not install, and revisit if the multiplexer-native control
idea gains adoption. Anyone wanting it *today* should look at `claude-squad` first, which is
already in STACK for driving parallel sessions.

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rimz](https://github.com/rimio-ai/rimz) | tool | Realtime dashboard and control room for agentic coding, built on tmux and Zellij | Running several coding agents at once, you can't see status across sessions without checking each terminal | claude-fleet, abtop, agentsview, ping-island |
