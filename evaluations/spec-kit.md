# Evaluation: spec-kit

**Repo:** [github/spec-kit](https://github.com/github/spec-kit)
**Stars:** 130,961 | **Last updated:** 2026-08-21 (release v1.0.1, 2026-08-21) | **License:** MIT
**Last verified:** 2026-08-23
**Dev loop stage:** Plan (primary); spans Implement and Review via `speckit implement` and `speckit analyze`
**Layer:** Process

---

## What it does

GitHub's Spec-Driven Development toolkit — Specify→Plan→Tasks→Implement, each with a human checkpoint. The thesis (from `docs/concepts/sdd.md`) is that "specifications become executable, directly generating working implementations rather than just guiding them" — the spec is the durable artifact and code is the build output, inverting the usual relationship where specs are discarded once coding starts.

The mechanism is a Python CLI (`specify`, run via `uvx`/`uv tool install`) plus a set of agent commands. `specify init <project> --integration claude` scaffolds a `.specify/` directory (templates, scripts, `memory/constitution.md`, and — new since the last review — `workflows/`) and writes the agent artifacts into that agent's own directory. The workflow is a fixed sequence of prompts, each producing a markdown artifact in `specs/<feature>/`:

1. **`speckit constitution`** — writes `.specify/memory/constitution.md`, the project's governing principles.
2. **`speckit specify`** — writes `spec.md`: user stories prioritized P1/P2/P3, each "independently testable," with Given/When/Then acceptance scenarios. Deliberately tech-stack-free (the "what/why").
3. **`speckit plan`** — writes `plan.md`: the tech stack and architecture (the "how").
4. **`speckit tasks`** — writes `tasks.md`: an actionable, ordered task list derived from the plan.
5. **`speckit implement`** — executes the tasks to build the feature.

Optional commands add quality gates: **`clarify`** (interrogate underspecified areas before planning), **`analyze`** (a *read-only* cross-artifact consistency check across spec/plan/tasks), **`checklist`** ("unit tests for English"), and — both new since the last review — **`converge`** ("assess the codebase and append remaining work as tasks", the brownfield entry point) and **`taskstoissues`**. A backing bash/PowerShell script layer handles branch creation and file scaffolding deterministically rather than leaving it to the model.

**The invocation name is integration-specific, so this doc names the commands without a separator.** The scaffolder writes an `invoke_separator` per integration: Claude Code gets `-` (`/speckit-plan`) and opencode gets `.` (`/speckit.plan`). The `/speckit.*` form the previous review quoted throughout is opencode's, not Claude Code's — see the run below.

Important nuance on "executable specs": despite the marketing framing, the specs are **durable markdown documents, not machine-enforced validation gates**. `analyze` is explicitly "STRICTLY READ-ONLY … Output a structured analysis report" and only *offers* a remediation plan; the constitution is described as "non-negotiable" but enforcement is the model honoring an instruction, not a failing build. The real gating is (a) the human checkpoint between phases and (b) the LLM cross-checking artifacts against each other.

## How we tested it

**Evidence:** RUN

Scaffolded real projects with the live CLI and inventoried what it writes. **No LLM key is needed for any of this** — `specify init` is deterministic scaffolding, which is what makes spec-kit measurable on a machine with no model credentials. The Specify→Plan→Tasks→Implement *loop itself* was **not** run (that needs an agent session per phase), so nothing below claims anything about generated-code quality; the claims are about the toolkit's structure, its per-harness output, and its multi-integration behaviour.

**Version under test: `specify 1.0.2.dev0`** (git `main`), against release **v1.0.1** (2026-08-21).

```bash
uvx --from git+https://github.com/github/spec-kit.git specify --version   # 1.0.2.dev0
uvx --from git+…                                specify check            # 39 integrations
uvx --from git+…  specify init demo-claude   --integration claude   --script sh --non-interactive
uvx --from git+…  specify init demo-opencode --integration opencode --script sh --non-interactive
diff -rq demo-claude/.specify demo-opencode/.specify
cd demo-claude && uvx --from git+… specify integration install opencode          # refused
cd demo-claude && uvx --from git+… specify integration install opencode --force  # accepted
```

**1. It has shipped 1.0.** The previous review's "pre-1.0 and self-described experimental … Version v0.11.2" is out of date: **v1.0.1** released 2026-08-21, and the CLI surface has grown from `init/check/version/self/extension` to also include `integration`, `event`, `preset`, `bundle` and `workflow`.

**2. The Claude Code integration really is skills-based.** `specify init --integration claude` writes **10 skills** to `.claude/skills/speckit-*/SKILL.md`, each with `name`, `argument-hint`, `user-invocable` and `disable-model-invocation` frontmatter. The previous review asserted this from the integrations doc; it is confirmed by the files on disk. 39 integrations are offered, and `specify check` detects Claude Code, **opencode**, Codex CLI, Antigravity, Oh My Pi and VS Code as available on this machine.

**3. The two harnesses get materially different artifacts — not one file in two places.** Same project, same version, `--integration opencode` instead:

| | Claude Code | opencode |
|---|---|---|
| Location | `.claude/skills/speckit-*/SKILL.md` | `.opencode/commands/speckit.*.md` |
| Kind | 10 skills (directory per skill) | 10 commands (flat `.md`) |
| Invoke | `/speckit-specify` | `/speckit.specify` |
| Extra | — | a **`handoffs:`** block chaining each command to the next agent |

The opencode form carries an agent-handoff graph the Claude skill form has no equivalent for. `.specify/` itself also differs between the two inits — `plan-template.md`, `tasks-template.md`, `checklist-template.md`, `check-prerequisites.sh` and `setup-tasks.sh` all differ, in every case *only* by the substituted separator.

**4. Multi-harness is possible, refused by default, and leaves the shared layer wrong.** This is the finding that matters for a repo like this one. `specify integration install opencode` into a Claude project is **refused**:

> Installing multiple integrations is only automatic when all involved integrations are declared multi-install safe.

With `--force` it succeeds — both surfaces exist (10 skills **and** 10 commands) and `integration.json` records both separators. But the **shared** `.specify/` layer still bakes only the default integration's:

```
plan-template.md      : 7 hyphen / 0 dot
check-prerequisites.sh: 3 hyphen / 0 dot
```

So an opencode user in that project — whose commands are `/speckit.plan` — reads template notes and hits script error messages instructing them to *"Run `/speckit-plan` first"*, a command their harness does not have. spec-kit says so itself, printing the shared files it declined to refresh and pointing at `specify init --here --force` / `integration upgrade --force` — which would flip the separator and break the Claude side instead.

## Test design

- **Task/corpus:** three scratch projects — `--integration claude`, `--integration opencode`, and a claude project with opencode force-installed on top.
- **Baseline:** the previous `REVIEW` eval's own written claims (skills-based Claude integration, `/speckit.*` command names, pre-1.0 status, `.specify/` contents) — the run was designed so each could be refuted.
- **Metric:** file inventory (`find`), cross-integration `diff -rq`, separator counts by grep, and the CLI's own accept/refuse behaviour on multi-install.
- **Reproduce:** the command block above; nothing needs an API key.
- **Not measured:** generated-code quality, constitution adherence during `implement`, token cost per feature, and brownfield artifact drift — all require agent sessions per phase.

## What worked

- **Deterministic scaffolding, verified.** 30 files, sub-second, no model call, no API key. The structural mechanics are reproducible exactly as claimed — which is also why this eval could reach `RUN` at all.
- **It is 1.0 now, and GitHub-official.** 131K stars, MIT, a release two days before this check, and a substantially wider CLI (`workflow`, `preset`, `bundle`, `event`, `integration`).
- **39 integrations, and the two that matter here both work.** Claude Code and opencode are each first-class, each with an idiomatic artifact form rather than a lowest-common-denominator one.
- **`--non-interactive` exists and is documented for agents.** Its own help text reads *"Required for agent harnesses that allocate a PTY but cannot send arrow-key input"* — someone thought about being driven by an agent, not just by a human.
- **Attacks the #1 failure mode head-on.** Separating *what/why* (`specify`, tech-stack-free) from *how* (`plan`) forces the misalignment conversation onto a cheap markdown artifact before any code is written, with real human checkpoints between four discrete artifacts.
- **`analyze` + constitution add a consistency layer most SDD tools lack**, and `converge` (new) is a real brownfield entry point the earlier review predates.

## What didn't work or surprised us

- **The dual-harness story is broken in the shared layer** — measured above. Refused without `--force`; with it, `.specify/` templates and scripts name one harness's commands at the other harness's users. For a repo whose premise is *one source file, zero drift across both harnesses* (this repo's ADR-0002), that is a direct conflict, and there is no setting that fixes it — the separator is a project-wide default.
- **"Executable specifications" is aspirational, not literal.** The artifacts are markdown and the strongest gate (`analyze`) is explicitly read-only and advisory. Don't adopt expecting a failing build when code violates the spec.
- **Heavy ceremony.** Constitution → specify → (clarify) → plan → (analyze/checklist) → tasks → implement is pure overhead for a bug fix. The value materializes on greenfield or genuinely PR-sized features.
- **The command surface churns, and the previous review's naming is already stale.** `/quizme`→`clarify`, dotted→hyphenated for Claude, plus two commands (`converge`, `taskstoissues`) that did not exist at the last look. Any doc that quotes `/speckit.*` literally is quoting one integration's form.
- **External toolchain dependency.** `uv`/pipx, Python 3.11+ and Git just to scaffold — more setup than a drop-in skill, and a real dependency to keep upgraded.
- **Still unvalidated: the part that produces code.** Generated-code quality, constitution adherence during `implement`, and token cost per feature were not measured here and remain read-from-the-templates claims.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Separating what/why from how, plus `analyze` cross-artifact consistency and a constitution authority, catches misalignment before code exists — not measured here |
| Speed | + (greenfield/large) / - (small) | Scaffolding is sub-second; the four-phase ceremony is slower than a single prompt for small changes |
| Maintainability | + / - | spec.md/plan.md/tasks.md/constitution.md are durable reviewable artifacts; but on a dual-harness repo the shared `.specify/` layer is measurably wrong for one of the two harnesses |
| Safety | neutral/+ | Human checkpoints and a read-only analyze pass add review gates; no sandboxing or machine-enforced contracts |
| Cost Efficiency | - | Multiple LLM passes per feature; justified only when rework avoided exceeds the overhead. Scaffolding itself costs nothing |
| Verifiability | + | `init` output is a deterministic file tree, so what the tool installs is inspectable and diffable without running a model — which is how every claim above was checked |

## Verdict

**CONDITIONAL** — adopt-if: you are starting **greenfield or a PR-sized feature** where misalignment is the expensive failure, **and** the repo runs a **single agent harness**.

The single-harness half of that gate is measured, not stylistic: with two integrations installed, `.specify/`'s templates and scripts name the default integration's commands at the other integration's users, and spec-kit refuses the configuration without `--force` for exactly that reason. A repo that runs both Claude Code and opencode off one source of truth would be adopting a tool that cannot hold that invariant.

Skip it for bug fixes, small changes, and exploratory work, where the four-phase ceremony costs more than it saves. Within the SDD trio, choose spec-kit when you want GitHub-official polish and the broadest agent support; choose **OpenSpec** for lighter, more portable specs; choose **BMAD-METHOD** for role-based agents rather than a phase pipeline. For a user already running **GSD** — a STACK pick that provides its own milestone/phase/plan/execute/verify loop — spec-kit is largely redundant, and adopting it means running two competing process frameworks.

This replaces a `discovery-log — tentative read` written from source. The run corrected three of its facts (pre-1.0 → 1.0.1; `/speckit.*` is opencode's naming, not Claude's; the command set has grown) and added the dual-harness finding, which no amount of reading the templates would have surfaced.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [spec-kit](https://github.com/github/spec-kit) | framework | GitHub's Spec-Driven Development toolkit — Specify→Plan→Tasks→Implement, each with a human checkpoint (131K stars) | "Prompt and pray" yields misaligned code; make the spec the durable artifact and code the build output | OpenSpec, BMAD-METHOD, GSD |
