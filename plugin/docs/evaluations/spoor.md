# Evaluation: spoor

**Repo:** [jhisse/spoor](https://github.com/jhisse/spoor)
**Stars:** 5 | **Last updated:** 2026-10-21 (pushed) | **License:** MIT
**Last verified:** 2026-11-02
**Last triaged:** 2026-11-02  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Local-first LLM observability — agent traces, token usage, latency, and estimated cost
in one binary plus one SQLite file, with no hosted backend.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient for
a P2 band disposition that turns on redundancy with the named STACK incumbent, not on
the tool's own behavior — a question the overlap answers directly. It would not
support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `triage.py` challenges it against `ccusage`
(STACK, ADOPT/MEASURED), but ccusage's job is specifically parsing local session logs
into token/cost reports. spoor's stated scope also covers trace inspection and latency,
closer to the bar-observatory/tracecrate class than to ccusage alone — a broader
observability surface, not a pure cost-report duplicate. At 5 stars and days old it is
far less established than the incumbent, so a hands-on look (not a bulk SKIP) is the
right next step if this category gets revisited.

_Triaged 2026-11-02 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [spoor](https://github.com/jhisse/spoor) | tool | Local-first LLM observability (MIT) — agent traces, token usage, latency, and estimated cost in one binary plus one SQLite file | Want lightweight local agent-trace and cost observability without standing up a hosted platform or sending session data anywhere | bar-observatory, tracecrate, ccusage |
