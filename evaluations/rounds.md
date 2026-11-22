# Evaluation: rounds

**Repo:** [krispuckett/rounds](https://github.com/krispuckett/rounds)
**Stars:** 72 | **Last updated:** 2026-11-21 (pushed) | **License:** MIT
**Last verified:** 2026-11-22
**Last triaged:** 2026-11-22  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A local canvas that collects everything a Claude Code session produces — diffs, files,
and other output — into one browsable place, instead of leaving it scattered across
terminal scroll and separate file edits.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and the repo's own description. That is sufficient to place the tool
in the band it belongs to, not to assess its behaviour. It would not support an ADOPT,
and this eval offers none.

## Verdict

**discovery-log — tentative read** — brand-new lead (found in today's discovery pass),
never exercised.

## Triage note

Landed in P3 backlog with zero overlap pressure — no STACK pick is cited against it, and
nothing structural (archived, vendored-under-copyleft, ships-inside) applies. Left at
`discovery-log`; nothing here forces or forbids a disposition, and a mechanical pass has
no basis to SKIP a lead no incumbent challenges. Worth a first-time look later against
`claude-devtools`/`claude-flightdeck` to see whether it's a genuinely distinct
artifact-browsing niche or redundant with one of them once actually exercised.

_Triaged 2026-11-22 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rounds](https://github.com/krispuckett/rounds) | tool | Local canvas (MIT) collecting everything your Claude Code sessions produce in one place to browse | Claude Code session output scatters across diffs, files, and terminal scroll with no single place to browse what was made | claude-devtools, claude-flightdeck, export-md |
