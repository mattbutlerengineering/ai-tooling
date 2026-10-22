# Evaluation: debuganything

**Repo:** [shreyassaw5394/debuganything](https://github.com/shreyassaw5394/debuganything)
**Stars:** 11 | **Last updated:** 2026-10-19 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

An MCP server + CLI (MIT) letting an AI agent observe a running process, container, or
pod — strace, py-spy, perf, lsof, tcpdump, gdb/lldb, heap snapshots — turned into
evidence-backed findings.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-17). Differentiator over `mirrord` (dev-environment traffic
mirroring) and `systematic-debugging` (a process skill, not an observation tool) is
direct runtime instrumentation (strace/py-spy/perf/gdb) surfaced over MCP. No archived
flag, no disqualifying license, no `Ships inside` container, zero overlap pressure. Left
at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [debuganything](https://github.com/shreyassaw5394/debuganything) | tool | MCP server + CLI (MIT) letting an AI agent observe a running process, container, or pod — strace, py-spy, perf, lsof, tcpdump, gdb/lldb and heap snapshots turned into evidence-backed findings | Agents can read code but can't inspect a live running process or container, so runtime-only bugs stay invisible to them | mirrord, systematic-debugging, dev3000 |
