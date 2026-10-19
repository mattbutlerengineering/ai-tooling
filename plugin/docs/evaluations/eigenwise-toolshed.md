# Evaluation: eigenwise-toolshed

**Repo:** [Eigenwise/eigenwise-toolshed](https://github.com/Eigenwise/eigenwise-toolshed)
**Stars:** 280 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-17
**Last triaged:** 2026-10-17  <!-- triaged: bulk -->
**Dev loop stage:** Cross-cutting
**Layer:** Tooling

---

## What it does

Six independent Claude Code plugins packaged as one marketplace: codebase mapping
(`codebase-mapper`), conditional rule re-injection (`live-rules`), a local task board with
verification gating (`sidequest`), a ChatGPT/Codex and Grok model gateway for the `/model`
picker (`model-gateway`), local metadata-only telemetry (`observability`), and a plugin
setup/update advisor that works across any marketplace on the machine (`quartermaster`). Each
plugin has its own install path and none requires the others.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the repo's
README, its `.claude-plugin/marketplace.json` manifest, and the per-plugin descriptions there.
That is sufficient to place the lead, not to judge any individual plugin's behaviour hands-on.

## Verdict

**discovery-log — tentative read** — newly catalogued this pass; not previously examined.

## Triage note

New lead, added today. Catalogued as the container only (not its individual plugins, to stay
within this run's add cap); the six member plugins — `codebase-mapper`, `live-rules`,
`sidequest`, `model-gateway`, `observability`, `quartermaster` — are listed as overflow in the
scan issue for a future pass to catalogue individually with `Ships inside` declared, following
the `anthropics/claude-plugins-official` precedent. Not a P2 challenger: `mattpocock/skills`
(STACK ADOPT) is a different-purpose engineering-skills pack and doesn't do session-memory
task-boards, model routing, or plugin-install advising. Left at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [eigenwise-toolshed](https://github.com/Eigenwise/eigenwise-toolshed) | plugin | Six independent Claude Code plugins (MIT) — codebase mapping, conditional rule injection, a verification-gated task board, a ChatGPT/Grok model gateway, local observability, and a plugin-setup advisor | Re-teaching context each session, ad hoc model routing, and plugin setup/update friction are separate unsolved problems; want one coherent pack to pick from | headcount, maintainer-skills-lab, mattpocock/skills |  |
