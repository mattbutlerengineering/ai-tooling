# Evaluation: OpenSpec

**Repo:** [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
**Stars:** 63,815 | **Last updated:** 2026-08-05 | **License:** MIT
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Plan (primary), with Implement (`/opsx:apply`) and Verify (`/opsx:verify`, `openspec validate`)
**Layer:** Process (with a thin Tooling layer — the `openspec` CLI scaffolds/validates/archives)

---

## What it does

Spec-driven development for AI coding assistants — lightweight, agent-agnostic specs that you agree on *before* code is written. The mechanism: `openspec init` (an npm CLI, Node ≥ 20.19) drops an `openspec/` directory into your repo and generates slash commands + skills for whichever assistant you select. The workflow centers on a "change" — a folder under `openspec/changes/<name>/` holding four artifacts: `proposal.md` (why/what), `specs/<capability>/spec.md` (requirements + scenarios), `design.md` (technical approach), and `tasks.md` (an implementation checklist). You drive it from chat: `/opsx:propose <idea>` scaffolds the artifacts, `/opsx:apply` implements the tasks, `/opsx:sync` merges the change's "delta" specs into the durable `openspec/specs/` source of truth, and `/opsx:archive` files the completed change under `changes/archive/`.

The core architectural idea is the **specs / changes split**: `openspec/specs/` describes how the system *currently* behaves (source of truth), while `changes/` holds *proposed deltas* in isolated folders. Spec deltas use a structured format with `## ADDED/MODIFIED/REMOVED Requirements`, each requirement carrying `#### Scenario:` blocks written in WHEN/THEN/AND prose. This delta model is deliberately brownfield-first — you specify *changes* to existing behavior, not just greenfield systems — and lets multiple changes proceed in parallel without colliding, merging cleanly on archive.

OpenSpec positions explicitly against GitHub's Spec Kit ("thorough but heavyweight — rigid phase gates, lots of Markdown, Python setup") and AWS Kiro ("locked into their IDE, Claude-only"). Its philosophy is "fluid not rigid, iterative not waterfall, easy not complex, brownfield-first" — no enforced phase gates; you create artifacts in any order.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed `@fission-ai/openspec` 1.14.3 from npm into a scratch prefix, ran `openspec init --tools claude` in an empty git repo, then built a fixed fixture of eight change folders (one clean control, seven each carrying one planted defect) and ran `openspec validate <change> --strict`, `openspec validate --all --strict` and `openspec archive --yes` against them. The baseline arm is markdownlint-cli 0.41.0 (default rules, `MD013`/`MD041` off) over the same files, which is what a repo has for Markdown specs without OpenSpec. Telemetry was disabled (`OPENSPEC_TELEMETRY=0`, `DO_NOT_TRACK=1`).

```
$ npm install --prefix /tmp/eval-openspec/npm @fission-ai/openspec     # 3.8s wall
$ openspec --version
1.14.3
$ openspec init --tools claude --force                                   # 0.29s wall
Created: Claude Code
6 skills and 6 commands in .claude/
Config: openspec/config.yaml (schema: spec-driven)

$ openspec validate c1-clean --strict            -> valid                          rc=0
$ openspec validate c2-no-scenario --strict      -> ERROR no scenario              rc=1
$ openspec validate c3-no-shall --strict         -> WARNING no SHALL/MUST          rc=1  (non-strict: rc=0)
$ openspec validate c4-modified-missing --strict -> valid + INFO "Archive would refuse this delta"   rc=0
$ openspec validate c5-no-deltas --strict        -> ERROR no deltas                rc=1
$ openspec validate c6-dup-req --strict          -> ERROR duplicate requirement    rc=1
$ openspec validate c7-bad-scenario-level --strict -> ERROR no scenario (+INFO "### Scenario" ignored)  rc=1
$ openspec validate c8-no-why --strict           -> valid                          rc=0

$ openspec archive c4-modified-missing --yes
auth: target spec does not exist; only ADDED requirements are allowed for new specs.
Aborted. No files were changed.                                                    rc=1
$ openspec archive c2-no-scenario --yes   -> "Validation failed"                   rc=1
$ openspec archive c1-clean --yes
Applying changes to openspec/specs/auth/spec.md:  + 1 added
Totals: + 1, ~ 0, - 0, → 0
Change 'c1-clean' archived as '2026-10-18-c1-clean'.                               rc=0
$ openspec archive c4-modified-missing --yes     (auth spec now exists)
auth MODIFIED failed for header "### Requirement: Password rotation" - not found
Aborted. No files were changed.                                                    rc=1
```

Result: the control passes; of the seven planted-defect changes, `validate --strict` fails five (c2, c3, c5, c6, c7), `archive` refuses a sixth (c4), and one (c8, proposal missing its "Why" section) is accepted. markdownlint over the same files returns formatting rules only (`MD022`, `MD032`, plus `MD024` on c6's repeated heading) and no rule that names a missing scenario, a missing SHALL, a missing delta or a MODIFIED target absent from the main spec. Three consecutive `validate --all --strict` runs over the eight changes took 0.91s total.

## Test design

- **Task/corpus:** eight change folders under `openspec/changes/` in a fresh `openspec init` repo, all with one `auth` capability delta: `c1-clean` (control); `c2-no-scenario` (requirement without a `#### Scenario:`); `c3-no-shall` (requirement text without SHALL/MUST); `c4-modified-missing` (MODIFIED a requirement that exists in no main spec); `c5-no-deltas` (proposal only); `c6-dup-req` (same requirement name twice in ADDED); `c7-bad-scenario-level` (scenario written as `###` not `####`); `c8-no-why` (proposal without a "Why" section).
- **Baseline:** markdownlint-cli 0.41.0 over each change's `proposal.md` and `specs/auth/spec.md`, using a config with `MD013` and `MD041` off.
- **Metric:** count of planted-defect changes the tool turns into a non-zero exit (k/7), false positives on the control (k/1), and whether the archive step merges deltas into `openspec/specs/` correctly.
- **Reproduce:** `npm install --prefix /tmp/x @fission-ai/openspec`, `openspec init --tools claude`, recreate the eight folders as described above, then `openspec validate <name> --strict` and `openspec archive <name> --yes`. The CLI sections of the run are deterministic.

## What worked

- **Detects 6 of 7 planted structural defects, 0 of 1 false positive on the control.** Five by `validate --strict`, one more by `archive` refusing (c4). That is the "validation gate" claim in its structural sense, now measured.
- **Archive is a real gate and atomic.** Both failing archives printed `Aborted. No files were changed.`; the clean archive created `openspec/specs/auth/spec.md` with the requirement and its scenario, and moved the change to `changes/archive/2026-10-18-c1-clean/`.
- **Error messages name the fix.** c5's message tells you to add delta headers or set `skip_specs: true`; c7's INFO says exactly why the `###` header is ignored.
- **Cheap to install and fast.** One npm install (3.8s), no Python, init writes 6 skills plus 6 commands under `.claude/` in 0.29s, and the Claude Code skills land at `.claude/skills/openspec-*/SKILL.md`.
- **Prior review claims about the delta model held in practice**: ADDED merges into the durable spec on archive, and MODIFIED against a missing requirement is refused rather than silently ignored.

## What didn't work or surprised us

- **The agent-driven half of the workflow was exercised only as files.** `/opsx:propose`, `/opsx:apply` and `/opsx:verify` need a model session and no credentials were available, so whether the generated proposals and tasks are good is unmeasured. Everything above is the deterministic CLI layer.
- **A missing SHALL/MUST is only a WARNING.** Plain `validate` returns rc=0 on c3; only `--strict` turns it into a failure, so a CI gate must pass `--strict`.
- **`validate` accepts c4, a change that `archive` will refuse.** The problem shows up as an INFO line, rc=0, and only at archive time does it fail. Gating CI on `validate` alone would let it through.
- **c8 (no "Why" in the proposal) passes.** Proposal structure is not checked by `validate`, so the proposal half of the change is convention only.
- **Archive writes a placeholder Purpose** (`TBD - created by archiving change c1-clean`), and `validate --all --strict` then fails the new `auth` spec with a Purpose-placeholder warning until a human edits it.
- **A comparison with other spec tools was not run.** Spec Kit and BMAD were not installed here, so "lighter than Spec Kit" remains the project's own claim and this baseline is a generic Markdown linter, a weak adversary for a spec validator.
- **Fixture is small and author-written.** Seven defects of one capability, picked by us from the validator's documented rules, so the 6/7 figure shows the checks exist and fire; it is not a defect-detection rate on real specs.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Measured: 6 of 7 planted structural defects blocked by `validate --strict` or `archive`, control passes; says nothing about whether specs are right, only well-formed |
| Speed | neutral | CLI is fast (0.3s init, ~0.3s per validate-all) but the spec/proposal/design/tasks artifacts are overhead on small changes; agent-side time not measured |
| Maintainability | + | Archive merges deltas into a durable `openspec/specs/` tree and keeps dated change history, observed in the run |
| Safety | neutral | No sandboxing or permission surface; the archive abort left no partial writes in both refusals |
| Cost Efficiency | neutral | CLI costs nothing; the model tokens spent generating artifacts were not measured |
| Verifiability | + | A deterministic `validate --strict` exit code lets a human or CI confirm spec shape at the rate changes are produced; semantic correctness still needs a reader |

## Verdict

**discovery-log — measured; promotion candidate** — the CLI layer measurably does its stated structural job (6 of 7 planted defects blocked, 0 false positives, atomic archive) and would read CONDITIONAL on human confirmation, with the condition "adopt if the team does non-trivial or brownfield feature work and CI runs `openspec validate --all --strict`"; the agent-driven proposal quality and comparison with spec-kit were not measured.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | framework | Spec-driven development for AI coding assistants — lightweight, agent-agnostic spec/alignment layer (specs/changes split, brownfield deltas) (55.6K stars) | Need SDD discipline without heavy four-phase ceremony, portable across agents | spec-kit, BMAD-METHOD, architect-loop |
