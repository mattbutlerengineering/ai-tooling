# Evaluation: Corvus

**Repo:** [Albasha0x0/Corvus](https://github.com/Albasha0x0/Corvus)
**Stars:** 8 | **Last updated:** 2026-10-23 (pushed) | **License:** MIT
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

A reverse-engineering MCP server (C#) for AI agents — decompiles and patches .NET
assemblies and native PE/ELF/Mach-O binaries, with optional IDA/Ghidra backends.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Pressure 0 — nothing in the catalog cites it yet. Its "Overlaps with" cell names
`ida-pro-mcp`, `eleven`, and `rea`, none of which is a STACK pick, so this does not band
as a P2 challenger. No archived flag, no disqualifying license (MIT), no `Ships inside`
container. Differentiator over `eleven`/`rea` is explicit .NET/IL2CPP + Unity coverage
(topics name `il2cpp`, `unity`) alongside native PE/ELF/Mach-O, which neither of the
existing reverse-engineering peers' one-liners claim. Left at `discovery-log`; very new
(created 2026-10-08) and low-signal (★8) so not an urgent P0 candidate yet.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Corvus](https://github.com/Albasha0x0/Corvus) | MCP server | Reverse-engineering MCP server (MIT) for AI agents — decompiles and patches .NET assemblies and native PE/ELF/Mach-O binaries, with optional IDA/Ghidra backends | Reverse-engineering compiled or obfuscated software with an agent means stitching together separate decompiler tools; want one MCP server across binary formats | ida-pro-mcp, eleven, rea |
