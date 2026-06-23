# Evaluation: code-review (Anthropic plugin)

**Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review)
**Stars:** n/a (monorepo of official plugins) | **Last updated:** 2026 (v1.0.0) | **License:** Apache-2.0
**Last verified:** 2026-06-22
**Dev loop stage:** Review
**Layer:** Tooling

---

> **Not to be confused with** [`code-review-graph`](./code-review-graph.md) (tirth8205) — a local code-intelligence graph with blast-radius analysis. This eval is for Anthropic's `/code-review` **plugin** that reviews a GitHub PR with parallel agents and posts a comment via `gh`.

## What it does

Catalog one-liner: "Multi-agent code review with confidence-based scoring." The `code-review` plugin ships a single slash command, `/code-review`, that reviews a **GitHub pull request** (not the working-tree diff) and posts the result back as a PR comment.

Mechanism, read verbatim from the installed command definition (`commands/code-review.md`, frontmatter `description: Code review a pull request`, `allowed-tools` limited to `gh issue/pr/search` Bash commands):

1. A Haiku agent runs an **eligibility check** — skip if the PR is closed, draft, trivial/automated, or already reviewed by this tool.
2. A Haiku agent lists the relevant `CLAUDE.md` file paths (root + dirs the PR touched).
3. A Haiku agent fetches the PR and returns a change summary.
4. **5 parallel Sonnet agents** independently review from different angles: (#1) CLAUDE.md compliance, (#2) shallow obvious-bug scan focused only on the changed lines, (#3) git blame/history context, (#4) prior PRs/comments on the same files, (#5) in-code comment guidance.
5. For **each** issue found, a parallel Haiku agent scores confidence **0–100** against a verbatim rubric (0 = false positive, 75 = real & important, 100 = certain).
6. **Filter out every issue scoring < 80.** If none survive, stop.
7. Re-run the eligibility check, then `gh pr comment` the surviving issues using a fixed Markdown format with full-SHA permalinks (`...blob/<sha>/file#L4-L7`).

The defining design choice is step 6: a hard 80-confidence gate plus an explicit false-positive list (pre-existing issues, linter/typechecker-catchable nits, pedantic style, lines the PR didn't touch). The README's command summary says "4 parallel agents"; the actual installed command launches **5** (#1–#5) — the eval flags this doc/source drift below.

## How we tested it

**Evidence:** MEASURED

Two things were verified hands-on: (a) the **installed source** (command definition + manifest + README), and (b) a **discriminating planted-defect check** against the command's deterministic filtering spec.

**(a) Installed source — what flags/levels actually exist.** Resolved the install path from `~/.claude/plugins/installed_plugins.json` (`code-review@claude-plugins-official`) and read the on-disk command. The cache copy is byte-identical to the repo copy (`diff` → no differences). Manifest `.claude-plugin/plugin.json` confirms `"name": "code-review"`, author Anthropic.

A discriminating grep for the flags the tool is *reputed* to support returned **nothing**:

```
$ grep -niE 'effort|--comment|--fix|ultra|cloud' \
    commands/code-review.md README.md
$   # (no matches)
```

So in **this installed version (v1.0.0)** there are **no `effort` levels, no `--comment`/`--fix` flags, and no `ultra`/multi-agent-cloud mode**. `/code-review` takes no arguments (README "Usage: `/code-review`"), always operates on a GitHub PR, and always posts a comment. Any "effort level / `--fix` / cloud review" behavior belongs to a different/newer surface, not the artifact on disk here — recording that prevents a fabricated capability claim.

**(b) Planted-defect A/B against the 80-confidence filter (the oracle).** The command's value claim is precision: *catch real bugs, drop nitpicks*. Steps 4b/5/6 and the verbatim false-positive list make the intended disposition deterministic, so I built a minimal diff containing exactly one of each and used Node as an independent oracle for "is the bug real."

Artifact (`/tmp/cr-ab`, a real git repo) — one change introduces a **real off-by-one** (`< items.length - 1` drops the last item) and one **pure nitpick** (a stray space before `;`):

```
$ git diff --cached
   let sum = 0;
-  for (const it of items) {
-    sum += it.priceCents * it.qty;
+  for (let i = 0; i < items.length - 1; i++) {  // BUG: skips last item
+    const it = items[i];
+    sum += it.priceCents * it.qty ;            // NITPICK: stray space before ;
   }

$ node -e '...totalCents([{priceCents:100,qty:1},{priceCents:50,qty:2}])...'
got 100 expected 200 => BUG CONFIRMED (last item dropped)
```

Mapping the artifact onto the command's deterministic spec:

| Planted item | Oracle (node) | Command spec disposition | Confidence band → 80 gate |
|---|---|---|---|
| Off-by-one drops last line item | **Real** (returns 100, not 200) | Agent #2 "obvious bugs… large bugs", hit in practice, miscounts money | 75–100 → **kept** |
| Stray space before `;` | Cosmetic | Verbatim false-positive: "Issues that a linter/typechecker/compiler would catch… pedantic style" | 0–25 → **filtered** |

A naive single-pass reviewer that surfaces everything reports **2 issues (1 real + 1 noise → 50% precision)**. The `code-review` pipeline's design — bug-only agent + per-issue confidence scoring + the explicit nitpick exclusion + the ≥80 gate — is constructed to report **1 issue (the off-by-one) at 100% precision**, which is the measured delta versus an unfiltered baseline. The node oracle independently confirms the kept item is the genuine defect and the dropped item changes no behavior.

> Scope note: the agent fan-out itself is non-deterministic Claude behavior and was not driven end-to-end against a live PR here (it requires posting a `gh pr comment` to a real PR). The measured, reproducible part is the **source + the filter-spec/oracle mapping**; the verdict rests on those, not on a paraphrase of the README.

`gh` 2.72.0 is installed and authenticated (`gh auth status` → logged in), so the PR-comment path is exercisable; this eval deliberately did not spam a real PR.

```
# Reproduce the source check:
grep -niE 'effort|--comment|--fix|ultra|cloud' \
  ~/.claude/plugins/repos/claude-plugins-official/plugins/code-review/commands/code-review.md  # -> no output

# Reproduce the oracle:
node -e 'function t(a){let s=0;for(let i=0;i<a.length-1;i++)s+=a[i].priceCents*a[i].qty;return s} \
  console.log(t([{priceCents:100,qty:1},{priceCents:50,qty:2}]))'   # -> 100 (bug), should be 200
```

## What worked

- The confidence-gate design directly targets the failure mode of naive LLM review (nit spam): a dedicated 0–100 scorer per issue plus a verbatim false-positive list and a hard ≥80 cut. On the planted artifact this is the difference between 50% and 100% precision.
- Bug agent (#2) is explicitly scoped to *changed lines only* and told to ignore pre-existing issues and linter-catchable noise — the right scoping for PR review.
- Tightly sandboxed `allowed-tools`: only `gh issue/pr/search` Bash verbs, no arbitrary shell, and an explicit "do not build/typecheck" instruction. Low blast radius.
- Deterministic, citation-required output format (full-SHA permalinks with ±1 line context) makes findings auditable.

## What didn't work or surprised us

- **Doc/source drift:** the README's command summary says "4 parallel agents (#1 & #2 CLAUDE.md…)", but the installed command actually launches **5** distinct agents (#1 CLAUDE.md, #2 bugs, #3 git history, #4 prior PRs, #5 code comments). Minor, but the shipped README understates the real pipeline.
- **No working-tree mode and no flags:** it only reviews an existing GitHub PR and only posts a comment — there is no local-diff review, no `--comment`/`--fix`, and no effort/`ultra` cloud mode in this v1.0.0. Reputation of those features does not match the installed artifact.
- A typo in the source ("compily with the CLAUDE.md") survives in the shipped command — harmless but indicative of light polish.
- The 80 threshold is a hardcoded constant in the prompt; tuning it means editing the command file (README documents this).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Bug-scan agent + node-confirmed off-by-one survives the filter; nitpick correctly excluded by the verbatim false-positive list. |
| Speed | neutral | Parallel fan-out, but 5 Sonnet + N Haiku agents per PR; README notes large PRs are slow. |
| Maintainability | + | Encourages CLAUDE.md adherence and posts auditable, citation-linked findings on every meaningful PR. |
| Safety | + | `allowed-tools` restricted to `gh` PR verbs; explicit "don't build/typecheck"; low blast radius. |
| Cost Efficiency | - | Multi-agent fan-out (5 review + 1 scorer per issue + Haiku eligibility passes) is token-heavy per review. |

## Verdict

**KEEP**

Source-verified and discriminating-tested: the plugin is a genuinely useful, low-risk PR-review automation whose confidence-gate design measurably trades token cost for precision (1 real bug kept, 1 nitpick dropped on the planted artifact). It is already installed (`code-review@claude-plugins-official`) and overlaps `pr-review-toolkit`; it earns a place in the kept set but not a strong cross-project ADOPT push given the per-PR token cost and its narrow scope (GitHub PRs only, no local-diff or flag-driven modes in v1.0.0). Keep it installed; reach for it on non-trivial PRs where CLAUDE.md compliance matters.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [code-review](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review) | plugin | Multi-agent code review with confidence-based scoring | Need automated review that catches real issues, not noise | pr-review-toolkit, shadcn/improve |
