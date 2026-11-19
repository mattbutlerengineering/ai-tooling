# Evaluation: pulsar

**Repo:** [yocontra/pulsar](https://github.com/yocontra/pulsar)
**Stars:** 51 | **Last updated:** 2026-11-19 (pushed) | **License:** MIT
**Last verified:** 2026-11-19
**Last triaged:** 2026-11-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An MCP server that lets AI coding agents in any harness find and message each other —
a shared directory, tags, multicast, and a `*` bus — over MCP rather than a bespoke
daemon or broker.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. That is sufficient to confirm the lead has no
overlap with a STACK pick, not to judge the tool's own behavior. It would not support
an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. `imbo`, `agmsg`, and `openrig` solve the same cross-agent
messaging problem but each over its own transport (Rust binary, shared SQLite file,
tmux) — none is an MCP server, so pulsar is a differently-plumbed entry in an already
crowded space rather than a clone of a named incumbent. No STACK pick covers this job.

_Triaged 2026-11-19 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pulsar](https://github.com/yocontra/pulsar) | MCP server | MCP server (MIT) letting coding agents in any harness find and message each other — one list, tags, multicast, a `*` bus | Coding agents running in different harnesses have no shared directory or bus to find and message each other through MCP | imbo, agmsg, openrig |
