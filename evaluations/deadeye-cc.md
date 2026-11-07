# Evaluation: deadeye-cc

**Repo:** [deepaksinghcs14/deadeye-cc](https://github.com/deepaksinghcs14/deadeye-cc)
**Stars:** 3 | **Last updated:** 2026-08-06 (pushed, per repo-metadata.json) | **License:** MIT
**Last verified:** 2026-11-07
**Last triaged:** 2026-11-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (plugin/hooks)

---

## What it does

A Claude Code plugin that fits the model, effort, and context window to each task through a
deterministic, hooks-based policy kernel — every number it reports is measured, not
estimated.

Mechanically it is a Go binary (`cmd/deadeye`, ~15.5K lines, 83 `_test.go` files) driven by Claude Code hooks (`SessionStart`, `UserPromptSubmit`, `PreToolUse` on `Agent` and on `Bash|Edit|Write|Read|Grep|WebFetch|Workflow`, `PostToolUse`, `SubagentStart`). `PreToolUse` on Bash rewrites a noisy command (tests, builds, linters, installs) before it runs so only the useful part reaches context; `PreToolUse` on `Agent` recommends (or, in `enforce` mode, sets) a subagent's model and effort; a coder persona, an exfiltration guard, a plan-first gate and a codebase map ride along. State lives in `~/.deadeye/`; the README says no hosted service, API key or telemetry. It also targets Codex, Gemini CLI, Cursor and Windsurf with fewer features each.

## How we tested it

**Evidence:** REVIEW

**Source-grounded review — not run hands-on.** The binary was not built or run: this unattended sandbox's permission classifier refused `go build` of the freshly cloned upstream source (code from an external repo), and the plugin's own route downloads a release binary on first use, so no route to a running instance was available. A model-driven check also needs a Claude login that the sandbox does not have. What was examined: a shallow clone of the repo at commit `2fdc78b` (2026-10-31), its README, `hooks/hooks.json`, `.claude-plugin/plugin.json` (version 0.82.3), `Makefile`, and the committed routing benchmark (`benchmarks/routing/README.md`, `results/summary.md`). Every figure below is the vendor's own, quoted from those files, not measured here.

```
Commands actually run (read-only):
git clone --depth 1 https://github.com/deepaksinghcs14/deadeye-cc   # source fetch only
sed / head over README.md, hooks/hooks.json, benchmarks/routing/*    # reading
(go build ./cmd/deadeye  -> denied by the sandbox permission classifier; nothing built)
```

Vendor claims, as published:

- README "Numbers" table (real runs, vendor-logged): `go test` with one failure 485 B → 99 B (79.6%); the repo's own 202-line passing suite 10,301 B → 55 B (99.5%); `npm install express mocha` 553 B → 55 B (90.1%); coder persona per subagent spawn 9,499 B → 1,099 B (88.4%).
- `benchmarks/routing/results/summary.md`: 6 pilot tasks (1 mechanical, 2 standard, 3 hard) run on haiku/sonnet/opus with `claude -p`, graded by hidden `go test`s, real billed cost. Oracle routing (cheapest passing tier) cost $0.619 against $1.796 all-opus, 66% saved; the file itself calls this the *ceiling*, not what the router achieves, and reports one task (`h5-expr`) failing on every tier.

## Test design

- **Task/corpus:** none run by us. The vendor's corpus is 6 self-contained Go tasks with hidden tests (`benchmarks/routing/tasks`), plus the three command-output cases above.
- **Baseline:** vendor's is everything-on-opus (routing) and untrimmed output (hygiene).
- **Metric:** vendor's are billed `total_cost_usd` plus pass/fail on a hidden test, and bytes before/after.
- **Reproduce:** `go build -o bin/deadeye ./cmd/deadeye` then, per the vendor, `benchmarks/routing/run.sh` (needs a Claude login and spends real money) and `python3 benchmarks/routing/summarize.py`. A hands-on pass should first check the output-trimming claim alone, since it needs no model credentials: pipe a planted-failure `go test` log and an `npm install` log through the PreToolUse hook and count bytes and whether the failing test name survives.

### Test design — skills (required when Type is skill or plugin)

- **Triggering:** not run. The plugin is hook-driven rather than description-triggered, so the relevant analogue is whether the `Bash` rewrite fires on test/build/install commands and stays out of the way on others; unmeasured here.
- **Output A/B:** not run. The vendor's with/without byte counts above are the only A/B on record.
- **Not run?** Stated at the top of this section: nothing was installed or exercised.

## What worked

- The repo is unusually checkable for a 3-star project: a committed benchmark with the method, task set, hidden-test grading and raw `results.jsonl`, and a summary that retires its own earlier claim (an `h5-expr` pass that two later sweeps failed to reproduce).
- Honest framing in the vendor's own results: the 66% routing figure is labelled the oracle ceiling, not the realized saving, and a realized-cost router arm is reported separately.
- The failure posture is stated and designed in: on an internal error the hooks pass the call through untouched, it advises by default, and it never edits `settings.json`.
- Active: 0.82.3, last commit 2026-10-31, after the 2026-08-06 push date in our cached metadata.

## What didn't work or surprised us

- The output-trimming numbers are the vendor's single runs on its own repo and three commands; there is no corpus, so the 79.6–99.5% range is an existence proof, not an expected saving. A 99.5% cut on an all-passing suite says little about whether a *failing* log keeps the lines an agent needs.
- Rewriting a command before it runs means the agent never sees the dropped output. Whether it ever needs it back is the correctness risk, and only a hands-on run can price it.
- The routing figure comes from a Go-only 6-task pilot where routing wins on the cheapest tier passing; transfer to other languages or larger tasks is unmeasured.
- Scope is wide for one plugin (ten controls, coder persona, review commands, codebase map, themes, a mod), which raises the surface to audit and overlaps with several separately catalogued tools.
- The README advertises a waitlist banner for an unspecified upcoming product.
- Our repo-metadata snapshot (fetched 2026-08-07) predates the latest commit; refresh before relying on its activity figures.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral (unknown) | Trimming and routing both risk hiding or under-powering; the vendor's one hard task failed on all tiers, and no run here prices the risk. |
| Speed | neutral | Hooks add per-call latency (5–15 s timeouts declared); the README quotes about 2.5 s for the routing judge; nothing measured here. |
| Maintainability | neutral | MIT, Go, 83 test files and an active release stream, but a very wide surface for one maintainer. |
| Safety | + (claimed) | Exfiltration guard turns credential reads into permission prompts; fail-open on internal errors; unverified here. |
| Cost Efficiency | + (claimed) | Vendor reports 66% oracle routing saving and 79.6–99.5% output cuts; all vendor-measured. |
| Verifiability | + | Committed raw results, hidden-test grading and a per-decision log (`~/.deadeye/decisions.jsonl`, `/deadeye-route`) let a human re-check each claim. |

## Verdict

**discovery-log — tentative read** — source reading only; the sandbox refused to build the Go source and no Claude login was available, so no hands-on number backs the vendor's savings. It is a differently-timed optimization from claude-code-router, litellm and codeburn (decides before the spend, not after), and the benchmark discipline is a point in its favour, so the next pass should build it where execution is allowed and measure output trimming on a planted-failure log, which needs no model key.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deadeye-cc](https://github.com/deepaksinghcs14/deadeye-cc) | plugin | Claude Code plugin (MIT) that fits the model, effort, and context window to each task via a deterministic hooks-based policy kernel — every number it reports is measured, not estimated | Manually picking model/effort per task wastes tokens on easy work or under-powers hard tasks; want an automatic, measured fit instead | claude-code-router, litellm, codeburn |
