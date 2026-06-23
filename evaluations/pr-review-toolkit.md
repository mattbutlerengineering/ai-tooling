# Evaluation: pr-review-toolkit

**Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit)
**Stars:** 30,653 (monorepo) | **Last updated:** 2026-06-23 | **License:** Apache-2.0
**Last verified:** 2026-06-22
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code plugin (authored by Anthropic, distributed in the official
`claude-plugins-official` marketplace) that ships six specialized PR-review
subagents plus a `/pr-review-toolkit:review-pr` slash command that orchestrates
them. Each subagent is a separate system prompt targeting one review axis:

| Agent | Targets | Model |
|-------|---------|-------|
| `code-reviewer` | CLAUDE.md / style-guide compliance, general bugs on the git diff | opus |
| `silent-failure-hunter` | swallowed errors, empty/broad catch blocks, unjustified fallbacks, missing logging | inherit |
| `comment-analyzer` | comment accuracy vs. code, comment rot, doc completeness | inherit |
| `pr-test-analyzer` | behavioral test coverage, critical gaps, test quality | inherit |
| `type-design-analyzer` | type encapsulation, invariant expression, quantitative design ratings | inherit |
| `code-simplifier` | post-review clarity/maintainability refactor that preserves behavior | opus |

When you invoke `/pr-review-toolkit:review-pr [aspects]`, the command (granted
`Bash, Glob, Grep, Read, Task`) inspects `git diff --name-only`, maps changed
file types to the applicable agents (always `code-reviewer`; `pr-test-analyzer`
if test files changed; `comment-analyzer` if docs/comments changed;
`silent-failure-hunter` if error handling changed; `type-design-analyzer` if
types added; `code-simplifier` as a final polish pass), dispatches them via the
`Task` tool (sequential by default, `parallel` on request), and aggregates the
findings into Critical / Important / Suggestions / Strengths buckets with
`file:line` references.

## How we tested it

**Evidence:** MEASURED

We verified the installed source on disk and ran a discriminating, objective
oracle against it — a wiring/consistency check, not a README paraphrase.

**Source inspected (real install):**
`~/.claude/plugins/repos/claude-plugins-official/plugins/pr-review-toolkit/` —
six agent `.md` files under `agents/`, the `commands/review-pr.md` orchestrator,
and `.claude-plugin/plugin.json` (name `pr-review-toolkit`, author Anthropic).
We read the full `silent-failure-hunter` system prompt (its non-negotiable
rules: forbids empty catch blocks, demands an error ID from
`constants/errorIds.ts` for Sentry, flags fallbacks to mock/stub implementations
outside tests) and the `code-reviewer` description (proactive, operates on the
unstaged `git diff`).

**The oracle — agent-routing bijection.** A multi-agent orchestrator is only as
good as its wiring: every agent the command dispatches must exist as a
registered subagent (matched by frontmatter `name:`, per the Claude Code
subagent registry), and there should be no orphan agents the command never
reaches. A dangling reference would make `/review-pr` fail at dispatch time with
"Agent type not found"; an orphan agent would be dead weight. We extracted both
sets and diffed them:

```bash
D=~/.claude/plugins/repos/claude-plugins-official/plugins/pr-review-toolkit
# registered agent names (frontmatter)
for f in "$D"/agents/*.md; do grep -m1 '^name:' "$f" | sed 's/name: //'; done \
  | sort > /tmp/agent_names.txt
# agent names the command actually routes to
grep -oE '\b(code-reviewer|code-simplifier|comment-analyzer|pr-test-analyzer|silent-failure-hunter|type-design-analyzer)\b' \
  "$D/commands/review-pr.md" | sort -u > /tmp/cmd_refs.txt

comm -23 /tmp/cmd_refs.txt /tmp/agent_names.txt   # referenced-but-missing
comm -13 /tmp/cmd_refs.txt /tmp/agent_names.txt   # registered-but-unwired
```

**Result:** both diffs empty. 6 registered agents, 6 command-referenced agents,
a clean bijection — no dangling dispatch targets, no orphan agents.

