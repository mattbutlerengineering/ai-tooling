# Evaluation: gbrain

**Repo:** [garrytan/gbrain](https://github.com/garrytan/gbrain)
**Stars:** 27,746 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (harness configuration)
**Layer:** Process

---

## What it does

An opinionated agent "brain" configuration — the companion to `gstack`, ported to the OpenClaw /
Hermes Agent harness pair.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`gstack`, `ECC`, `superpowers`). Sufficient for a
SKIP that turns on *host scope*; not sufficient for a positive verdict, and none is offered.

## Verdict

**SKIP** — it configures a harness pair this stack does not run. gbrain is, by its own description,
the OpenClaw/Hermes port of `gstack`; the supported harnesses here are Claude Code and opencode
(ADR-0002), and a configuration pack is worth exactly the harness it targets — its whole substance
is files laid down in another tool's config directories.

On the discipline it encodes, the incumbent is
[`superpowers`/GSD](https://github.com/obra/superpowers) (STACK, `MEASURED`), and the Claude-Code
side of this same lineage is `gstack`, which is already a catalog row in its own right. Nothing here
reaches this stack that is not already reachable through one of those two.

★27.7K reflects the author's reach rather than the pack's applicability, and it is worth saying so
plainly: star count is not portability. This is the same call `page-agent` and `claude-task-master`
got — a real artifact aimed at a host we do not run.

Re-open if this stack adopts OpenClaw or Hermes Agent as a harness, at which point gbrain is the
obvious first configuration to read.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gbrain](https://github.com/garrytan/gbrain) | harness | Garry Tan's opinionated OpenClaw/Hermes Agent Brain — companion configuration to gstack, ported to the OpenClaw/Hermes harness pair | Want a known-good agent configuration rather than assembling one | gstack, ECC, superpowers |
