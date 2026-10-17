# Evaluation: pensieve

**Repo:** [TedHaley/pensieve](https://github.com/TedHaley/pensieve)
**Stars:** 65 | **Last updated:** 2026-10-16 (pushed) | **License:** MIT
**Last verified:** 2026-10-17
**Last triaged:** 2026-10-17  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Local macOS search across files, git repos, and past AI-agent sessions by meaning or exact
wording, exposed to agents via MCP, plus a 3D topic map and git-blame ownership view.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge the
tool's behaviour hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; picked up as one of the oldest
untriaged leads in the P2 challenger band this pass.

## Triage note

P2 challenger: cites `serena` and `claude-mem` in Overlaps, pressure 0. Neither incumbent does
pensieve's actual job — serena is symbol-level code navigation, claude-mem is structured
persistent memory with a knowledge graph — and pensieve's own niche (macOS-only, unified search
across files/git/prior sessions plus a 3D topic map) doesn't duplicate either. The macOS-only
scope is a real adoption limiter worth noting for any future eval, but it isn't grounds for a
mechanical redundancy SKIP. Left at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [pensieve](https://github.com/TedHaley/pensieve) | MCP server | Local macOS search (MIT) across files, git repos, and past AI-agent sessions by meaning or exact wording, exposed to agents via MCP, plus a 3D topic map and git-blame ownership | Agents and humans re-derive context already sitting in prior sessions, commits, and files scattered across a machine, with no unified local search | serena, claude-context, claude-mem |  |
