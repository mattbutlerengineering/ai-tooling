# Evaluation: agy-fast

**Repo:** [INK-Q/agy-fast](https://github.com/INK-Q/agy-fast)
**Stars:** 366 | **Last updated:** 2026-11-22 (pushed) | **License:** MIT
**Last verified:** 2026-11-22
**Last triaged:** 2026-11-22  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A non-invasive MCP accelerator plugin for Google Antigravity (CLI/Desktop/IDE) that
claims to cut LLM turns (-34%), token quota (-31%), and upload traffic (-40%) without
touching Antigravity's native UI or diffs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool, and we did **not** verify the claimed
percentage reductions — those are the repo's own self-reported figures, unverified here.
This evaluation is source-grounded only: the CATALOG one-liner and the repo's own
description. That is sufficient to place the tool in the band it belongs to, not to
assess its behaviour or its savings claims. It would not support an ADOPT, and this eval
offers none.

## Verdict

**discovery-log — tentative read** — brand-new lead (found in today's discovery pass),
never exercised; its turn/token/upload-savings figures are self-reported and unverified.

## Triage note

Landed in P3 backlog with zero overlap pressure — no STACK pick is cited against it.
`agy-staff` (the nearest catalogued peer, same Antigravity-bridging niche) does a
different job: it bridges Antigravity's Gemini models *into* Claude Code/Codex as a
second opinion, where `agy-fast` instead accelerates Antigravity's *own* native MCP
usage — not a competing tool for the same task. Left at `discovery-log`; the self-reported
savings numbers (if ever graduated to a real eval) should go through
`evaluations/token-savings-protocol.md` before being taken at face value, per this
repo's own token-savings-claims convention.

_Triaged 2026-11-22 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agy-fast](https://github.com/INK-Q/agy-fast) | plugin | Non-invasive MCP accelerator plugin (MIT) cutting Google Antigravity's LLM turns, token quota, and upload traffic without touching its native UI or diffs | Google Antigravity burns extra turns, tokens, and upload traffic with no drop-in way to cut them without changing its UI or diffs | agy-staff, antiglaude, codex-plugin-cc |
