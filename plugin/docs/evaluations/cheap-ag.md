# Evaluation: cheap-ag

**Repo:** [muaaz9329/cheap-ag](https://github.com/muaaz9329/cheap-ag)
**Stars:** 175 | **Last updated:** 2026-10-31 (pushed) | **License:** MIT
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An MCP server (MIT) for Claude Code that routes the actual code-writing to a cheap model while a fixed test suite gates what ships, aimed at stretching a fixed-price Claude plan further.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. It shares the "route cheap work to a cheap model" job with `deadeye-cc` and `claude-code-routing`, neither of which is a STACK pick, so there is no mechanical redundancy call.

## Triage note

No STACK-pick overlap. P3 backlog — left at `discovery-log` with a stamp.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cheap-ag](https://github.com/muaaz9329/cheap-ag) | MCP server | MCP server (MIT) routing Claude Code's actual code-writing to a cheap model, gating output with tests before it ships | Opus-tier usage limits get hit fast when a cheap model could write the boilerplate and tests decide what ships | deadeye-cc, claude-code-routing, quicksilver |
