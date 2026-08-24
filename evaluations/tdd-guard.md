# Evaluation: TDD Guard

**Repo:** [nizos/tdd-guard](https://github.com/nizos/tdd-guard)
**Stars:** 2,311 | **Last updated:** 2026-08-16 (last push) | **License:** MIT | **Language:** TypeScript (npm: `tdd-guard` 1.7.0, 96K downloads/mo)
**Last verified:** 2026-08-23
**Dev loop stage:** Review / Verify — enforces TDD during Implement
**Layer:** Tooling (Claude Code hook + test reporters)

---

## What it does

TDD Guard is a Claude Code **PreToolUse hook** that blocks file edits which violate test-driven
development: implementation written with no failing test behind it, and implementation that goes
beyond what the current tests require. Test-framework reporters (Vitest, Jest, Storybook, pytest,
PHPUnit, Go, Rust, RSpec, Minitest) write results into `.claude/tdd-guard/data/test.json`, and the
hook reads that state when deciding.

The decision is made in two layers, and the split is the whole story of this evaluation: a
**deterministic layer** that resolves most events locally with no model, and a **model layer** that
adjudicates everything else by asking Claude.

## How we tested it

**Evidence:** RUN

Installed `tdd-guard@1.7.0` into a scratch project and drove the CLI directly — it is a stdin/stdout
hook, so hook payloads can be fed to it without an agent in the loop. Two environments:

1. **No credentials**, isolated `HOME`, to map the deterministic frontier — which events are decided
   locally and which escalate.
2. **`MODEL_TYPE=claude_cli USE_SYSTEM_CLAUDE=true`**, to measure the enforcement itself.

The real `~/.claude` was never a target: `CLAUDE_PROJECT_DIR` scoped all guard state to the scratch
tree, and the only use of the real home was the `claude` binary's own auth.

`npm i tdd-guard@1.7.0` took 4.65 s and left a 170 MB `node_modules`; each case was then driven as
`CLAUDE_PROJECT_DIR=/private/tmp/tg/proj tdd-guard < case.json`, which prints a decision on stdout
and nothing at all when the edit is allowed.

### Test design

| | |
|---|---|
| **Question** | Does the guard block TDD violations, allow compliant edits, and how much of that needs a model? |
| **Task set** | 24 hook payloads: session events, ignore-pattern files, non-modifying tools, test-file additions in 6 languages, implementation edits under three recorded test states |
| **Oracle** | The CLI prints a JSON decision on a block and nothing at all on an allow — mechanically checkable, no judgement |
| **Control** | Every claim is a **pair**: a violation payload that must block *and* a compliant payload that must not. A rule that blocked both would be indistinguishable from a broken guard |
| **N** | 3–5 per model-layer cell, with the full state directory wiped between runs so each is genuinely identical |

Two fixture bugs of mine were found and fixed before any measurement was reported, neither a tool
defect: `/tmp` is a symlink on macOS, so a `CLAUDE_PROJECT_DIR` that did not match `realpath` threw;
and payloads missing `transcript_path` fail schema validation and are silently allowed, which made an
entire language battery read as "all allowed" until the field was added.

## What worked

- **The deterministic layer is real and fast.** With no credentials at all, six event classes resolve
  locally in **~150–200 ms**: `SessionStart`; the 11 default ignore patterns (`*.md`, `*.json`,
  `*.yml`, …, matched basename-wide); non-modifying tools (`Read`, `Bash`); unparseable payloads
  (fail-open); the `tdd-guard off` toggle, which persists `{"guardEnabled":false}` and passes
  implementation edits through; and test-file edits that add **exactly one** test.
- **That one-test exemption is AST-based, not a regex.** `@ast-grep` parses the before and after
  content and diffs the test count per language. Measured across the languages that ship a grammar:
  Go, PHP and Ruby each allowed a 1-test addition locally and escalated a 2-test addition — including
  Python and Go with no Python or Go toolchain on the machine.
- **A block that needs no model at all.** With tests green and lint issues recorded, the hook blocks
  once with a code-quality message, flips `hasNotifiedAboutLintIssues`, and goes quiet on the next
  edit. Deterministic, and it fires ahead of the one-test fast path.
- **The enforcement itself works, on both halves of the claim.** With a model reachable:
  - **Violation** — implementation with no failing test recorded: **3/3 blocked**, median **8.0 s**.
    The reason is specific enough to act on, naming the file and the function: *"Premature
    implementation - this is a new implementation file (src/impl.ts) adding the `add` function with
    full working logic, but no test output was provided showing a failing test that requires this."*
  - **Over-implementation** — tests green covering `add` only, edit adds five functions: **3/3
    blocked**, median **7.2 s**. This is the half most "write tests first" skills do not attempt.

## What didn't work or surprised us

- **The guard is not a deterministic gate, and its failure mode is blocking work you were entitled
  to.** A **compliant** edit — implementation written against a recorded *failing* test, the exact
  case TDD says to allow — was blocked **2 of 5 times** with the entire state directory wiped between
  runs, so the inputs were byte-identical. Across all 13 runs of that payload, 4 blocked. The two
  refusals in the clean batch did not even agree with each other on what the violation was: one said
  *"Premature implementation"*, the other *"Over-implementation violation"*, about the same edit.
  This is inherent — a model adjudicates, so identical inputs need not produce identical verdicts —
  and it is the cost nobody writes down, because the documented caveat runs the other way
  (bypassable, false negatives) while what we measured is a false positive at a rate you will notice.
- **No credentials means block, not pass.** With no reachable model the hook returns
  `{"decision":"block","reason":"Error during validation: Not logged in · Please run /login"}` —
  **5/5, deterministically**. A logged-out session, an expired token or an offline machine therefore
  stops every implementation edit, and the message arrives as a TDD refusal rather than an auth
  error. Fail-closed is defensible for a guardrail; it is not what "bypassable by design" prepares
  you for, and it is worth knowing before it happens mid-task.
- **Two of the nine advertised frameworks get no fast path**, both because of how a test file is
  *recognised* rather than how it is parsed:
  - **Rust** — `isTestFile` has no pattern for a `.rs` source file, and idiomatic Rust unit tests
    live inline in `src/*.rs` under `#[cfg(test)] mod tests`. Measured: `tests/calc.rs` (integration
    style) takes the fast path; the same test inline in `src/lib.rs` escalates to the model.
  - **Minitest** — the Ruby counter matches `it` calls only, i.e. RSpec. Minitest's `def test_add`
    counts as zero tests, so `test/calc_test.rb` escalates. Not a failure — the model still decides —
    but the free path is unavailable to those users.
- **Latency is bimodal and lands on every guarded edit**: allow ≈ **2.7–3.1 s**, block ≈ **9–12 s**,
  with a 37.5 s outlier observed. The CLI client hardcodes `--max-turns 5`, so a validation is an
  agentic call, not a single completion.
- **`TDD_GUARD_MODEL_VERSION` does not reach the CLI client.** It defaults to `claude-sonnet-4-6`,
  but `ClaudeCli` passes a hardcoded `--model sonnet`; the setting applies to the API/SDK clients
  only. A config surface that silently does nothing on the default path is worth knowing about.
- **A supply-chain advisory is reachable from the current version.** `npm audit` reports 3 moderate
  findings — `@anthropic-ai/sdk` insecure default file permissions (GHSA-p7fg-763f-g4gf), pulled in
  via `@anthropic-ai/claude-agent-sdk` by `tdd-guard >=1.5.1`. `npm audit fix --force` resolves it by
  **downgrading `tdd-guard` from 1.7.0 to 1.5.0**, a breaking change; there is no clean fix at the
  current version.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | 3/3 blocked implementation with no failing test; 3/3 blocked over-implementation past the current tests. Both halves of red-green enforced, measured. |
| Speed | − | Every guarded edit pays 2.7–3.1 s to pass or 9–12 s to be refused; a wrongly-refused edit costs a full retry loop on top. |
| Maintainability | + | Enforced test-first plus a deterministic lint gate keeps diffs small and covered. |
| Safety | + / − | A real guardrail against skipping verification — but it fails **closed** (5/5 blocked with no credentials), so a credential or network problem stops implementation entirely. |
| Cost Efficiency | − | MIT and free, but each escalated edit is an agentic Sonnet call at up to 5 turns. The deterministic layer (~150–200 ms, no tokens) absorbs session events, ignored files and single-test additions. |
| Verifiability | + | The decision is machine-checkable — JSON on block, silence on allow — so the planted-violation/compliant pairing makes a green result falsifiable rather than assumed. |

## Verdict

**CONDITIONAL** — adopt-if: you practise strict TDD, **and** you accept that the gate is a model
judgement rather than a deterministic rule — it blocked a compliant edit 2 times in 5 identical runs —
**and** every machine running the hook has working Claude credentials, because without them it blocks
every implementation edit rather than passing them through.

The enforcement claim is true and now measured: 3/3 on premature implementation and 3/3 on
over-implementation, with reasons specific enough to act on. That is a real difference in kind from
the `tdd` / `test-driven-development` skills, which *advise* test-first and are followed at the
model's discretion. What the tool's own docs frame as the risk — that a determined agent can route
around a hook via MCP or shell — is the *less* likely thing to bite you day to day. The measured
risk runs the other way: a legitimate edit refused, non-reproducibly, with a confident and
inconsistent explanation.

Two things make that tolerable rather than disqualifying: `tdd-guard off` is a one-line escape that
works deterministically, and the deterministic layer already absorbs the high-frequency events, so
the model is consulted less often than the framing suggests.

Compared to neighbours: **stryker-js** mutation-tests whether your tests are any good;
**pr-review-toolkit** reviews after the fact; the **superpowers** TDD skill advises. TDD Guard is the
only one that stops the edit in real time — and the only one whose verdict on the same edit can
differ between runs.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tdd-guard](https://github.com/nizos/tdd-guard) | plugin | Claude Code hook that blocks implementation without a failing test and over-implementation past current tests (MIT); AST-based fast path for 1-test additions, model-adjudicated otherwise | Agents skip tests and over-build; want red-green-refactor discipline mechanically enforced, not just requested | stryker-js, superpowers (tdd skill), pr-review-toolkit |
