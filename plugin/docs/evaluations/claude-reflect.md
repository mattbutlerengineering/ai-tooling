# Evaluation: claude-reflect

**Repo:** [BayramAnnakov/claude-reflect](https://github.com/BayramAnnakov/claude-reflect)
**Stars:** 1069 | **Last updated:** 2026-03-16 | **License:** MIT
**Last verified:** 2026-06-22  <!-- the date you last checked this eval against reality; staleness sweep (audit-evals.py --staleness) flags evals older than their category threshold -->
**Dev loop stage:** Reflect
**Layer:** Process

---

## What it does

Self-learning Claude Code plugin that captures corrections and preferences from your sessions, queues them, and (after human review) syncs the survivors into `CLAUDE.md` / `AGENTS.md` / rule files. Commands: `/reflect`, `/reflect-skills`, `/view-queue`, `/skip-reflect`.

The mechanism, verified in the installed source (`~/.claude/plugins/marketplaces/claude-reflect-marketplace/`, v3.1.0), has two halves. **Capture** is hook-driven: `hooks/hooks.json` wires a `UserPromptSubmit` hook to `scripts/capture_learning.py`, which runs each prompt through `detect_patterns()` in `scripts/lib/reflect_utils.py`. That function matches regex families — `CORRECTION_PATTERNS` (`^no,`, `don't`, `use X not Y`, `that's wrong`), `GUARDRAIL_PATTERNS` (`don't add … unless`, confidence 0.90), explicit `remember:` markers, and CJK parallels — while a `FALSE_POSITIVE_PATTERNS` / `NON_CORRECTION_PHRASES` set suppresses task requests and agreements ("no problem", "can you help"). A hit becomes a queue item (`type`, `message`, `patterns`, `confidence`, `sentiment`, `decay_days`, `timestamp`, `project`) appended to a **per-project** queue at `~/.claude/projects/<encoded-path>/learnings-queue.json` (resolved by `get_queue_path()`). **Application** is the `/reflect` command (`commands/reflect.md`): it loads the queue via `scripts/read_queue.py`, validates/dedupes, routes each learning to the right memory tier (guardrails → `.claude/rules/guardrails.md`, global behavioral → `~/.claude/CLAUDE.md`, project-specific → `./CLAUDE.md`), then **asks the user** (`AskUserQuestion`) before writing. Confidence/decay only prioritize and expire *queued* items; once written to a memory file the entry is permanent. `--dry-run`, `--scan-history`, `--days N`, `--dedupe`, `--organize`, `--targets` are real flags in the command spec.

## How we tested it

**Evidence:** MEASURED

Hands-on against the installed v3.1.0 source on this machine, with a discriminating true-positive/false-positive check on the detection engine plus the upstream test suite as an oracle.

**1. Source verified.** Manifest `version: 3.1.0`, MIT, repo `bayramannakov/claude-reflect`. Confirmed the hook wiring (`hooks/hooks.json`: `UserPromptSubmit → capture_learning.py`, plus `PreCompact`, `PostToolUse:Bash`, `SessionStart` reminders), the queue path logic (`get_queue_path()` → `~/.claude/projects/<encoded>/learnings-queue.json`), and the command spec (`commands/reflect.md` 10-phase, human-review-gated workflow with `AskUserQuestion`).

**2. Upstream test suite (oracle).** Ran the bundled tests — **222 passed, 13 subtests passed in 0.69s** — covering pattern detection, the false-positive guards, queue load/save, the memory-hierarchy router, and tool-error extraction.

**3. Discriminating A/B on the detector.** Drove `detect_patterns()` directly over a balanced should/shouldn't-fire prompt set:

```
FIRED  type=auto      conf=0.85 pat=no, use-X-not-Y   | no, use pnpm not npm
FIRED  type=guardrail conf=0.90 pat=dont-unless-asked | don't add comments unless I ask
FIRED  type=explicit  conf=0.90 pat=remember:         | remember: always run the linter before committing
skip   type=None      conf=0.00                       | can you help me fix this build error?   (task request)
skip   type=None      conf=0.00                       | no problem, go ahead                    (agreement)
FIRED  type=auto      conf=0.80 pat=that's-wrong      | that is wrong, the port is 8080
```

4/4 genuine corrections fired with calibrated confidence; both decoys (a task request and an agreement) were correctly suppressed — the value-add over a naive keyword grep.

**4. Queue round-trip + real on-disk state.** `create_queue_item(...)` produced the documented schema, and `get_queue_path("/tmp/demo-project")` resolved the per-project path. This machine already has **real queue files** from prior sessions under `~/.claude/projects/*/learnings-queue.json` — i.e. the capture hook has been firing in normal use, not just in this eval.

```bash
# from ~/.claude/plugins/marketplaces/claude-reflect-marketplace
python3 -m pytest tests/ -q                 # 222 passed
python3 scripts/read_queue.py               # prints current project's queue as JSON
# detector check
python3 -c 'import sys; sys.path.insert(0,"scripts"); from lib.reflect_utils import detect_patterns; print(detect_patterns("no, use pnpm not npm"))'
```

## What worked

- **False-positive discipline is real.** The `FALSE_POSITIVE_PATTERNS` / `NON_CORRECTION_PHRASES` layer demonstrably suppressed "can you help me fix this" and "no problem" while still catching "no, use X not Y" — the hard part of correction-mining done right, and pinned by the 222-test suite.
- **Human-in-the-loop by design.** `/reflect` never writes silently: the command spec routes through `AskUserQuestion` before editing any memory file, and the queue is the staging area you inspect with `/view-queue`. Matches the "human-reviewed learnings" promise.
- **Per-project isolation.** Queues are keyed by encoded project path, so one repo's corrections don't leak into another's `CLAUDE.md`.
- **Hierarchy-aware routing.** Guardrails go to `.claude/rules/guardrails.md`, global behavioral to `~/.claude/CLAUDE.md`, project-specific to `./CLAUDE.md` — not a single flat dump.

## What didn't work or surprised us

- **`remember:` is greedy.** A real on-disk queue item on this machine was a 2KB automated agent prompt (a "memory observer" system message) that merely contained the substring `remember:` — captured at confidence 0.90 with `type=explicit`. The `MAX_CAPTURE_PROMPT_LENGTH` (500) guard is explicitly bypassed for `remember:`, so long machine-generated prompts from *other* tooling can pollute the queue. The human-review gate catches this before it reaches `CLAUDE.md`, but it adds review noise.
- **No automatic eviction from memory files.** Decay only prunes *queued* items; once a learning is written it is permanent and must be removed by hand (`/reflect --dedupe`/`--organize` help consolidate but you still confirm each).
- **Capture quality is regex-bound at the hook layer.** Semantic validation happens later in `/reflect` (model-driven), but the initial gate is pattern-matching, so paraphrased corrections that don't hit a regex never enter the queue at all.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Captured corrections (e.g. "use X not Y", guardrails) persist into CLAUDE.md so the agent stops repeating mistakes; routing keeps them in the right tier. |
| Speed | neutral | Capture is a fast regex hook (suite runs in 0.69s); `/reflect` is an interactive on-demand pass, not in the hot path. |
| Maintainability | + | Centralizes hard-won project conventions into reviewed memory files instead of tribal knowledge; `--dedupe`/`--organize` fight CLAUDE.md bloat. |
| Safety | + | Nothing is written without explicit `AskUserQuestion` review; per-project queue isolation prevents cross-repo leakage. |
| Cost Efficiency | neutral | Hook capture is near-free; `/reflect` spends model tokens on semantic validation (configurable via `--model haiku/sonnet/opus`). |

## Verdict

**ADOPT**

Installed and validated hands-on (v3.1.0): the bundled 222-test suite passes, the detector cleanly separates real corrections from task-requests/agreements in a discriminating check, and this machine already carries real per-project queue files from normal use. The human-review gate makes the one rough edge — `remember:` over-capturing long machine prompts — a review-noise annoyance rather than a correctness risk. Consistent with the existing **KEEP**: worth keeping installed for the Reflect stage; the standout is its false-positive discipline plus hierarchy-aware, human-confirmed routing into CLAUDE.md.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | plugin | Self-learning system that captures corrections and preferences, syncs to CLAUDE.md | Agent keeps making the same mistakes; doesn't learn from feedback | claude-mem, OMEGA (different focus: learning vs. recall) |
