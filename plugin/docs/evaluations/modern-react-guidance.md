# Evaluation: modern-react-guidance

**Repo:** [adhhamdev/modern-react-guidance](https://github.com/adhhamdev/modern-react-guidance)
**Stars:** 28 | **Last updated:** 2026-09-21 (pushed) | **License:** MIT
**Last verified:** 2026-09-25
**Last triaged:** 2026-09-25  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An agent skill (MIT) documenting current React 19+ APIs — Actions, `use`, the React Compiler, View
Transitions, Fragment refs, `Activity`, `browser()`, and `useEffectEvent` — so a coding agent writes
against today's React rather than the stale pre-19 patterns baked into its training data.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this skill. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (vercel-labs/agent-skills, agent-skills, mattpocock/skills).
That is sufficient to note the overlap with Vercel's broader React/Next skill collection, not to
judge whether the narrower React-19-specific coverage here is materially better or redundant — it
would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped as redundant: `vercel-labs/agent-skills` covers
React/Next performance and view-transitions broadly, but is a 9-skill collection rather than a
React-19-specific reference, and this repo's one-liner names several 19.x-era APIs (Compiler,
Fragment refs, `Activity`, `useEffectEvent`) that predate or sit outside Vercel's stated scope. Not
clearly dominated — worth a first-time hands-on eval to see whether the narrower, more current
coverage earns its own slot rather than folding into the existing pick.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [modern-react-guidance](https://github.com/adhhamdev/modern-react-guidance) | skill | Agent skill (MIT) for React 19+ APIs — Actions, `use`, Compiler, View Transitions, Fragment refs, Activity, `useEffectEvent` | Coding agents default to stale pre-19 React patterns from training data; want current API guidance the agent actually follows | vercel-labs/agent-skills, agent-skills, mattpocock/skills |
