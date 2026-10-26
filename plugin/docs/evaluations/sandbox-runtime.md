# Evaluation: sandbox-runtime

**Repo:** [anthropics/sandbox-runtime](https://github.com/anthropics/sandbox-runtime)
**Stars:** 6,700 | **Last updated:** n/a (not checked via API; this session's GitHub access is repo-scoped) | **License:** Apache-2.0
**Last verified:** 2026-10-26
**Last triaged:** 2026-10-26  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

Anthropic's own lightweight sandboxing tool (`srt`) for enforcing filesystem, network,
and Unix-socket restrictions on arbitrary processes at the OS level, without a
container. Uses native platform primitives — `sandbox-exec`/Seatbelt on macOS,
`bubblewrap` + network namespaces on Linux, a restricted account + WFP egress filter
on Windows (alpha). Ships as both a CLI (`srt "cmd"`) and a library, documented as a
beta research preview built for Claude Code — e.g. wrapping a local MCP server's
command so it runs under the same restrictions. Default posture is secure: no network
access and writes only where explicitly allowed.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
repo's own README (fetched over the web, since this session's GitHub API access is
scoped to this repository and does not extend to arbitrary repos) plus the CATALOG
"Overlaps with" cell. That is sufficient to place the lead against its closest catalog
peers, not to support any verdict, and none is offered here.

## Triage note

No STACK pick appears in its "Overlaps with" cell (`code-on-incus`, `strands-agents/box`,
`daytona` are all themselves unevaluated leads or non-STACK rows), so this lands in P3
backlog rather than P2 — nothing to call redundant against. It is also a first-party
Anthropic tool addressing a real gap this catalog already tracks closely (OS-level
agent sandboxing without a container, alongside `code-on-incus` and
`strands-agents/box`), so it is significant enough to deserve a real hands-on eval
rather than a mechanical disposition. Left at `discovery-log`.

_Triaged 2026-10-26 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sandbox-runtime](https://github.com/anthropics/sandbox-runtime) | tool | Anthropic's OS-level sandbox (Apache-2.0, ★6.7K) restricting filesystem/network/Unix-socket access for any process — Seatbelt/bubblewrap/WFP, no container required | Running untrusted agent commands or local MCP servers needs OS-level isolation without container overhead | code-on-incus, strands-agents/box, daytona |
