# Evaluation: oh-my-android

**Repo:** [ateymoori/oh-my-android](https://github.com/ateymoori/oh-my-android)
**Stars:** 31 | **Last updated:** 2026-09-29 (pushed) | **License:** MIT
**Last verified:** 2026-09-29
**Last triaged:** 2026-09-29  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers (mobile/Android)
**Layer:** Tooling

---

## What it does

Android emulator and ADB GUI for Mac — dark mode, font size, RTL, TalkBack, network/GPS control, and a Layout Inspector in dp. Ships a built-in MCP server so Claude Code, Codex, or Cursor can drive the emulator directly.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a bulk-triage disposition, not for an ADOPT/KEEP call — this eval offers none.

## Triage note

None of its cited overlaps (unity-mcp, blender-mcp, nuphus-mcp) is a STACK pick, so this lands in P3 backlog rather than a redundancy band. It is the catalog's first Android-emulator-specific MCP server (unity-mcp/blender-mcp cover other domain-specific editors; nuphus-mcp is generic desktop automation) — a real gap it fills rather than a duplicate. Newly catalogued (added 2026-09-29), macOS-only, Swift. Left at discovery-log for a future hands-on look.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [oh-my-android](https://github.com/ateymoori/oh-my-android) | MCP server | Android emulator + ADB GUI for Mac (MIT) — dark mode, RTL, Layout Inspector, plus a built-in MCP server driving the emulator | Agents can't drive an Android emulator directly; mobile UI testing/inspection needs a GUI and MCP bridge, not hand-rolled ADB calls | unity-mcp, blender-mcp, nuphus-mcp |
