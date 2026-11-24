# Evaluation: lochness

**Repo:** [ronyfadel/lochness](https://github.com/ronyfadel/lochness)
**Stars:** 52 | **Last updated:** 2026-11-20 (pushed) | **License:** MIT
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

A Claude Code skill + CLI that localizes an app the way Apple localizes iOS: it looks up Apple's own iOS translations from a database built locally on your Mac, instead of hand-translating strings.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — a narrow, platform-specific (macOS/iOS-translation-database) localization skill with no direct catalogued incumbent.

## Triage note

Left at `discovery-log`, stamped. No STACK pick is cited in its Overlaps cell (the listed peers — godmode, mcode-stack, coleam00/skills — are generic lifecycle skill packs that don't touch localization), so there is no redundancy to SKIP against. Niche enough that it's not an obvious P0 candidate either.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lochness](https://github.com/ronyfadel/lochness) | skill | Claude Code skill + CLI (MIT) that localizes an app by looking up Apple's own iOS translations from a database built locally on your Mac | Localizing app strings the way Apple localizes iOS means hand-hunting Apple's own translations with no local, queryable database | godmode, mcode-stack, coleam00/skills |
