# Evaluation: Apple Docs 2.0 MCP

**Repo:** [mishafyi/Apple-Docs-2.0-MCP](https://github.com/mishafyi/Apple-Docs-2.0-MCP)
**Stars:** 25 | **Last updated:** 2026-10-18 (pushed) | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement (also Plan — checking current Apple API docs before writing code)
**Layer:** Tooling

---

## What it does

An MCP server (a fork of Apple Docs MCP) exposing Apple Developer Documentation — API
reference, Human Interface Guidelines, App Store Connect Help, sample code, and 1,700 WWDC
sessions with transcripts and code — to coding agents, so an agent building an iOS/macOS app
reads Apple's own current docs instead of guessing from stale training data.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the README,
the CATALOG one-liner, and GitHub repo metadata (stars, license, topics). No hands-on run was
performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

New lead, cataloged today. Bands as P2 challenger (cites `context7`, a STACK pick) but is left
at `discovery-log` rather than SKIPped as redundant: context7 is a generic library/framework
documentation lookup, while this server is specialized to Apple's own developer docs, HIG, and
WWDC session transcripts — a documentation source context7 does not index. Significant enough
a differentiation to warrant a real eval rather than a mechanical P2 SKIP. Stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [Apple Docs 2.0 MCP](https://github.com/mishafyi/Apple-Docs-2.0-MCP) | MCP server | MCP server (MIT) exposing Apple's developer documentation, Human Interface Guidelines, and 1,700 WWDC session transcripts to coding agents | Agents building iOS/macOS apps guess at Apple APIs from stale training data instead of reading Apple's own current docs and guidelines | context7, TanStack-cli, azure-skills |  |
