# Evaluation: mergegate

**Repo:** [damian-kolasinski/mergegate](https://github.com/damian-kolasinski/mergegate)
**Stars:** 5 | **Last updated:** 2026-10-19 (pushed) | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A local code-review hub (Rust) for developers running several AI coding agents in parallel.
Agents submit work with one CLI; the operator reviews it in a fast local UI with files ordered
by importance, comments on lines, marks files viewed, and requests changes — feedback goes
straight back to the agent that wrote the code, no copy-paste. Works over GitHub or plain git.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the README,
the CATALOG one-liner, and GitHub repo metadata (stars, license, topics). No hands-on run was
performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

New lead, cataloged today. P3 backlog — zero overlap pressure (no existing row cites it yet).
Closest peers (`facet`, `easel`, `human-in-the-loop`) are human-approval-gate tools, none a
STACK pick, so not a P2 challenger. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [mergegate](https://github.com/damian-kolasinski/mergegate) | tool | Local code-review hub (MIT, Rust) for developers running several AI coding agents in parallel — files ranked by importance, feedback fed straight back to the agent | Reviewing many agents' submitted work means ad hoc diffing with no importance-ranked queue or a direct feedback loop back to the agent that wrote it | facet, easel, human-in-the-loop |  |
