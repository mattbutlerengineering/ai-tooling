# Evaluation: xtermium

**Repo:** [xtermium/xtermium](https://github.com/xtermium/xtermium)
**Stars:** 11 | **Last updated:** 2026-11-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-04
**Last triaged:** 2026-11-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement / Agent Orchestration (terminal/session manager with an MCP server)
**Layer:** Infrastructure

---

## What it does

A terminal and session manager (SSH, SFTP, RDP, VNC, telnet, serial, WinRM, BMC
consoles, and tunnels) in tabs and split panes, encrypted on disk, with an MCP server
and CLI so AI agents can run commands across those sessions without ever seeing the
underlying passwords.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. The credential-hiding mechanism for the MCP server
path specifically is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Cites no STACK pick in
`Overlaps with` (mcp-warden, rmux, farhand are catalogued leads, not STACK picks). Not
examined further in this pass.

_Triaged 2026-11-04 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [xtermium](https://github.com/xtermium/xtermium) | tool | Terminal/session manager (Apache-2.0, Rust) for SSH/SFTP/RDP/VNC/telnet/serial/WinRM/BMC — encrypted on disk, with an MCP server so agents run commands without seeing passwords | Letting an agent drive remote sessions means handing it raw credentials in its context, with no encrypted, credential-hidden session layer | mcp-warden, rmux, farhand |
