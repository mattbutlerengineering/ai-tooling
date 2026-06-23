# Evaluation: evalview

**Repo:** [hidai25/eval-view](https://github.com/hidai25/eval-view)
**Stars:** 117 | **Last updated:** 2026-06-15 | **License:** Apache-2.0
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Catalog one-liner: "AI agent regression testing." EvalView is a Python framework (PyPI `evalview`, v0.8.0) that snapshots an AI agent's behavior — tool calls, call order, parameters, and output — as a golden baseline, then diffs subsequent runs against that baseline to catch *behavior* regressions that a passing health check or HTTP `200` would miss. Its tagline is "Think Playwright, but for tool-calling and multi-turn AI agents."

The mechanism is a three-command loop: `evalview init` auto-detects the agent type (chat/tool-use/multi-step/rag/coding) and scaffolds a starter suite; `evalview snapshot` records traces as baselines; `evalview check` replays the tests, diffs against the baseline, and emits a graded ship/don't-ship verdict (`SAFE_TO_SHIP` / `SHIP_WITH_QUARANTINE` / `INVESTIGATE` / `BLOCK_RELEASE`). Scoring has four layers, the first two free and offline: exact tool-call+sequence diff, code-based checks (regex/JSON-schema/contains), embedding semantic similarity (~$0.00004/test), and optional LLM-as-judge (~$0.01/test). Beyond detection it adds drift trend analysis (`drift`, OLS slope + sparklines), model-drift canary (`model-check`, zero-judge structural probe against a provider to catch silent model updates), record/replay cassettes for hermetic CI, auto-heal (retry flakes / propose variants / hard-fail structural changes), flake quarantine governance, and `autopr` (turn a production incident into a pinned regression test + PR).

The **MCP server** — the form this catalog entry references — is one of several integration surfaces, not the whole product. `claude mcp add --transport stdio evalview -- evalview mcp serve` exposes 8 tools to Claude Code: `create_test`, `run_snapshot`, `run_check`, `list_tests`, `validate_skill`, `generate_skill_tests`, `run_skill_test`, `generate_visual_report`. The pitch: ask Claude "did my refactor break anything?" and it runs `run_check` inline. The same engine is also reachable as a CLI, a Python API (`gate()`/`gate_async()`), a pytest plugin, and a GitHub Action (`hidai25/eval-view@v0.8.0`).

## How we tested it

**Evidence:** REVIEW

Not hands-on tested. This is an **architecture / source-review** evaluation based on the repository README (46.7 KB, read in full), repository metadata via the GitHub API, the PyPI/npm package listing, and the repo's own positioning docs. No `pip install evalview`, no `evalview mcp serve`, and no agent regression run were performed — stating this honestly per the integrity rule; the verdict is calibrated against that limitation.

Repo identification was the first task because the catalog entry was unlinked and carried no URL. The catalog hint ("agent-regression-testing MCP server, overlaps langfuse") matched, and the repo was positively verified:

```
gh search repos evalview --limit 20 --json fullName,description,url,stargazersCount
# → surfaced hidai25/evalview_landing_page + hidai25/evalview-support-automation-template

gh api repos/hidai25/eval-view --jq '{full_name, description, stars, pushed_at, license, topics}'
# → full_name "hidai25/eval-view" (renamed from EvalView), 117 stars, Apache-2.0,
#   description "Regression testing for AI agents. Snapshot behavior, diff tool calls,
#   catch regressions in CI. Works with LangGraph, CrewAI, OpenAI, Anthropic."
#   topics include: mcp, regression-testing, agent-evaluation, agentic-ai, ai-agents

npm view evalview        # description confirms "...and MCP", maintainer hidai25, v0.8.0
gh api repos/hidai25/eval-view/readme   # README header: <!-- mcp-name: io.github.hidai25/evalview-mcp -->
```

Three converging signals confirm the identity: the renamed canonical repo `hidai25/eval-view` carries the `mcp` + `regression-testing` topics; its README declares the MCP server name `io.github.hidai25/evalview-mcp` and documents the 8-tool `evalview mcp serve` command; and the satellite repos (`evalview_landing_page`, `evalview-support-automation-template`) by the same author both point back to it. Identity is **high confidence**.

```
# Commands actually run for this evaluation (identification + review only):
gh search repos evalview --limit 20 --json fullName,description,url,stargazersCount
gh api repos/hidai25/eval-view --jq '{full_name,description,stars,pushed_at,license,topics,forks,open_issues}'
gh api repos/hidai25/eval-view/readme --jq '.content' | base64 -d
npm view evalview --json
```

## What worked

- **Repo positively identified despite the unlinked catalog entry.** `hidai25/eval-view` is the right repo: 117 stars, Apache-2.0, Python, last push 2026-06-15 (active), 21 forks, 7 open issues. The MCP-server framing in the catalog is accurate — `evalview mcp serve` is real and documented with a concrete 8-tool surface.
- **The problem is real and under-served.** "Agent returns 200 and is still wrong" — silent tool-choice/output drift after a model or prompt change — is a genuine gap that ordinary tests and uptime checks do not cover. The trajectory diff (tool names + parameters + order, not just final output) is the differentiating primitive and the right level to gate on.
- **Free, offline, deterministic core.** The tool+sequence diff and code-based checks run with no API key and no LLM cost. That makes the regression gate cheap enough for a per-commit / pre-push hook, which is exactly where a Verify-stage gate belongs.
- **Strong Claude Code fit on paper.** Native MCP server, an `AGENTS.md` architecture map, agent recipes, a `CLAUDE.md.example`, and explicit "Claude Code ✅ E2E + trace capture" support. The `validate_skill` / `generate_skill_tests` / `run_skill_test` MCP tools specifically target Claude Code skills testing — directly relevant to this repo's domain.
- **Graded verdicts, not binary alarms.** Drift is classified `low/medium/high` and the verdict distinguishes "the provider changed" (model-check / runtime fingerprint) from "my system regressed." This is more useful than a pass/fail bit and addresses the real triage question.
- **Complements rather than competes with langfuse.** EvalView is a merge-time *gate*; langfuse is a production *observability/eval platform*. The README's own comparison table positions them as run-together tools, which matches the catalog's overlap marker.

## What didn't work or surprised us

- **No hands-on verification of any claim.** Verdict tiers, "92% claimed" numbers are absent here (good — none invented), but pass-rate, latency, false-positive, and auto-heal behavior are all README assertions only. The four-tier verdict, auto-variant clustering, and noise-tracker math are plausible but unverified.
- **Modest maturity.** 117 stars, single primary maintainer (`hidai25`), v0.8.0 (pre-1.0). Small blast radius if it stalls because the core CLI is local and free, but it is not a battle-tested dependency the way langfuse (large platform) is.
- **MCP is a thin wrapper over a CLI-first tool.** The product's center of gravity is the CLI + pytest + GitHub Action. The 8-tool MCP surface is convenient inside Claude Code but adds little the CLI can't do; an agent could just shell out to `evalview check`. The MCP server is a nice-to-have, not the reason to adopt.
- **Setup cost is non-trivial for the catalog's primary use case.** To gate *this* (a docs-only repo) there is nothing to test — EvalView only pays off when you own a tool-calling/multi-turn agent with a stable enough spec to baseline. That makes it niche relative to general-purpose catalog tools.
- **`evalview` namespace is noisy.** Multiple unrelated `evalview` repos exist (a 2021 `evalview/app` landing page, a DUNE numeric library). The unlinked catalog entry was genuinely ambiguous until the README MCP marker pinned it down — worth linking the entry to remove that ambiguity.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Trajectory + output baseline diffing catches silent agent regressions normal tests miss (the core value prop; mechanism verified in README, outcomes not benchmarked here) |
| Speed | neutral | Free deterministic tier is sub-second / watch-mode friendly, but adds a baseline-maintenance step to the loop |
| Maintainability | + | Pinned baselines + `autopr` turn production incidents into committed regression tests, growing a safety net over time |
| Safety | + | `forbidden_tools` hard-fail contracts and `gate: strict` first-failure alerting guard against dangerous tool calls |
| Cost Efficiency | neutral | Core diff is $0 offline; LLM-judge and semantic tiers cost per-test (~$0.01 / ~$0.00004) and a budget circuit-breaker exists, but value scales only with how much agent behavior you actually baseline |

## Verdict

**CONDITIONAL**

Adopt when you build, ship, or maintain a real tool-calling or multi-turn AI agent and need a merge-time regression gate — that is exactly the Verify-stage gap EvalView fills, and its free offline tool/sequence diff is cheap enough to run per-commit. For a documentation-only repo like this one there is no agent to baseline, so it is not part of the recommended STACK here; this evaluation establishes the catalog entry's identity and scope. EvalView and langfuse are complementary, not competing: langfuse for production observability/eval, EvalView for the pre-merge behavior gate — many teams run both. The verdict is CONDITIONAL rather than ADOPT primarily on maturity (117 stars, v0.8.0, single maintainer) and because the value is contingent on owning an agent worth regression-testing; the MCP server specifically is a convenience layer over a stronger CLI/pytest/GitHub-Action core. Re-evaluate hands-on if a coding-agent project in scope acquires a stable tool-calling spec.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [evalview](https://github.com/hidai25/eval-view) | MCP server | AI agent regression testing | Can't tell if agent behavior regressed after config changes | langfuse (complementary: langfuse = production observability/eval, evalview = pre-merge behavior gate) |
