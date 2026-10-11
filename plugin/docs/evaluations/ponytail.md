# Evaluation: ponytail

**Repo:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
**Stars:** 160,404 | **Last updated:** 2026-10-10 (pushed; v5.1.0 released 2026-10-08) | **License:** MIT
**Last verified:** 2026-10-10
**Last triaged:** 2026-10-10  <!-- triaged: human -->
**Dev loop stage:** Implement (a behavioral ruleset that gates *how much* code the agent writes before it writes it); touches Review (`ponytail-audit` / `ponytail-debt` / `ponytail-review` report on over-build and deferred shortcuts)
**Layer:** Process / Tooling (one ruleset distributed for ~14 agents; in Claude Code a plugin whose SessionStart hook injects the ruleset every session)

---

## What it does

The catalog one-liner: "Makes AI agents think like the laziest senior dev — write minimum code, avoid overengineering." The core is `skills/ponytail/SKILL.md`, a "smallest complete change" ladder the agent runs before writing: (1) does it need to exist, (2) already in this codebase, (3) stdlib/platform, (4) installed dependency, (5) one line, (6) otherwise the minimum that works. It bans unrequested abstractions, wrappers, options and "for later" code, but explicitly never cuts validation at trust boundaries, data-loss error handling, security or accessibility. Two rules shape output beyond size: non-trivial new logic must leave "one small test or an assert-based self-check", and a deliberate simplification gets a `shortcut: <limit>, <when to upgrade>` comment (renamed from the older `ponytail:` marker). Every reply ends with a line on what was skipped or not checked.

As a Claude Code plugin (`.claude-plugin/plugin.json`, v5.1.0) it registers three Node hooks: `SessionStart` (`ponytail-activate.js` — writes a mode flag to `$CLAUDE_CONFIG_DIR/.ponytail-active` and emits the filtered SKILL.md body plus a "codebase map" as hidden context), `SubagentStart` (same for subagents) and `UserPromptSubmit` (mode tracking for `/ponytail lite|full|ultra`). Companion skills: `ponytail-audit` (whole-repo ranked audit: bugs, security, load, missing tests, speed, lean), `ponytail-review` (diff review), `ponytail-debt` (greps `shortcut:` markers into a ledger and tags ones with no upgrade trigger), `ponytail-gain`, `ponytail-help`.

## How we tested it

**Evidence:** MEASURED

Re-evaluated hands-on on 2026-10-10 (human-directed; the earlier bulk `discovery-log` read was a README review). Ponytail was cloned at commit `9b58c1f` (v5.1.0) into a scratch directory and driven through headless Claude Code 2.1.296 with `claude-sonnet-5-5`, never installed globally. Four measurements, all with a hidden or planted objective oracle:

1. **Implement A/B (the headline):** 5 coding tasks × 2 arms × 3 runs = 30 runs, each scored by a hidden test suite the agent never saw.
2. **Triggering:** the bare `ponytail` skill (no hook) on 4 should-fire and 2 shouldn't-fire prompts, detected from `stream-json` `Skill` tool calls.
3. **`ponytail-audit` vs a plain audit prompt** on a fixture with 5 planted defects, 2 runs per arm.
4. **`ponytail-debt` vs a plain ledger prompt** on a fixture with 3 planted `shortcut:` markers (one without a trigger) and one decoy, 1 run per arm.

Total API spend across all 46 runs: **$2.43**.

### Isolation (what "baseline" means)

Both arms ran with `--setting-sources project`, which drops the user's global `~/.claude` settings, plugins and `CLAUDE.md` (a positive/negative control confirmed it: the same "does your context mention X from the global CLAUDE.md" probe answered *Yes* with default sources and *No* with `--setting-sources project`). This matters because the operator's own global rules already include a karpathy-derived "Simplicity First" section — so **the baseline is stock Claude Code, not this operator's configured setup**, and ponytail's marginal value over an existing minimalism rule was *not* measured.

The ponytail arm reproduces the plugin's always-on mode faithfully: ponytail's own `hooks/ponytail-activate.js` was executed from each fixture's cwd with `CLAUDE_CONFIG_DIR` pointed at a scratch dir (so its flag files never touched `~/.claude`), and its stdout — the full-level ruleset plus codebase map — was passed via `--append-system-prompt-file`. The only edit was deleting the trailing "STATUSLINE SETUP NEEDED … proactively offer to set this up" nudge, which would otherwise have asked the agent to edit settings. Difference from a real install: the text lands in the system prompt instead of SessionStart `additionalContext`.

## Test design

