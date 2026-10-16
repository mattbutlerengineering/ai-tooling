# Evaluation: eleven

**Repo:** [Zfinix/eleven](https://github.com/Zfinix/eleven)
**Stars:** 568 | **Last updated:** not verified (pushed date not fetched this pass) | **License:** Apache-2.0
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Agent-first reverse engineering for macOS, Windows, and Linux: any ACP (Agent Client Protocol)
agent can read, rename, and patch binaries, Android apps, and GPU kernels.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only: the public GitHub repo page
(description, star count, license) plus the CATALOG one-liner and "Overlaps with" cell.

## Triage note

Left at `discovery-log`. No STACK pick is cited in its "Overlaps with" cell (`decomp.wtf`,
`awesome-reverse-engineering` are peers, not incumbents), so it is ordinary P3 backlog, not a
structural SKIP candidate. It is also the active peer named in today's `decomp.wtf` SKIP
(archived 2026-10-15) — worth a real look precisely because it is the broader, maintained
option in the same niche, not a reason to dispose of it mechanically here.

_Triaged 2026-10-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [eleven](https://github.com/Zfinix/eleven) | tool | Agent-first reverse engineering (Apache-2.0) — any ACP agent reads, renames, and patches binaries, Android apps, and GPU kernels | Binary/decompiled-code understanding has no agent-native workflow; RE tools (Ghidra, Hopper) aren't built for an agent loop | decomp.wtf, awesome-reverse-engineering |
