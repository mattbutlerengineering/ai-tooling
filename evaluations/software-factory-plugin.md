# Evaluation: software-factory-plugin

**Repo:** [8090-inc/software-factory-plugin](https://github.com/8090-inc/software-factory-plugin)
**Stars:** ~6 | **Last updated:** 2026-06-08 | **License:** MIT
**Last verified:** 2026-06-29
**Dev loop stage:** Plan (Requirements → Blueprints → Work Orders is the front of the loop; the execution skills then reach into Implement → Review)
**Layer:** Process (an SDLC methodology delivered as installable skills + scaffolding scripts)

---

## What it does

`software-factory-plugin` is the **open-source, MIT-licensed** packaging of [8090's](https://www.8090.ai/) AI-native SDLC methodology — the same "Software Factory" pipeline that the (proprietary, DEFER) [8090 Software Factory](./8090-software-factory.md) platform sells, but as a portable set of **skills, guides, and execution scripts** for coding agents, with no hosted service required.

It ships a single top-level `software-factory` skill that routes into:

- **Authoring guides** — `requirements-writing-guide.md` (Product Overview + Feature Requirements Documents, `REQ-`/`AC-` IDs), `blueprint-writing-guide.md` (Container/Component/Feature Blueprints as `component`/`model` blocks with `@`-mention edges), `work-order-writing-guide.md` (six-section Work Orders with E2E `COV_` test specs).
- **Execution skills** — `writing-implementation-plans.md`, `execute-work-order.md` (scope-only implementation against a mandatory checklist), `review-phase.md` (delegate-per-bucket review across 6 dimensions, `APPROVED`/`CHANGES_REQUESTED` loop).
- **Scaffolding scripts** — `init-wo-execution.sh` (creates the per-WO execution directory) and `update-context-index.sh`, plus `*-template.md` files for the four execution artifacts.

The methodology's whole point is **traceability**: requirements → blueprints → work orders → code, each a durable cross-linked artifact. The plugin installs via `npx skills add` and is distributed for ~16 harnesses (Claude Code, Cursor, Codex, Gemini, Kiro, Vercel, …). It deliberately ships an **empty MCP config** so teams wire in their own Software Factory or project tools.

## How we tested it

**Evidence:** MEASURED

Installed and exercised hands-on on macOS (arm64) in an isolated scratch repo — not a README skim.

```bash
# 1. Install (real run, exit 0)
npx -y skills add 8090-inc/software-factory-plugin --skill software-factory
#  → installed to ./.agents/skills/software-factory (universal: 16 harnesses,
#    symlinks for Claude Code/Windsurf/OpenHands/Hermes)
#  → skills.sh security panel: Gen "Safe", Socket "0 alerts", Snyk "Low Risk"

# 2. Run the execution scaffold (real run)
bash .agents/skills/software-factory/execution/scripts/init-wo-execution.sh \
  --work-order-number WO-001 --work-order-title "add-health-endpoint" --work-order-id WO-001
#  → created .sw-factory/WO-001/{checklist,context,implementation-plan,review-log}.md
#    with a UTC init timestamp and a populated, phase-structured checklist

# 3. Overwrite-safety guard (real run)
#  re-running the same command → "Error: ... already exists. Refusing to overwrite" (guard fires)
```

**What I verified by running it:** the install succeeds standalone and is security-vetted via skills.sh; the scaffold script produces the real four-file execution directory with a correct timestamp and a non-trivial, phase-organized checklist; the overwrite guard works. **What I did not do:** drive a complete Requirements→…→merged-PR cycle, because the execution checklist's context-gathering phase is written around **MCP tool output** ("review work order description provided by MCP tool output", "read each referenced blueprint **via MCP**") and the plugin ships an empty MCP stub — so the *automated* loop has no work-order source without a backend you supply (see below).

## What worked

- **Clean, fast, standalone install.** `npx skills add` worked first try (exit 0), landed in `.agents/skills/`, multi-harness, with an inline skills.sh security assessment (Safe / 0 alerts / Low Risk). No hosted-service login, no account.
- **The scaffolding scripts genuinely work.** `init-wo-execution.sh` is real, defensive shell (`set -euo pipefail`, an overwrite guard, sed-escaped substitution) that produces the four traceability artifacts — not just prose. The checklist it emits is detailed and phase-structured.
- **High-quality SDLC conventions.** The guides encode a coherent, genuinely useful discipline (typed requirement/AC IDs, blueprints-as-written-diagrams, scope-bounded work orders, delegate-per-bucket review). Adopting just the *conventions* is valuable even without the automation.
- **MIT + decoupled from the paid platform.** Explicitly "does not assume access to a hosted Software Factory service" — the one artifact in 8090's orbit that clears the permissive-OSS adoption bar.

## What didn't work or surprised us

- **The automated loop needs an MCP backend the plugin doesn't provide.** The execution skills assume MCP tools (`get_next_work_order`, `read_blueprint`, …) to source and link work orders. With the shipped empty stub, you get authoring conventions + scaffolding, not a turnkey autonomous factory — you'd hand-author the Requirements/Blueprints/Work Orders as markdown and feed them manually, or stand up your own server.
- **Very young, very small.** v0.0.1, ~6 stars, last pushed 2026-06-08. The conventions are mature (lifted from a commercial product) but the open packaging is brand new and unproven at scale.
- **Heavy ceremony for small work.** The full Requirements→Blueprint→Work Order→Plan→Execute→Review chain is overkill for a one-file fix; its payoff is on larger, multi-artifact features where traceability matters.
- **Doc/skill drift in arg names.** The script flags are `--work-order-title`/`--work-order-id` (a first attempt with `--title` was rejected) — minor, but the kind of thing that bites an agent following stale instructions.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Typed requirements/ACs, scope-bounded work orders, and a 6-dimension review loop reduce spec drift — structurally, per the installed skills. |
| Speed | − / neutral | Adds front-loaded authoring ceremony; net speed depends on feature size — slower for small tasks, plausibly faster on large traceable ones (unmeasured here). |
| Maintainability | + | Durable, cross-linked artifacts (`.sw-factory/WO-*/`) + ADR-style blueprints favor long-term maintainability. |
| Safety | + | Defensive scaffold scripts (overwrite guard), security-vetted install, and a structured review phase; MIT and local. |
| Cost Efficiency | + | Free/MIT, runs in your existing agent; no platform fee. (Token cost of the heavier loop not measured.) |

## Verdict

**CONDITIONAL**

Adopt the **conventions and scaffolding** when you want 8090's structured, traceable SDLC discipline (typed requirements → blueprints → work orders → scope-bounded execution → multi-dimension review) inside your coding agent, without the commercial platform — it installs cleanly, is MIT, and the scripts genuinely work. **Condition:** the *automated* work-order-execution loop assumes an MCP backend the plugin doesn't ship (empty stub), so out of the box you're adopting a high-quality methodology + scaffolding, not a turnkey autonomous factory; budget for hand-authoring artifacts or standing up your own server. Best fit for larger, multi-artifact features where traceability earns its ceremony; overkill for small fixes. Distinct from the [8090 Software Factory platform](./8090-software-factory.md) eval, which is **DEFER** (proprietary; self-serve now exists at $200/user/mo, so the blocker is budget rather than access).

Compared to neighbors: **BMAD-METHOD** and **spec-kit** are larger, more mature spec-driven frameworks (role-based agile; Specify→Plan→Tasks→Implement) with big communities; `software-factory-plugin` is younger and smaller but carries a sharper *traceability + audit* lineage (it's a commercial product's methodology open-sourced) and a distinctive blueprint-as-written-diagram model. Pick it when the requirement↔blueprint↔work-order linkage is the point.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [software-factory-plugin](https://github.com/8090-inc/software-factory-plugin) | plugin | 8090's AI-native SDLC methodology as installable skills (MIT, ★6) — Requirements/FRD → Blueprints → Work Orders → Implementation Plan → Execute → Review, with scaffolding scripts and an empty MCP stub; `npx skills add`, multi-harness | Coding agents skip requirements/specs/planning and leave no traceable artifacts; want 8090's structured SDLC discipline without the commercial platform | BMAD-METHOD, spec-kit, OpenSpec, ccpm, 8090 Software Factory |
