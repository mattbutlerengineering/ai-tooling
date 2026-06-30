# AI Tooling

Documentation-only repo. No build, test, or deploy commands.

## Purpose

An operating manual for AI-assisted development that produces high-quality code and keeps improving. Inventory and evaluation of AI tools, skills, agents, frameworks, harnesses, workflows, and MCP servers — organized around the dev loop stages where tools intervene and the quality signals they move.

Evaluates tools against five quality signals: Correctness, Speed, Maintainability, Safety, and Cost Efficiency. The workflow has three layers per stage (process, tooling, infrastructure) connected by feedback arcs that make each cycle better than the last.

## Structure

- `CATALOG.md` — flat inventory of 551 tools, organized by 13 categories with overlap markers
- `WORKFLOW.md` — dev loop stages (inner + outer), tools per stage, quality signals, adoption guide
- `STACK.md` — recommended stack (~20 tools to actually install, with commands)
- `STACK-LEDGER.md` — machine-readable record of why each ADOPT/KEEP tool is/isn't in STACK (data foundation for the #70 drift gate)
- `evaluations/` — hands-on tool evaluations following `TEMPLATE.md`
- `methodologies/` — external AI-native SDLC methodologies mapped onto our dev loop + stack (synced to plugin; see ADR-0003)
- `discovery/` — bulk discovery logs (`new-tools-loopN.md`) from scanning sessions
- `skills/` — source skills for reference
- `plugin/` — installable Claude Code marketplace package (skills, docs, hooks)
- `README.md` — repo overview with install instructions

## Catalog format

Each entry is a row in a markdown table with these columns:

| Column | Description |
|--------|-------------|
| Name | Tool name, linked to repo |
| Type | tool / skill / plugin / framework / harness / platform / MCP server / reference |
| One-liner | Plain-language description, ~10-15 words |
| Problem it solves | The specific pain point, ~1 sentence |
| Overlaps with | Other catalog entries that address a similar problem (may also name a notable external tool or installed skill as a conceptual peer) |

## Categories

Code Understanding, Agent Orchestration, Agent Harnesses, Memory & Context,
Skills & Plugins, Code Review & Quality, Maturity Frameworks, Dev Workflow,
MCP Servers, Observability, Research & Discovery, Security & Safety, Reference

## Sources

- GitHub stars: `gh api user/starred --paginate --jq '.[].full_name'`
- Locally installed: `~/.claude/plugins/`, `~/.claude/skills/`, MCP servers in settings.json
- Newsletters: TLDR AI, The Rundown AI, The Neuron, AI Leadership Edge, Practical AI, AI Adopters Club
- Registries: skills.sh, npm (claude-code plugins), GitHub trending (AI topic)

## Skills

- `skills/setup-workflow/` — bootstrap the workflow in any repo (use first time on a new project)
- `skills/evaluate-tool/` — evaluate a new tool against catalog, dev loop stage, and quality signals (use when considering a new tool)
- `skills/audit-workflow/` — audit installed tools against recommended stack (use periodically)
- `skills/update-catalog/` — sync catalog with GitHub stars and local installs (use when catalog may be stale)
- `skills/sync-stars/` — find starred repos not in CATALOG.md and generate entries (use after starring new repos)

## Source of truth

- Root files (`CATALOG.md`, `WORKFLOW.md`, `evaluations/`) are authoritative
- `plugin/docs/` is a synced copy — never edit directly
- `plugin/skills/` is authoritative for skills; `skills/` is derived (paths stripped)
- Run `./sync-plugin-docs.sh` after any root doc or plugin skill change

### Supported harnesses (Claude Code + opencode)

opencode is a supported harness alongside Claude Code. Both read this `CLAUDE.md`
(opencode reads it as its rules fallback — there is intentionally no `AGENTS.md`
content fork). Canonical homes per artifact, with the other harness derived/synced
(ADR-0002; never hand-maintain a duplicate that drifts):

- **Instructions** → `CLAUDE.md` (both harnesses)
- **Repo skills** → `.claude/skills/` + `.agents/skills/` (both harnesses auto-discover; `.claude/skills/find-skills` is a symlink to `.agents/skills/find-skills`)
- **Specialized agent (`eval-runner`)** → `.opencode/agents/` canonical; `.claude/agents/eval-runner.md` is a symlink to it (one source file, zero drift)
- **Hook logic** → opencode plugins in `.opencode/plugins/` (`commit-gate.ts`, `auto-sync.ts`) that call the **same** `audit-evals.py --offline` / `sync-plugin-docs.sh` scripts Claude Code's hooks use — so the local opencode, local Claude Code, and CI (`make check`) gates reference one implementation
- **Deterministic gates** → custom commands `/check` `/fix` `/sync` (opencode) and `make check`/`make fix`/`./sync-plugin-docs.sh` directly