- **Task/corpus:** five Python/Node tasks, each a one-function or one-class request worded with an over-engineering lure ("make it robust and production-ready", "design it to be extensible", "flexible enough to support YAML and env vars", "make it enterprise-grade"):
  - t1 `parse_duration("1h30m")` → seconds, ValueError on bad input (Python; 18 hidden tests)
  - t2 `slugify(title)` with accent stripping and TypeError (Node; 7)
  - t3 `LRUCache(capacity)` with `get/put/len/in`, ValueError on bad capacity (Python; 8)
  - t4 `loadConfig(path)` JSON-over-defaults with validation, then wire it into `server.js` (Node; 6)
  - t5 `batch_send(items, send, size)` with 3-attempt retry, in a repo that already has a `utils.chunked` helper (Python; 4)

  Every hidden suite was first validated green against a hand-written reference solution.
- **Baseline:** identical prompt and fixture, no ponytail text.
- **Metric:** hidden tests passed (k/N); implementation LOC = non-blank added lines in non-test files, *excluding* any `if __name__ == "__main__":` / `if (require.main === module)` self-check block (counted separately with any test files the agent wrote); output tokens, cost and wall time from `--output-format json`.
- **Reproduce:** the per-run script, a sketch:

```bash
# per run: fresh fixture copy + git init, then
CLAUDE_CONFIG_DIR=$SCRATCH/cfg CLAUDE_PLUGIN_ROOT=$PONYTAIL node $PONYTAIL/hooks/ponytail-activate.js \
  | sed '/^STATUSLINE SETUP NEEDED/,$d' > injected.txt                       # ponytail arm only
claude -p "$(cat prompt.txt)" --model claude-sonnet-5-5 --setting-sources project \
  --output-format json --no-session-persistence --dangerously-skip-permissions \
  --max-budget-usd 0.75 [--append-system-prompt-file injected.txt] > claude.json
git add -A && git diff --cached --numstat HEAD      # LOC
cp hidden/test_hidden.* . && pytest -q test_hidden.py   # or: node --test test_hidden.js
```

### Test design — skills

- **Triggering:** bare skill in `.claude/skills/ponytail/` with no hook. Should-fire **1/4**: it fired only on "write a CLI script … make it flexible". It did *not* fire on "add `mean(xs)`", on "refactor chunked to accept `fill`", or even on "I think this code is over-engineered, give me the simplest solution", despite "simplest solution" and over-engineering complaints being named triggers in its `description`. Shouldn't-fire: **0/2** false fires (a process-vs-thread question, a haiku). The skill under-triggers; the plugin's SessionStart hook is what makes ponytail work in Claude Code. JetBrains' independent test (below) reports the same: zero self-activations in ten sessions.
- **Output A/B:** the results follow.

### Results — Implement A/B (n = 3 per arm per task, claude-sonnet-5-5)

| Task | Arm | Hidden tests | Impl LOC per run | Median impl LOC | Self-check + test LOC (sum) | Mean output tokens | Cost (3 runs) |
|------|-----|--------------|------------------|-----------------|------------------------------|--------------------|---------------|
| t1 duration | baseline | 54/54 | 21, 23, 22 | 22 | 0 | 1,900 | $0.200 |
| t1 duration | ponytail | 54/54 | 14, 10, 10 | 10 (−55%) | 40 | 1,348 | $0.181 |
| t2 slugify | baseline | 21/21 | 12, 12, 12 | 12 | 0 | 718 | $0.140 |
| t2 slugify | ponytail | 21/21 | 10, 10, 10 | 10 (−17%) | 23 | 742 | $0.154 |
| t3 LRU | baseline | 24/24 | 38, 43, 30 | 38 | 0 | 1,525 | $0.183 |
| t3 LRU | ponytail | 24/24 | 21, 21, 21 | 21 (−45%) | 98 | 1,662 | $0.206 |
| t4 config | baseline | 18/18 | 39, 45, 40 | 40 | 0 | 1,522 | $0.181 |
| t4 config | ponytail | 18/18 | 23, 24, 24 | 24 (−40%) | 0 | 1,409 | $0.190 |
| t5 batch | baseline | 12/12 | 21, 21, 21 | 21 | 0 | 679 | $0.138 |
| t5 batch | ponytail | **11/12** | 20, 17, 16 | 17 (−19%) | 54 | 893 | $0.160 |
| **All** | baseline | **129/129** (15/15 runs green) | — | Σ 400 | 0 (0/15 runs) | 1,269 | $0.842 |
| **All** | ponytail | **128/129** (14/15 runs green) | — | Σ 251 (**−37%**) | 215 (12/15 runs) | 1,211 (−5%) | $0.892 (**+6%**) |

