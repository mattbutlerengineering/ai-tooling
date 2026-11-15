# Evaluation: deadeye-cc

**Repo:** [deepaksinghcs14/deadeye-cc](https://github.com/deepaksinghcs14/deadeye-cc)
**Stars:** 3 | **Last updated:** 2026-08-06 (pushed, per repo-metadata.json) | **License:** MIT
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (plugin/hooks)

---

## What it does

A Claude Code plugin that fits the model, effort, and context window to each task through a
deterministic, hooks-based policy kernel — every number it reports is measured, not
estimated.

Mechanically it is a Go binary (`cmd/deadeye`, ~15.5K lines, 83 `_test.go` files) driven by Claude Code hooks (`SessionStart`, `UserPromptSubmit`, `PreToolUse` on `Agent` and on `Bash|Edit|Write|Read|Grep|WebFetch|Workflow`, `PostToolUse`, `SubagentStart`). `PreToolUse` on Bash rewrites a noisy command (tests, builds, linters, installs) before it runs so only the useful part reaches context; `PreToolUse` on `Agent` recommends (or, in `enforce` mode, sets) a subagent's model and effort; a coder persona, an exfiltration guard, a plan-first gate and a codebase map ride along. State lives in `~/.deadeye/`; the README says no hosted service, API key or telemetry. It also targets Codex, Gemini CLI, Cursor and Windsurf with fewer features each.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed via `go build` from the upstream source at commit `2fdc78b` (2026-10-31, plugin 0.82.3) with Go 1.24.7 on Linux, fed the real `deadeye hook PreToolUse` binary Claude Code's PreToolUse JSON for `Bash` commands, executed the original command (baseline arm) and the rewritten `updatedInput.command` it returned (treatment arm) in the same directory, and scored output bytes, exit code and whether the three planted failures stay visible. Scope of the measurement: the output-trimming (context hygiene) claim only.

```
git clone --depth 1 https://github.com/deepaksinghcs14/deadeye-cc   # 2fdc78b
go build -o deadeye ./cmd/deadeye                                    # 18.8s, 14.5 MB binary
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","cwd":...,"tool_input":{"command":"go test -v ./..."}}' | deadeye hook PreToolUse

fixture: 40-test Go package and 40-test pytest file, each with 3 planted failures (07, 19, 33), 3 log lines per test
cmd                          raw     trimmed  cut      exit raw/trim  planted failures visible
go test ./...                578 B   578 B    0.0%     1/1            3/3   (3 repeat runs, identical)
go test -v ./...             6589 B  1064 B   83.9%    1/1            3/3
pytest                       2039 B  1843 B   9.6%     1/1            3/3
pytest -v                    5247 B  4088 B   22.1%    1/1            3/3
all-pass Go, go test ./...   15 B    56 B     -273.3%  0/0            n/a
all-pass Go, go test -v ./.. 6451 B  56 B     99.1%    0/0            n/a
echo hello                   -> not rewritten (empty updatedInput)
go test ./... | tail -5      -> not rewritten (pipeline left alone)
```

The first hook call in a fresh `HOME` printed `{}` (no rewrite); every call after that rewrote.

## Test design

- **Task/corpus:** two generated fixtures under `/tmp/eval-deadeye-cc/fx` (40 tests each, failures at tests 07, 19, 33), plus an all-pass copy of the Go one. `npm install` and routing cases were out of reach offline and without a model login, so they are outside this measurement.
- **Baseline:** the original command run directly. **Treatment:** the command string the hook returns as `updatedInput.command`.
- **Metric:** bytes of combined output (`wc -c`), exit code equality, count of planted failure names present in trimmed output; mechanical, no judgement.
- **Reproduce:** build as above, generate the fixtures with the loop-numbered tests, then pipe the PreToolUse JSON through `deadeye hook PreToolUse` and run the returned command next to the original.

### Test design — skills (required when Type is skill or plugin)

- **Triggering:** the rewrite fires on `go test` and `pytest` (with and without `-v`) and stays out of the way on `echo` and on a piped command: 4 of 4 expected rewrites, 2 of 2 expected passthroughs on this small set.
- **Output A/B:** the table above is the with/without comparison, applied to command output rather than to model prose.
- **Model-driven checks:** routing and persona behaviour need a Claude login this environment lacks; unmeasured here.

## What worked

- The repo is unusually checkable for a 3-star project: a committed benchmark with the method, task set, hidden-test grading and raw `results.jsonl`, and a summary that retires its own earlier claim (an `h5-expr` pass that two later sweeps failed to reproduce).
- Honest framing in the vendor's own results: the 66% routing figure is labelled the oracle ceiling, not the realized saving, and a realized-cost router arm is reported separately.
- The failure posture is stated and designed in: on an internal error the hooks pass the call through untouched, it advises by default, and it never edits `settings.json`.
- Active: 0.82.3, last commit 2026-10-31, after the 2026-08-06 push date in our cached metadata.

## What didn't work or surprised us

- Plain `go test ./...` was left byte-for-byte at 578 B; with all tests passing the "trimmed" form is larger than the original (56 B against 15 B), because it replaces `ok  fx 0.003s` with a sentence. The savings only exist on verbose runs.
- pytest saved 9.6% (default) and 22.1% (`-v`) because the filter keeps `-B 3 -A 5` context around every line matching `FAIL|Error|assert`, so a three-failure run keeps most of its traceback text.
- On the passing run the pass summary is dropped entirely: the agent sees "command exited 0, no output survived filtering", not the package timing or test counts. Exit codes matched in every run, so this is lost information, not a lost signal.
- The Go `-v` cut also keeps unrelated `--- PASS` and log lines inside the context window of each failure.
- Rewrite of an unmatched command is a no-op, and the first call in a fresh `HOME` returned `{}`; the cause is unexplored.
- Routing (66% oracle saving), the exfiltration guard and the persona figures remain the vendor's own claims; scope is wide for one plugin and overlaps several catalogued tools. Our metadata snapshot (fetched 2026-08-07) predates the latest commit.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Measured: all 3 planted failures stayed visible in all 4 failing-run cases and exit codes matched; routing correctness is unmeasured. |
| Speed | neutral | Hooks add per-call latency (5–15 s timeouts declared); the README quotes about 2.5 s for the routing judge; nothing measured here. |
| Maintainability | neutral | MIT, Go, 83 test files and an active release stream, but a very wide surface for one maintainer. |
| Safety | + (claimed) | Exfiltration guard turns credential reads into permission prompts; fail-open on internal errors; unverified here. |
| Cost Efficiency | + (conditional) | Measured here: 0% to 83.9% cut on failing runs depending on command and verbosity, 99.1% on a verbose passing run, negative on a terse one; routing saving is vendor-only. |
| Verifiability | + | Committed raw results, hidden-test grading and a per-decision log (`~/.deadeye/decisions.jsonl`, `/deadeye-route`) let a human re-check each claim. |

## Verdict

**discovery-log — tentative read** — measured on output trimming only: a verbose `go test -v` run shrank 83.9% (99.1% when passing) with every planted failure kept and exit codes intact, but default `go test` saved 0%, pytest 9.6–22.1%, and a terse passing run grew. The routing and persona claims need a model login that was not available, and it overlaps claude-code-router, litellm and codeburn, so there is no basis for a promotion call; a next pass with a Claude login should measure routing cost against the committed `benchmarks/routing` tasks.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deadeye-cc](https://github.com/deepaksinghcs14/deadeye-cc) | plugin | Claude Code plugin (MIT) that fits the model, effort, and context window to each task via a deterministic hooks-based policy kernel — every number it reports is measured, not estimated | Manually picking model/effort per task wastes tokens on easy work or under-powers hard tasks; want an automatic, measured fit instead | claude-code-router, litellm, codeburn |
