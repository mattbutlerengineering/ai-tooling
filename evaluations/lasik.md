# Evaluation: lasik

**Repo:** [pktq/lasik](https://github.com/pktq/lasik)
**Stars:** 130 | **Last updated:** 2026-11-10 (pushed) | **License:** MIT
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A static de-blinding CLI plus MCP server that undoes "BLA" (Blind LLM Agent)
hardening, so a coding agent or reviewing-exfiltration-agent (REA) can read
the real code again instead of an obfuscated stand-in. It never executes the
target it is de-blinding.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide
whether this lead is redundant with a catalogued incumbent, not to judge the
tool's actual behavior — this eval offers no ADOPT/KEEP signal.

## Triage note

This lead cites `SkillSpector` (a STACK pick) in its "Overlaps with" cell, which
bands it P2 challenger, but the two do different jobs: SkillSpector scans agent
skills for malicious patterns, while this tool reverses a specific code-level
obfuscation technique aimed at blinding LLM agents so they can read source at
all. Not a genuine redundancy — SKIPping it on that basis would be the
mechanical-SKIP-on-weak-overlap mistake the eliminate-only guardrail warns
against. Left at `discovery-log` for a real hands-on eval.

_Triaged 2026-11-15 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lasik](https://github.com/pktq/lasik) | tool | Static de-blinding CLI + MCP server (MIT) undoing BLA ("Blind LLM Agent") hardening so coding agents can read the real code again | Code hardened against LLM agents blinds a coding agent from reviewing or editing it, with no tool safely reversing that hardening | vibe-shield, agent-scan, SkillSpector |