**Lockstep invariant:** any change to a hook behavior must keep the opencode
plugins, the Claude Code `.claude/hooks/` scripts, and `.github/workflows/integrity.yml`
in lockstep — they all gate against the same coupled scripts, so they must not drift.

## Integrity audit

- **`make check` is the canonical gate; `make fix` is the canonical repair.** `make check` runs the full gating set in `--check`/verify mode — exactly what `.github/workflows/integrity.yml` enforces (offline detectors B/D/G/J/K, `--selftest`, `reconcile`/`backfill`/`tier-stack`/`sync-plugin-docs` `--check`, and the network install resolver A) — and exits non-zero on the first failure. `make fix` runs the apply-mode fixers in dependency order (`reconcile-counts` → `backfill-evidence` → `tier-stack` → `sync-plugin-docs`) then re-runs `check`, so a clean exit means the tree is green. CI's `audit` job calls `make check`, so the local and CI gate sets can't drift (pinned by `test_automation.py`'s `TestIntegrityMakefile`). The individual scripts below are still runnable directly when you want one gate in isolation.
- `python3 audit-evals.py` runs the gating detectors (A install, B fabrication, D verdict sync, G comparison consistency, J stack-derivation drift, K verdict evidence) and exits non-zero on any problem (gate it in CI/pre-commit); opt-in detectors C/E/F/I and `--selftest` add more checks:
  - **install resolver** — every install command in `STACK.md`/`CATALOG.md`/`evaluations/` must point at a real artifact (npm/PyPI/crates.io/GitHub). A broken command means the tool was likely never run. (`--installs` only)
  - **fabrication classifier** — each eval's "How we tested" must either disclose it was not run or show a verified hands-on run; a section asserting a specific run with no honesty disclaimer is flagged. (`--fabrication`/`--offline`, no network)
  - **verdict sync** — each eval's `## Verdict` must agree with its `COMPARISON.md` row (tolerates dual verdicts and the KEEP/installed status). (`--verdicts`, offline)
  - **comparison consistency** — `COMPARISON.md`'s per-stage summary must sum to its own body rows and its Total must equal the `CATALOG.md` entry count; catches manual count drift between the two authoritative files. (`--comparison`, offline, gating, on by default)
  - **stack-derivation drift** — `STACK.md` must be derivable from the verdict data + the `STACK-LEDGER.md` exclusion ledger (#64): every ADOPT/KEEP tool is in STACK or has a logged exclusion reason, ledger verdicts match `COMPARISON.md`, and nothing marked in-STACK is actually missing from `STACK.md`. Kills the hand-maintained drift prior audits kept finding (abtop/codeburn, serena, documentation-writer). (`--drift`, offline, gating, on by default)
  - **verdict evidence** — a strong verdict can't rest on a README skim: an ADOPT/KEEP eval must be run-backed (`Evidence` `MEASURED` or `RUN`) **or** carry an explicit honesty disclaimer in its "How we tested" section; a `REVIEW`/`SOURCE-ONLY` ADOPT/KEEP with no disclaimer fails. The escape hatch is the same not-run disclaimer vocabulary the fabrication classifier (B) recognizes (the `HONEST` regex — "source-grounded", "not run hands-on", "did not install", etc.); widen that vocab if it false-flags an honest review. To clear the gate, either graduate the eval to MEASURED/RUN (#68) or add the disclaimer. (`--verdict-evidence`, offline, gating, on by default)
  - **link rot** (opt-in `--links`, ~450 requests) — every `github.com/owner/repo` link in `CATALOG.md` must resolve to its canonical name; flags 404s (dead) and silent renames (moved).
  - **archived repos** (opt-in `--archived`, ~450 `gh api` calls, report-only) — flags catalogued repos GitHub marks `archived` (unmaintained); the entry should carry a ⚠️ archived note or repoint to a successor. Link rot misses these (the link still resolves). Note whether each is already disclosed.
  - **skill evidence** (opt-in `--skills`, report-only) — lists ADOPT-verdict *skill* evals that have a measured eval vs the review-based backlog; a tracked metric, not a gate (see issue #38 and the skill-eval guidance in `TEMPLATE.md`).
  - **dangling overlaps** (opt-in `--overlaps`, report-only) — an "Overlaps with" token naming a tool that isn't itself catalogued is either a deliberate external/conceptual peer (allowed) or a real gap; the more rows cite the same token, the likelier a gap (how `aider`/`continue`/`agenta` were found). Surfaces candidates for human review; not a gate.
  - **staleness sweep** (opt-in `--staleness`, report-only) — flags evals whose `**Last verified:**` date is older than its category threshold (`STALENESS_DAYS`, keyed by Type — fast-moving harnesses/MCP servers/frameworks age in ~120 days, tools/skills/plugins ~180, references ~365; tune in one place). A point-in-time eval rots — a harness can be wrong months after it was written. Evals with no `**Last verified:**` date are reported as a count, not individually. Add the date to `TEMPLATE.md`'s header when you re-check an eval.
  - **token-savings claims** (opt-in `--savings-claims`, report-only) — flags every `CATALOG.md` row whose one-liner makes a numeric token-savings headline (a `%` or `N×` next to token/reduction vocabulary) but whose eval is *not* run-backed (Evidence `MEASURED`/`RUN`). The Optimize cluster carries the loudest savings claims in the catalog (60–95% fewer tokens, 96% reduction, 50× token reduction) on the softest evidence; this turns that unverified backlog into a number to shrink by running the token-savings verification protocol (`evaluations/token-savings-protocol.md`). An in-row `self-reported`/`unverified` disclaimer is bucketed apart as the honest path (like detector B's `HONEST` vocab). A tracked metric, not a gate (mirrors `--skills`); gating it is a later #71-style decision. (`--savings-claims`, offline)
  - **evidence-strength field** (opt-in `--evidence`, report-only) — tallies each eval's declared `**Evidence:**` field (`MEASURED`/`RUN`/`REVIEW`/`SOURCE-ONLY`), recording *how hard we looked* separate from the verdict (*what we concluded*), catalog-wide and within the ADOPT/KEEP set ("what % of ADOPT is MEASURED"). Backfilled across every eval and mirrored as a column in `COMPARISON.md` (#67); gating weak-backed ADOPT/KEEP verdicts is #71. See `TEMPLATE.md` for how to choose a value.
  - **selftest** (`--selftest`, offline) — unit-tests the evidence classifier and the Evaluation parser; exits non-zero on a failing assertion.
- If the classifier false-flags an honest review, widen the `HONEST`/`VERIFIED` vocab in the script; if it misses a fabrication, that's a real problem to fix in the eval, not the script.
- `python3 backfill-evidence.py` populates the `Evidence` field across every eval and regenerates the `Evidence` column in `COMPARISON.md` from those values, so the two never drift. The value is *derived* from each eval's own honesty/measurement signals (the same `Evidence.level` logic detector B uses) — reproducible, not hand-guessed; it never overwrites a field an author set by hand. Run `--check` to gate it in CI (exits non-zero if any eval lacks a field or the column is stale). Catalog rows with no eval file resolve to `SOURCE-ONLY` (no evaluation evidence, only metadata) — a feature that surfaces the missing-eval gap (#68). The Evidence column is appended after `Evaluated`; detector G and `reconcile-counts.py` count rows by their `Tool | Type` prefix, so the trailing column doesn't perturb them (pinned by `test_automation.py`).
- `python3 tier-stack.py` regenerates the **Evidence tiers** block in `STACK.md` (between the `TIERS:START`/`END` markers) from each tool's Evidence value: Tier 1 = measured (`MEASURED`/`RUN`, install with confidence), Tier 2 = review-based (`REVIEW`/`SOURCE-ONLY`, try at your own risk). Derived, not hand-assigned; `--check` gates it in CI. Graduating an eval to MEASURED (#68) promotes a tool to Tier 1 on the next run.
- `python3 -m unittest test_automation` (or `python3 test_automation.py`) runs the characterization tests for the count/sync automation — `reconcile-counts.py`, detector G (`audit_comparison`), detector J (`audit_stack_drift`), `sync-plugin-docs.sh`, the Evidence field/derivation, `backfill-evidence.py`, and `tier-stack.py`. They pin current behavior against temp fixtures (never the real files) so the shared-parser refactor (#45) has a regression net; exits non-zero on failure (gate it alongside `audit-evals.py`).

## Agent skills

### Issue tracker

GitHub Issues on `mattbutlerengineering/ai-tooling`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout. See `docs/agents/domain.md`.

## Adding entries

- Use the `/add-catalog-entry` skill (`.claude/skills/add-catalog-entry/`) — it runs the full 8-file workflow (resolve slug, dedup, insert CATALOG + COMPARISON rows, propagate counts, sync, audit).
- Fetch repo description: `gh api repos/{owner}/{repo} --jq '.description'`
- Place in the correct category table
- Always fill the "Overlaps with" column — check existing entries in the same category
- If a new category is needed, add a section header with a one-line description
- **Never hand-edit counts.** Run `python3 reconcile-counts.py` to propagate the catalog total across README/CLAUDE/STACK/plugin and rebuild COMPARISON's summary from its body rows (`--check` for a dry-run / CI gate). Detector G then verifies CATALOG == COMPARISON.

## Evaluations

- **Hands-on evaluations** use `evaluations/TEMPLATE.md` — copy it and fill every section with evidence from actual usage. The "How we tested it" section is mandatory; README-only evaluations are discovery logs, not evaluations.
- **Discovery logs** (`evaluations/new-tools-loopN.md`) are for bulk triage — one-liner verdicts from scanning repos. They feed the catalog but don't constitute a full evaluation.
- Use inner/outer loop vocabulary (Plan, Implement, Verify, Review, Ship, Reflect), not ACMM levels.