Mean wall time per run: 12.2 s baseline vs 14.4 s ponytail (+18%); turns 50 vs 60 in total, the extra turns spent running the self-checks.

Variance and significance, stated honestly: the median implementation-LOC reduction held on **5/5 tasks** (a sign test gives p = 0.0625 two-sided, so it is suggestive at this n, not significant). Baseline runs were remarkably stable within a task (t2 and t5 identical across all three); ponytail's t3 runs were identical at 21 lines. Cost moved the *wrong* way on 4/5 tasks; only t1 was cheaper.

**Where the LOC went.** The baseline took the bait each time it was offered: on t3 all three runs added `_on_hit` / `_on_miss` / `_touch` / `_evict` "extension point" hook methods that nothing calls, and on t4 all three built a `parsers = { '.json': JSON.parse }` registry for the YAML that was never requested. Ponytail runs skipped both and, in 2/3 t4 runs, left the exact `shortcut:` marker the rules ask for (`// shortcut: JSON only; for YAML pick the parser by extension here, for env overrides merge after this line`). Every ponytail run ended with a skipped / not-checked risk line, and 12/15 left a runnable self-check or test file. Baseline runs left none in 15/15.

**The one regression (t5, run 2).** Ponytail's version sliced `items[i:i+size]` directly, so a `range` input produced `range` batches instead of the lists the prompt specified ("calls `send(batch)` with each batch (a list)"). The hidden test failed on `isinstance(got[0], list)`. Its own self-check only passed lists, so it did not catch this. The baseline run it can be compared with converted with `list(items)` first. Separately, **0/6 runs in either arm reused the repo's existing `utils.chunked`** even though rung 2 of ponytail's ladder ("already in this codebase? use it") is aimed at exactly this case.

### Results — companion skills

| Check | Oracle | Baseline prompt | With skill |
|-------|--------|-----------------|------------|
| `ponytail-audit` (2 runs/arm) | 5 planted defects: SQL injection, `split_bill` dropping remainder cents, dead `legacy.py`, unused or duplicated `utils.chunked`, speculative no-op cache hooks | 5/5 found in both runs; 800–930 words; $0.070 mean | 5/5 found in both runs; ~1,090 words; $0.091 mean (+30%) |
| `ponytail-debt` (1 run/arm) | 3 `shortcut:` markers, 1 with no trigger, 1 "keyboard shortcut" decoy | 3/3, flagged the no-trigger one, excluded the decoy; $0.050 | 3/3, `no-trigger` tag, decoy excluded, ends "3 markers, 1 with no trigger."; $0.044 |

Neither companion skill found anything a direct prompt missed. `ponytail-audit` adds a fixed structure (Must / Should / Nice-to-have, a numbered "If we skip it" consequence on each finding, a Lean line total, a "Not checked" footer) at about 30% more cost. `ponytail-debt` is a well-specified grep with a stable one-line-per-marker format. Neither has a detection edge at this scale. Both arms left the audited tree unchanged (`git status` clean).

### Independent corroboration (third-party, not ours)

JetBrains' write-up ([blog.jetbrains.com, 2026-07](https://blog.jetbrains.com/ai/2026/07/ponytail-skill-claude-tested/), treated as data) ran SkillsBench, 80 paired tasks on `claude-sonnet-5`. It reports 15.4% less code (p = 0.088), 10.3% lower cost (p = 0.004), −11% time, and quality differences it calls a null result (65 identical, 9 slightly worse, 6 slightly better), with savings concentrated in large builds (−31%). Its caveats match ours: the installed skill self-activated 0 times in 10 sessions (the results came from hook injection), the `shortcut:`-style comment appeared once in 80 trials, and safety was not tested. The vendor's own headline (−54% code, −20% cost) did not reproduce there. Our code-size reduction is larger (−37%) because our tasks were chosen as over-build traps, and our cost result is the opposite sign (+6%) because on tasks this small the fixed cost of the injected ruleset and extra self-check turns outweighs the tokens saved.

## What worked

- **It reliably refuses the over-build lure.** Implementation LOC was down on every task (−17% to −55% median, −37% overall), and the difference is the speculative structure, not golfing. The baseline's unused hook methods (t3) and parser registry (t4) never appeared under ponytail.
- **It makes its own output easier to check.** 12/15 ponytail runs left a runnable self-check or test (baseline: 0/15), every run ended with an explicit "skipped / not checked" line, and t4's deferral was recorded as a greppable `shortcut:` comment that `ponytail-debt` then turns into a ledger. A reviewer gets less code plus a stated boundary.
- **Correctness was essentially held** on the hidden oracle: 128/129 vs 129/129, with no validation dropped. Every ponytail t3 run kept the `ValueError` on bad capacity, and t4 kept both config validators and the JSON error path. That is consistent with the "never cut validation" carve-out.
- **The hook-based activation is faithful and inspectable.** `ponytail-activate.js` is about 170 lines, reads `SKILL.md`, filters it by level, and honours `CLAUDE_CONFIG_DIR`, so it could be sandboxed to a scratch dir with no global writes.

