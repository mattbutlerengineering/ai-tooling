# Evaluation: OpenSpec

**Repo:** [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
**Stars:** 55,646 | **Last updated:** 2026-06-13 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (primary), with Implement (`/opsx:apply`) and Verify (`/opsx:verify`, `openspec validate`)
**Layer:** Process (with a thin Tooling layer — the `openspec` CLI scaffolds/validates/archives)

---

## What it does

Spec-driven development for AI coding assistants — lightweight, agent-agnostic specs that you agree on *before* code is written. The mechanism: `openspec init` (an npm CLI, Node ≥ 20.19) drops an `openspec/` directory into your repo and generates slash commands + skills for whichever assistant you select. The workflow centers on a "change" — a folder under `openspec/changes/<name>/` holding four artifacts: `proposal.md` (why/what), `specs/<capability>/spec.md` (requirements + scenarios), `design.md` (technical approach), and `tasks.md` (an implementation checklist). You drive it from chat: `/opsx:propose <idea>` scaffolds the artifacts, `/opsx:apply` implements the tasks, `/opsx:sync` merges the change's "delta" specs into the durable `openspec/specs/` source of truth, and `/opsx:archive` files the completed change under `changes/archive/`.

The core architectural idea is the **specs / changes split**: `openspec/specs/` describes how the system *currently* behaves (source of truth), while `changes/` holds *proposed deltas* in isolated folders. Spec deltas use a structured format with `## ADDED/MODIFIED/REMOVED Requirements`, each requirement carrying `#### Scenario:` blocks written in WHEN/THEN/AND prose. This delta model is deliberately brownfield-first — you specify *changes* to existing behavior, not just greenfield systems — and lets multiple changes proceed in parallel without colliding, merging cleanly on archive.

OpenSpec positions explicitly against GitHub's Spec Kit ("thorough but heavyweight — rigid phase gates, lots of Markdown, Python setup") and AWS Kiro ("locked into their IDE, Claude-only"). Its philosophy is "fluid not rigid, iterative not waterfall, easy not complex, brownfield-first" — no enforced phase gates; you create artifacts in any order.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection, not hands-on installation. Reviewed the live repo via the GitHub API: README, `docs/concepts.md`, `docs/commands.md`, `docs/supported-tools.md`, `docs/cli.md`, the repo tree, a real example change (`add-global-install-scope`) including its `spec.md` delta format and `tasks.md` checklist, release history, and contributor count. Did not run `npm install -g @fission-ai/openspec` or `openspec init`, so no command outputs below are observed runs — they are quoted from the project's own docs.

```bash
gh api repos/Fission-AI/OpenSpec --jq '{stars,license,description,pushed_at}'
gh api repos/Fission-AI/OpenSpec/readme --jq '.content' | base64 -d
gh api "repos/Fission-AI/OpenSpec/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/Fission-AI/OpenSpec/contents/docs/concepts.md --jq '.content' | base64 -d
gh api repos/Fission-AI/OpenSpec/contents/docs/commands.md --jq '.content' | base64 -d
gh api repos/Fission-AI/OpenSpec/contents/docs/supported-tools.md --jq '.content' | base64 -d
gh api repos/Fission-AI/OpenSpec/contents/docs/cli.md --jq '.content' | base64 -d
gh api repos/Fission-AI/OpenSpec/contents/openspec/changes/add-global-install-scope/specs/cli-init/spec.md --jq '.content' | base64 -d
gh api repos/Fission-AI/OpenSpec/releases --jq '.[0:6][] | {tag,date}'
gh api "repos/Fission-AI/OpenSpec/contributors?per_page=100" --jq 'length'
```

## What worked

- **First-class Claude Code integration, not an afterthought.** `openspec init` generates Claude Code skills at `.claude/skills/openspec-*/SKILL.md` and namespaced commands at `.claude/commands/opsx/<id>.md`. Claude Code is one of 25+ supported tools, and OpenSpec recommends Opus 4.7 (alongside Codex 5.5) for both planning and implementation. This is genuinely agent-agnostic and works with the catalog's primary harness out of the box.
- **The specs/changes delta model is a real idea, not just folder hygiene.** Isolating each change as a folder of deltas (ADDED/MODIFIED/REMOVED requirements) that merge into a durable source-of-truth on archive directly addresses the "requirements live only in chat history" failure mode, and the brownfield delta framing is a meaningful differentiator from greenfield-oriented spec tools.
- **Lighter than Spec Kit by design.** One `npm install -g` + `openspec init`, no Python toolchain, no enforced phase gates. The `core` profile is just five commands (propose/explore/apply/sync/archive); the heavier `new`/`continue`/`ff`/`verify`/`bulk-archive` set is opt-in via `openspec config profile`. This matches the catalog entry's "SDD discipline without heavy four-phase ceremony" claim.
- **Structured, readable spec format.** The example `spec.md` uses `### Requirement:` + `#### Scenario:` with WHEN/THEN/AND prose — human-reviewable and machine-checkable, and the same format an LLM can both author and follow.
- **Healthy maturity signals.** 55.6K stars, MIT, ~60 contributors, regular SemVer npm releases (v1.4.1 in June 2026, six releases in ~5 months), published package `@fission-ai/openspec`, telemetry with documented opt-out, CI, changesets-based release flow. This is a maintained product, not a single-author experiment.

## What didn't work or surprised us

- **"Validation gates" overstates what `validate` does.** `openspec validate` checks *structural* issues in the spec/change Markdown (requirement/scenario shape, format compliance) — it is a linter for the spec documents, not a test runner that executes acceptance criteria against your code. There is a `/opsx:verify` command that asks the agent to "validate implementation matches artifacts," but that is LLM judgment, not a deterministic executable gate. The catalog one-liner's "act as validation gates" framing should be read as *alignment artifacts*, not CI-enforceable gates (contrast architect-loop, whose gates are committed shell commands the architect re-runs).
- **The repo is mid-migration to a new "opsx" workflow.** README leads with `/opsx:propose` and flags "we've rebuilt OpenSpec with a new artifact-guided workflow"; there is a `README_OLD.md` and a `docs/migration-guide.md`. The newer artifact-guided model is sound but still settling, and the coordination-**workspaces** layer is explicitly beta ("external automation… should still treat command behavior, state files, and JSON output as evolving").
- **No enforcement of the discipline.** "Fluid not rigid" is the selling point, but it also means nothing *stops* an agent from skipping specs and writing code — adherence depends on the human and the model following the slash-command workflow. The value is convention + scaffolding, not a hard gate.
- **Best with high-reasoning models + clean context.** The docs recommend Codex 5.5 / Opus 4.7 and call out "context hygiene" (clear context before implementation). On weaker models or a cluttered session the artifact quality degrades — this is a planning aid, and planning quality tracks the model.
- **Not hands-on validated here.** Claims about generated artifact quality and the apply/sync/archive round-trip rest on the docs and example change, not an observed run in this environment.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Forces human/AI alignment on requirements + WHEN/THEN scenarios before code, reducing "vague prompt → wrong build"; `validate` catches malformed specs but does not test code |
| Speed | + / - | Faster on ambiguous/multi-step features (less rework from misunderstanding); pure overhead on trivial changes where a spec folder is ceremony |
| Maintainability | + | Durable `openspec/specs/` source of truth + archived changes give the repo (and future agents) a readable record of intent, countering chat-history-only requirements |
| Safety | neutral | No sandboxing, permissions, or security surface; reduces blast radius only indirectly via review-before-build |
| Cost Efficiency | + / - | Less wasted implementation on misunderstood requirements; but artifact generation itself spends tokens and is recommended on expensive high-reasoning models |

## Verdict

**CONDITIONAL**

Adopt OpenSpec when you do non-trivial, multi-step, or brownfield feature work where pinning requirements before implementation pays for itself — and especially if you want SDD that is genuinely portable across Claude Code, Cursor, Codex, and 20+ other assistants rather than locked to one IDE. It is the lighter, npm-based, brownfield-first alternative to GitHub Spec Kit, and that distinction (delta-based specs, no enforced phase gates, first-class Claude Code skills + commands) justifies keeping it as a separate catalog entry rather than collapsing it into spec-kit. Two caveats temper a full ADOPT: the "validation gates" are structural linting plus LLM verification, not executable CI gates (don't expect architect-loop-style enforcement), and the project is mid-migration to its `opsx` workflow with a beta workspaces layer. Skip it for trivial fixes, throwaway scripts, or solo prompting where the spec folder is pure overhead. Recommend the existing catalog entry stay, with the one-liner softened from "validation gates" to "alignment artifacts / spec layer."

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | framework | Spec-driven development for AI coding assistants — lightweight, agent-agnostic delta specs as a pre-build alignment layer (55.6K stars) | Need SDD discipline without heavy four-phase ceremony, portable across agents and brownfield codebases | spec-kit, BMAD-METHOD, architect-loop |
