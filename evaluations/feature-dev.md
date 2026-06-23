# Evaluation: feature-dev

**Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
**Stars:** 30,653 | **Last updated:** 2026-06-23 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- the date you last checked this eval against reality; staleness sweep (audit-evals.py --staleness) flags evals older than their category threshold -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A Claude Code plugin for guided feature development with codebase-understanding and architecture-focused subagents (code-architect, code-explorer, code-reviewer) plus a `/feature-dev` command.

The plugin ships from Anthropic's official marketplace (`anthropics/claude-plugins-official`, installed locally under `~/.claude/plugins/repos/claude-plugins-official/plugins/feature-dev`). It contributes one slash command and three specialized subagents. Invoking `/feature-dev [feature description]` drives a fixed 7-phase workflow: (1) Discovery, (2) Codebase Exploration, (3) Clarifying Questions, (4) Architecture Design, (5) Implementation, (6) Quality Review, (7) Summary. The orchestrating command fans out work to the subagents — it launches 2-3 `code-explorer` agents in parallel to trace existing code, 2-3 `code-architect` agents in parallel to propose competing implementation approaches (minimal-change vs clean-architecture vs pragmatic-balance), and 3 `code-reviewer` agents in parallel at the end. Critically, the command imposes two hard human-in-the-loop gates: it must present clarifying questions and *wait for answers* before designing (Phase 3, marked `**CRITICAL**: ... DO NOT SKIP`), and it must not implement without explicit user approval (Phase 5, `DO NOT START WITHOUT USER APPROVAL`). The three subagents are read-only by construction — their tool grants exclude Edit/Write/MultiEdit/Bash — so they produce blueprints and review findings, and only the top-level orchestrator writes code.

## How we tested it

**Evidence:** MEASURED

We verified the installed plugin source directly and ran discriminating checks on the agent and command definitions to confirm the behavioral claims (not a README paraphrase). The plugin is installed locally, so "source" here means the actual files Claude Code loads at runtime, not the upstream README.

**Files inspected (installed runtime copy):**
`~/.claude/plugins/repos/claude-plugins-official/plugins/feature-dev/` — `commands/feature-dev.md` (125 lines), `agents/code-architect.md`, `agents/code-explorer.md`, `agents/code-reviewer.md`, and `.claude-plugin/plugin.json`.

**Discriminating check 1 — read-only subagents.** A naive "feature dev" plugin would give its agents Write/Edit so they implement directly. We checked the `tools:` frontmatter of all three agents. None grants Edit/Write/MultiEdit/Bash:

```
$ for f in agents/*.md; do grep "^tools:" "$f"; done
# all three identical:
tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput
```

`BashOutput`/`KillShell` only read/manage already-running shells — they cannot start a command. So the design is genuinely propose-then-orchestrator-implements, which matches the workflow's separation of Phase 4 (design, read-only architects) from Phase 5 (implementation, run by the main thread).

**Discriminating check 2 — confidence-gated review.** The `code-reviewer` agent defines a 0-100 confidence rubric and a hard filter:

```
$ grep -n "confidence ≥\|0-100" agents/code-reviewer.md
25:Rate each potential issue on a scale from 0-100:
33:**Only report issues with confidence ≥ 80.** Focus on issues that truly matter - quality over quantity.
```

This is the false-positive-suppression mechanism that distinguishes it from a generic "review my code" prompt.

**Discriminating check 3 — mandatory human gates.** The command enforces two stop points, confirmed by grep:

```
$ grep -n "DO NOT SKIP\|DO NOT START WITHOUT\|Wait for answers" commands/feature-dev.md
61:**CRITICAL**: This is one of the most important phases. DO NOT SKIP.
67:4. **Wait for answers before proceeding to architecture design**
89:**DO NOT START WITHOUT USER APPROVAL**
```

**Discriminating check 4 — parallel fan-out and pinned model.** All three agents pin `model: sonnet`; the command launches them in parallel at three phases:

```
$ grep -n "in parallel" commands/feature-dev.md
41:1. Launch 2-3 code-explorer agents in parallel. ...
78:1. Launch 2-3 code-architect agents in parallel ...
106:1. Launch 3 code-reviewer agents in parallel ...
```

**Metadata oracle.** Confirmed the marketplace repo and license via `gh api`:

```
$ gh api repos/anthropics/claude-plugins-official \
    --jq '.full_name+" | stars="+(.stargazers_count|tostring)+" | license="+(.license.spdx_id)'
anthropics/claude-plugins-official | stars=30653 | license=Apache-2.0
```

We did not drive the full interactive 7-phase flow end-to-end on a sample feature (it requires a live multi-turn session with human approvals at Phases 3 and 5, which an automated A/B can't gate), but the structural claims that constitute the plugin's value — read-only blueprint agents, ≥80 confidence review filter, mandatory clarify/approve gates, parallel fan-out — are each confirmed against the runtime source.

## What worked

- **Read-only subagents are a real safety property, not marketing.** Verified by frontmatter: architects and reviewers physically cannot edit files, so the multi-agent design stage can't silently mutate the repo before the user approves an approach.
- **The ≥80 confidence filter is concrete and discriminating.** A 0-100 rubric with a hard cutoff is a documented mechanism to suppress nitpick noise — the common failure mode of "review this" prompts.
- **Two enforced human gates** (clarifying questions before design; approval before implementation) make the workflow auditable and hard to skip, encoded in capitals in the command body.
- **Competing-architecture fan-out** (minimal / clean / pragmatic) surfaces trade-offs instead of committing to the first idea — useful on non-trivial features.

## What didn't work or surprised us

- **The agent count is unconditional.** Phase 6 always launches 3 reviewers and Phases 2/4 launch 2-3 agents regardless of change size — a one-line fix gets the same 3x-parallel review treatment, which is token-expensive for small diffs. No "small fix" fast path.
- **All agents pinned to `model: sonnet`.** No way to escalate the architect to a stronger model for a hard design without editing the plugin; the pin is a fixed cost/quality point.
- **Value depends on multi-turn discipline.** The whole benefit hinges on the user actually answering the Phase 3 questions and approving Phase 5; in a hurried session the gates can be rubber-stamped, collapsing it toward an ordinary "just build it" run.
- **Not a CLI** — there is nothing to benchmark deterministically; the workflow is a prompt-orchestration contract, so its output quality is non-deterministic per run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Codebase exploration before design plus a confidence-gated 3-reviewer pass targets real bugs over nitpicks (verified ≥80 filter in code-reviewer.md). |
| Speed | - | Three sequential agent fan-outs (explore/design/review) and unconditional 3x review add latency vs writing code directly. |
| Maintainability | + | Competing minimal/clean/pragmatic architecture proposals plus convention-compliance review push toward maintainable code. |
| Safety | + | Read-only subagents (no Edit/Write/Bash) and two mandatory human approval gates prevent unreviewed mutation. |
| Cost Efficiency | - | 7-12 parallel sonnet subagent invocations per feature regardless of change size; no small-diff fast path. |

## Verdict

**KEEP**

The installed source substantiates feature-dev's core claims: genuinely read-only blueprint/review subagents, a concrete ≥80-confidence review filter, mandatory clarify-and-approve human gates, and parallel competing-architecture fan-out. It is a well-constructed, Anthropic-official process plugin worth keeping for non-trivial feature work where the up-front exploration and multi-gate discipline pay off. Its cost/speed overhead (unconditional multi-agent fan-out, sonnet-pinned, no small-fix fast path) makes it overkill for one-line changes — a CONDITIONAL-on-feature-size caveat — but as a kept tool the structural safeguards justify retention.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [feature-dev](https://github.com/anthropics/claude-plugins-official) | plugin | Guided feature development with codebase-understanding and architecture subagents plus a /feature-dev command | Unstructured feature work that skips exploration, design trade-offs, and review | code-architect / code-explorer / code-reviewer subagents; setup-workflow |