## What didn't work or surprised us

- **It did not save money here.** Cost was +6% and wall time +18% (extra turns to run the self-checks), with output tokens only −5%. On small tasks the injected ruleset (~3.7 KB per session) and the check-running turns cost more than the shorter code saves. JetBrains saw −10% cost on larger SkillsBench tasks, so treat cost as task-size dependent, not a reliable win.
- **The bare skill under-triggers badly (1/4).** It missed even an explicit "simplest solution / over-engineered" request. Installing only the `skills/` folder (e.g. via a generic skills installer) gives you very little. You need the plugin's SessionStart hook, which is three Node hooks on the hot path that write flag files under `~/.claude`.
- **"Lazy" produced one real spec miss.** t5 run 2 skipped the `list(...)` conversion the prompt asked for, and its own self-check was too narrow to catch it. Minimal code plus a self-written check is not the same as a correct one.
- **Rung 2 (reuse the codebase) did not fire.** 0/3 ponytail runs used the existing `utils.chunked` helper. Where it counted here, the ladder worked on rungs 1 and 6, not 2.
- **The self-check convention adds lines.** Counted naively (everything non-test that was added), ponytail's t2 and t5 diffs are *larger* than baseline (median 17 vs 12, 34 vs 21) because of `if __name__ == "__main__":` assert blocks living inside the module. Teams that keep test code out of source files will want lite mode or a house rule to put the check in a test file.
- **Not measured: marginal value over an existing minimalism rule.** The baseline had no "Simplicity First" text. A setup that already carries karpathy-style guidance (as this operator's global rules do) may see a smaller delta.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Hidden-oracle pass 128/129 vs 129/129 (one run's `range`-vs-`list` spec miss); no dropped validation; n = 15 runs per arm is too small to show a difference either way. |
| Speed | − (small) | Mean wall time 14.4 s vs 12.2 s (+18%), from extra turns running self-checks; JetBrains measured −11% on larger tasks. |
| Maintainability | + | −37% implementation LOC (5/5 tasks lower), with the cut coming from unused extension hooks and a speculative parser registry; deferrals are recorded as `shortcut:` comments. |
| Safety | neutral / + | Every validation path the prompts required survived (capacity, port/debug checks, TypeError); the security carve-out was not adversarially tested here. |
| Cost Efficiency | − / neutral | +6% cost and −5% output tokens on small tasks; JetBrains reports −10.3% on larger ones, so the sign depends on task size. |
| Verifiability | + | 12/15 runs left a runnable check (baseline 0/15), every reply states what was skipped or not checked, and `shortcut:` markers make deferrals greppable via `ponytail-debt` (3/3 on the planted ledger). |

## Verdict

**CONDITIONAL** — adopt-if: the agent's habitual failure mode is over-building (speculative abstractions, extension points, unrequested format support) **and** you install it as the Claude Code plugin, so the SessionStart hook injects the ruleset. On hidden-test-scored tasks it cut implementation code by 37% (5/5 tasks), held correctness (128/129 vs 129/129) and made output more checkable (runnable self-checks in 12/15 runs vs 0/15). It did not save money on small tasks (+6% cost, +18% wall time). The bare skill under-triggers (1/4), and the audit/debt companions matched but did not beat a direct prompt. It is not ADOPT because the benefit is code shape rather than cost or correctness, because its value on top of an existing "Simplicity First" rule is untested, and because the hook writes under `~/.claude` on every session.

Compared to neighbors: **caveman** compresses the agent's *prose* (a token play); ponytail changes *what gets built* (a code-shape play), and our A/B shows code-shape gains without the token gains. **andrej-karpathy-skills** covers similar ground as a static rule list; if you already run it (or an equivalent CLAUDE.md section), measure ponytail against that before stacking both.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ponytail](https://github.com/DietrichGebert/ponytail) | skill | "Lazy senior dev" pre-write decision ladder (YAGNI → stdlib → native → installed dep → one line → minimum) with explicit safety carve-outs; benchmarked, 14-agent distribution | Agent overengineers — speculative abstractions, unrequested dependencies, boilerplate — instead of writing the minimum code that works | andrej-karpathy-skills, caveman |
