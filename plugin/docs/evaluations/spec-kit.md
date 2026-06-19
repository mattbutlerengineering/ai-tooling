# Evaluation: spec-kit

**Repo:** [github/spec-kit](https://github.com/github/spec-kit)
**Stars:** 114,078 | **Last updated:** 2026-06-19 (release v0.11.2, 2026-06-18) | **License:** MIT
**Dev loop stage:** Plan (primary); spans Implement and Review via `/speckit.implement` and `/speckit.analyze`
**Layer:** Process

---

## What it does

GitHub's Spec-Driven Development toolkit — Specify→Plan→Tasks→Implement, each with a human checkpoint. The thesis (from `docs/concepts/sdd.md`) is that "specifications become executable, directly generating working implementations rather than just guiding them" — the spec is the durable artifact and code is the build output, inverting the usual relationship where specs are discarded once coding starts.

The mechanism is a Python CLI (`specify`, installed via `uv tool install`) plus a set of agent slash commands. `specify init <project> --integration claude` scaffolds a `.specify/` directory (templates, scripts, `memory/constitution.md`) and writes the command files into the agent's directory. The workflow is a fixed sequence of prompts, each producing a markdown artifact in `specs/<feature>/`:

1. **`/speckit.constitution`** — writes `.specify/memory/constitution.md`, the project's governing principles.
2. **`/speckit.specify`** — writes `spec.md`: user stories prioritized P1/P2/P3, each "independently testable," with Given/When/Then acceptance scenarios. Deliberately tech-stack-free (the "what/why").
3. **`/speckit.plan`** — writes `plan.md`: the tech stack and architecture (the "how").
4. **`/speckit.tasks`** — writes `tasks.md`: an actionable, ordered task list derived from the plan.
5. **`/speckit.implement`** — executes the tasks to build the feature.

Optional commands add quality gates: **`/speckit.clarify`** (interrogate underspecified areas before planning), **`/speckit.analyze`** (a *read-only* cross-artifact consistency check across spec/plan/tasks, run before implement), and **`/speckit.checklist`** ("unit tests for English" — requirements completeness checks). Each phase is a human checkpoint: you review and edit the markdown before invoking the next command. A backing bash/PowerShell script layer (`scripts/bash/create-new-feature.sh`, `setup-plan.sh`, etc.) handles branch creation and file scaffolding deterministically rather than leaving it to the model.

Important nuance on "executable specs": despite the marketing framing, the specs are **durable markdown documents, not machine-enforced validation gates**. `/speckit.analyze` is explicitly "STRICTLY READ-ONLY … Output a structured analysis report" and only *offers* a remediation plan; the constitution is described as "non-negotiable" but enforcement is the model honoring an instruction, not a failing build. The real gating is (a) the human checkpoint between phases and (b) the LLM cross-checking artifacts against each other. This is closer to "the spec is the source of truth the agent must reconcile against" than to executable contracts.

## How we tested it

Source-grounded inspection, not hands-on installation. I read the repo metadata, the full README and `docs/concepts/sdd.md`, the integrations reference, the core command templates (`templates/commands/specify.md`, `plan.md`, `tasks.md`, `implement.md`, `analyze.md`), the `spec-template.md`, and the CLI/integration source tree (`src/specify_cli/integrations/claude/`). I did not run `specify init` or execute a full Specify→Plan→Tasks→Implement loop against a real project, so I have no first-hand output on generated-code quality or merge rates. The mechanics described above are read directly from the command templates and scripts, which are the load-bearing artifacts.

```bash
gh api repos/github/spec-kit --jq '{stars,license,description,pushed_at,forks,open_issues}'
gh api repos/github/spec-kit/readme --jq '.content' | base64 -d
gh api "repos/github/spec-kit/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/github/spec-kit/contents/docs/reference/integrations.md --jq '.content' | base64 -d
gh api repos/github/spec-kit/contents/docs/concepts/sdd.md --jq '.content' | base64 -d
gh api repos/github/spec-kit/contents/templates/commands/analyze.md --jq '.content' | base64 -d
gh api repos/github/spec-kit/contents/templates/spec-template.md --jq '.content' | base64 -d
gh api repos/github/spec-kit/releases --jq '.[0:3]'
gh api repos/github/spec-kit/contributors --jq 'length'   # 30
```

## What worked

- **First-class Claude Code support — not just agent-agnostic.** The integrations table lists Claude Code with a dedicated skills-based integration that installs into `.claude/skills`, and there is a `src/specify_cli/integrations/claude/` module. Spec Kit supports 30+ agents (Copilot, Cursor, Gemini, Codex, etc.), but Claude Code is a maintained target, invoked as `/speckit.*` slash commands. This directly answers the "does it work with Claude Code specifically?" question: yes, natively.
- **Attacks the #1 failure mode head-on.** The whole design exists to kill "prompt and pray." Separating *what/why* (`specify`, tech-stack-free) from *how* (`plan`) forces the misalignment conversation to happen on a cheap markdown artifact before any code is written. The P1/P2/P3 "independently testable" user-story structure in `spec-template.md` pushes toward MVP-sliceable specs rather than a monolithic dump.
- **Human checkpoints are the point, and they're real.** Four discrete artifacts with review-and-edit gates between them is exactly the antidote to one-shot generation. You can correct course at the spec layer (seconds of reading) instead of at the diff layer (minutes of review of wrong code).
- **`/speckit.analyze` + constitution add a consistency layer most SDD tools lack.** A dedicated read-only pass that cross-checks spec↔plan↔tasks for contradictions, plus a constitution treated as CRITICAL-priority authority, is genuinely more rigorous than "write a spec then code." It catches drift between the three artifacts before implement.
- **Deterministic scaffolding via scripts, not vibes.** Branch creation, feature-directory setup, and prerequisite checks run through committed bash/PowerShell scripts, so the structural mechanics are reproducible and not subject to model whim.
- **Top-tier maturity signals.** GitHub-official, 114K stars, MIT, 30 contributors, ~10K forks, a release the day before this eval (v0.11.2), and an extension/preset ecosystem. Abandonment risk is near zero — unusual for the SDD category.

## What didn't work or surprised us

- **"Executable specifications" is aspirational, not literal.** The headline framing implies specs are enforced contracts. In practice the artifacts are markdown and the strongest gate (`/speckit.analyze`) is explicitly read-only and advisory. OpenSpec's catalog entry calls its specs "validation gates"; spec-kit's are closer to durable source-of-truth docs the agent reconciles against. Don't adopt it expecting a failing build when code violates the spec.
- **Heavy four-phase ceremony.** Constitution → specify → (clarify) → plan → (analyze/checklist) → tasks → implement is a lot of process. For a bug fix or a small feature this is pure overhead — the artifacts cost more to produce and review than the change is worth. The value materializes on greenfield or genuinely PR-sized features where misalignment is expensive.
- **Pre-1.0 and self-described experimental.** Version v0.11.2 and an "Experimental Goals" section in the README. Command names have already churned (`/quizme`→`/speckit.clarify`, dotted→hyphenated skill dirs for some agents), so the workflow surface is still moving.
- **External toolchain dependency.** Requires `uv` (or pipx), Python 3.11+, and Git just to scaffold — more setup than a drop-in skill. The CLI is a real dependency to install and keep upgraded (`specify self upgrade`), unlike a single `SKILL.md`.
- **Not hands-on validated here.** Claims about generated-code quality, how well the agent honors the constitution during `/speckit.implement`, and whether the artifacts stay in sync during brownfield evolution rest on reading the templates, not on an observed run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Separating what/why from how plus `/speckit.analyze` cross-artifact consistency and a constitution authority catch misalignment before code exists — the dominant defect source |
| Speed | + (greenfield/large) / - (small) | Front-loads alignment so big features avoid expensive rework; four-phase ceremony makes it slower than a single prompt for bug fixes and small changes |
| Maintainability | + | spec.md/plan.md/tasks.md/constitution.md are durable, reviewable artifacts that persist intent in the repo rather than in throwaway prompts |
| Safety | neutral/+ | Human checkpoints between phases and the read-only analyze pass add review gates; but no sandboxing or machine-enforced contracts — gating relies on the human and the model honoring instructions |
| Cost Efficiency | - | Multiple LLM passes per feature (constitution, specify, plan, tasks, optional clarify/analyze/checklist, implement) burn more tokens than direct prompting; justified only when rework avoided exceeds the overhead |

## Verdict

**CONDITIONAL**

Adopt for greenfield projects and substantial, PR-sized features where misalignment is the expensive failure — the Specify→Plan→Tasks→Implement sequence with human checkpoints is a disciplined, well-maintained answer to "prompt and pray," and Claude Code is a first-class integration. Skip it for bug fixes, small changes, and exploratory work, where the four-phase ceremony costs more than it saves. Two caveats temper the enthusiasm: the "executable specs" framing oversells what is really durable-markdown-plus-advisory-checks (not enforced gates), and it's still pre-1.0 with churning command names. Within the SDD trio, choose spec-kit when you want GitHub-official polish, the broadest agent support, and the heaviest process; choose **OpenSpec** when you want lighter, more portable specs that act as validation gates without the four-phase ceremony; choose **BMAD-METHOD** when you want role-based agents (analyst/PM/architect/dev) rather than a phase pipeline. For a user already running **GSD** (milestones/phases/planning/execution/verification with its own agents), spec-kit is largely redundant — GSD already provides the structured plan→execute→verify loop, so adding spec-kit would mean running two competing process frameworks; prefer it only if you specifically want the GitHub-standard SDD artifacts or cross-agent portability GSD doesn't offer.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [spec-kit](https://github.com/github/spec-kit) | framework | GitHub's Spec-Driven Development toolkit — Specify→Plan→Tasks→Implement, each with a human checkpoint (114K stars) | "Prompt and pray" yields misaligned code; make the spec the durable artifact and code the build output | OpenSpec, BMAD-METHOD, GSD |
