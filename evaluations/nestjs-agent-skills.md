# Evaluation: nestjs-agent-skills

**Repo:** [nestjs/agent-skills](https://github.com/nestjs/agent-skills)
**Stars:** 158 | **Last updated:** 2026-11-20 (pushed) | **License:** MIT
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

The official NestJS agent-skill pack: framework-specific guidance for AI-assisted Node.js/NestJS development, maintained by the NestJS team itself.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — a framework-specific skill pack (NestJS), not a substitute for the general-purpose lifecycle skills it's compared against.

## Triage note

Left at `discovery-log`, not SKIPped. It cites `agent-skills` and `documentation-and-adrs` in Overlaps — both STACK picks — but those are general-purpose lifecycle/documentation skills, while this pack is scoped specifically to NestJS idioms and conventions. A NestJS codebase would plausibly run both together rather than choosing one over the other, so a redundancy SKIP isn't warranted; left for a real eval.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [nestjs-agent-skills](https://github.com/nestjs/agent-skills) | skill | Official NestJS agent-skill pack (MIT) with framework-specific guidance for AI-assisted Node.js/NestJS development | Agents default to generic Node patterns with no curated, maintained NestJS-specific guidance to follow | android/skills, vercel-labs/agent-skills, agent-skills |