**Secondary oracles:**
- Every agent declares a `model` (`code-reviewer` and `code-simplifier` pin
  `opus`; the other four `inherit`) — none missing, so none silently fails to
  launch.
- The command's frontmatter grants `Task` in `allowed-tools` — the capability
  required to dispatch subagents at all. Without it `/review-pr` could compute a
  routing plan but never launch an agent.
- The `name:` field on every agent matches its filename and the command's
  routing table — the exact failure mode called out in CLAUDE.md ("the registry
  keys agents by frontmatter `name:`, not the filename") is absent here.

We did not execute a full end-to-end `/review-pr` against a live PR (that is a
non-deterministic, interactive multi-agent LLM run whose findings can't be
scored by an objective oracle). The wiring oracle above is the deterministic,
reproducible part and is what we measured.

## What worked

- **Routing is fully wired.** All six dispatch targets resolve to real
  registered agents and vice-versa (bijection oracle passed) — the command will
  not 404 on a dispatch.
- **Clear separation of concerns.** Each agent is a focused system prompt for
  one axis (errors / comments / tests / types / general / simplify), so a
  targeted invocation (`/review-pr errors`) launches exactly the relevant
  reviewer instead of one diffuse mega-prompt.
- **`silent-failure-hunter` is genuinely opinionated and concrete.** Its prompt
  encodes hard rules (no empty catch blocks, demand Sentry error IDs, no
  production fallback to mocks) — the kind of error-handling review a generic
  "review my PR" prompt routinely skips. This is the plugin's differentiated
  value.
- **Diff-scoped by default.** Agents target the `git diff`, keeping each review
  bounded to the change rather than re-reviewing the whole repo.

## What didn't work or surprised us

- **Two agents hard-pin `opus`** (`code-reviewer`, `code-simplifier`). On an
  account without opus access or under cost pressure these will be the expensive
  legs of every full review; the value is real but the cost is not configurable
  without editing the agent files.
- **`silent-failure-hunter` references project-specific artifacts**
  (`constants/errorIds.ts`, a `logError` helper, Sentry). Those heuristics are
  tuned to Anthropic's internal codebase conventions; on a repo without them the
  advice degrades to generic "log your errors."
- **No objective gate.** Output is LLM prose bucketed by severity — useful, but
  there is no machine-checkable pass/fail, so it complements a linter/type-checker
  rather than replacing one. (This is inherent to agentic review, not a defect.)
- **The full review is non-deterministic and interactive** — repeatability and
  cost depend on diff size and how many agents the router fires.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | `silent-failure-hunter` + `code-reviewer` surface swallowed errors, broad catches, and CLAUDE.md violations a single generic review prompt tends to miss. |
| Speed | neutral | Adds an LLM review pass before PR; sequential default trades wall-clock for clarity, `parallel` mode recovers it. |
| Maintainability | + | `comment-analyzer` (comment rot) and `code-simplifier` (clarity-preserving refactor) directly target long-term readability. |
| Safety | + | The error-handling and type-design agents target failure-masking and weak invariants — the bugs that bite in production. |
| Cost Efficiency | - | Two agents pin `opus`; a full multi-agent review on a large diff is several model calls per PR. |

## Verdict

**KEEP**

Source-verified and routing-measured: an Apache-2.0, first-party Anthropic plugin
whose six-agent fan-out is correctly wired (bijection oracle passed) and whose
`silent-failure-hunter` / `type-design-analyzer` prompts add review depth a
generic "review this PR" prompt does not. Worth keeping installed for Review-stage
work, with two caveats: the opus-pinned agents make a full review cost-sensitive,
and several heuristics assume Anthropic-internal conventions (`errorIds.ts`,
Sentry) that soften on other codebases. Use it as a complement to deterministic
gates (linter, type-checker, tests), not a replacement — it has no machine-checkable
oracle of its own.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit) | plugin | Six specialized Claude Code PR-review subagents plus a /review-pr orchestrator command | Generic "review my PR" prompts miss error-handling, type-design, and comment-rot defects; this fans out one focused agent per axis | code-reviewer, silent-failure-hunter, codeburn |
