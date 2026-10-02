# Evaluation: playwright-cli

**Repo:** [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli)
**Stars:** 13,735 | **Last updated:** 2026-09-28 (last push) | **License:** Apache-2.0
**Last verified:** 2026-10-02
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Microsoft's token-efficient Playwright CLI plus an agent `SKILL.md` for browser automation and UI verification.

`@playwright/cli` installs a `playwright-cli` binary that drives a persistent headless browser daemon. The agent issues one-shot shell commands (`open`, `goto`, `click e15`, `fill e5 "x"`, `snapshot`, `console`, `eval`, `find`, and storage/tab/network commands). The commands use the same `[ref=eN]` accessibility refs as Playwright MCP. The difference is the delivery channel. MCP returns the accessibility snapshot inline in the tool result. The CLI writes the snapshot to `.playwright-cli/page-*.yml` and prints a short status block with the URL, title, console error count and a link to the snapshot file. The agent then decides how much of that file to load. The bundled skill (`skills/playwright-cli/SKILL.md`, 15.4 KB plus 10 reference files) teaches the command surface. `playwright-cli install --skills` installs it.

The README says this split is the point: CLI plus skill is "more token-efficient" for coding agents because it avoids "large tool schemas and verbose accessibility trees", and MCP is better kept for long exploratory loops. This eval tests that claim against Playwright MCP, the current STACK Verify pick.

## How we tested it

**Evidence:** MEASURED

Verified hands-on on 2026-10-02 with `@playwright/cli@0.1.22` and `@playwright/mcp@0.0.83`, both installed locally via `npm i`. The agent was `claude -p` (Claude Code 2.1.287, `--model sonnet`, which resolves to `claude-sonnet-5-5`), run headless. There were three arms and 5 runs per arm (15 runs in all), executed sequentially so the CLI daemon was never shared. One extra pilot run (`cli-skill-0`) is excluded from every figure.

**Fixture:** a one-page "Acme Shop" app served by `python3 -m http.server 8947`, with **8 planted defects** (the answer key):

| ID | Planted defect |
|----|----------------|
| D1 | "Pricing" nav link → `pricng.html` (404) |
| D2 | "Clear cart" throws `TypeError` (`cart` undefined), so the cart is not cleared |
| D3 | "Add Gadget" adds $10 to the total instead of $15 |
| D4 | Contact form confirmation reads "Thanks, null!" because it reads the wrong field name |
| D5 | Console error on load: `ReferenceError: trackPageview is not defined` |
| D6 | Email input has no label or accessible name (placeholder only) |
| D7 | Icon-only SVG search button has no accessible name |
| D8 | Logo `<img>` has no `alt` attribute |

**Prompt (identical except for the last sentence):** *"A small web app is running at http://127.0.0.1:8947/ . Verify this page works: exercise every interactive feature (links, buttons, forms), check the browser console, and check basic accessibility. You cannot read the app's source files directly; use the browser. When done, report every defect you found as a numbered list under a heading DEFECTS, one defect per line."* Each arm then adds its tool instruction:

- **mcp**: `--mcp-config` with `playwright-mcp --headless --isolated`, `--strict-mcp-config`, `--tools "Read,ToolSearch"`, allow `mcp__playwright`. There is no Bash. In Claude Code the MCP schemas load lazily through ToolSearch, which is the harness default.
- **cli-skill**: the upstream `skills/playwright-cli/` copied into the run directory's `.claude/skills/`, `--tools "Bash,Read,Skill"`, allow `Bash(playwright-cli:*)`.
- **cli-noskill**: the README's "skills-less operation" mode. The prompt adds "Check playwright-cli --help", with `--tools "Bash,Read"` and no skill.

Every arm ran with `--setting-sources project --permission-mode dontAsk --no-session-persistence --output-format stream-json`.

**Oracles:**
- **Recall** is defects found out of 8, scored with one regex per defect over the numbered `DEFECTS` lines. I then hand-audited all 120 run×defect cells. The audit overturned one regex hit: in `cli-skill-4`, the D8 line says the logo "is probably a broken image" and never mentions `alt`. Figures below are after the audit.
- **Tokens and cost** come from the `result` event's `usage` and `total_cost_usd`.
- **Context size** is input + cache-creation + cache-read on the final assistant turn.
- **Wall-clock** is measured around the whole `claude -p` call.
- **Tool calls and tool-result payload** (characters returned to the model) are taken from the stream.

### Results (n=5 per arm; median, range in parentheses)

| Arm | Defects found (sum / 40) | Median per run | Cost USD | Total input tok (incl. cache) | Final-turn context tok | Output tok | Wall-clock s | Tool calls | Tool-result chars |
|-----|---------------|-----|------|------|------|------|------|------|------|
| **Playwright MCP** | **39/40** (D8 missed once) | 8 | **0.065** (0.062–0.093) | 53,954 (42.8K–100.9K) | 12,136 (11.9K–14.5K) | 1,572 | **20.7** (16.5–26.2) | 11 (11–23) | 8,359 |
| **playwright-cli + skill** | **39/40** (D8 missed once) | 8 | **0.100** (0.080–0.119) | 125,093 (70.8K–183.1K) | 18,764 (17.1K–19.8K) | 1,746 | 28.9 (15.8–32.4) | 8 (4–16) | **6,725** |
| playwright-cli, no skill | 36/40 (D8 2/5, D4 4/5) | 7 | **0.049** (0.042–0.079) | 38,370 (29.0K–98.2K) | 10,379 (9.0K–12.4K) | 1,295 | 22.9 (15.2–33.8) | 4 (3–21) | 9,759 |

**Headline:** on this task, playwright-cli + its skill found the same defects as Playwright MCP (39/40 each) and cost **54% more** ($0.100 vs $0.065 median). Its final context was **55% larger** (18.8K vs 12.1K tokens) and it took longer (28.9 s vs 20.7 s). The CLI did deliver what it promises at the tool-result level: **20% fewer characters** came back from the browser (6.7K vs 8.4K). The skill itself cancels that saving. Loading `SKILL.md` grew the context from 8,196 to 14,248 tokens in a single step in `cli-skill-1`, and that ~6K-token body is re-sent on every later turn. The skill also adds ~3K tokens to the very first turn (8,196 vs 5,192 for the no-skill CLI), which is its listing plus the Skill tool. Without the skill the CLI is the cheapest arm (−25% vs MCP), but recall drops to 36/40.

## Test design

- **Task/corpus:** the one-page planted-defect fixture above (8 defects, answer key fixed before any run) plus the prompt quoted above. Files are in the eval scratch dir `scratchpad/evals/pwcli/{site/,DEFECTS.md,run.sh,analyze.py}`, which is outside the repo. The fixture is small enough to rebuild from the defect table.
- **Baseline:** Playwright MCP (`@playwright/mcp@0.0.83`), the STACK Verify pick, on the same model, prompt, fixture and permission scope. A second baseline is the same CLI without its skill, which isolates what the skill contributes.
- **Metric:** recall k/40 with each arm vs MCP (Correctness protocol). Median and range over N=5 for cost, tokens and wall-clock (Speed and Cost protocols).
- **Reproduce:** start `python3 -m http.server 8947` in `site/`, run `./run.sh <mcp|cli-skill|cli-noskill> <rep>` for reps 1–5, then `python3 analyze.py`.

### Test design — skills (required when Type is skill or plugin)

- **Triggering:** should-fire 5/5. The `Skill` tool was invoked with `playwright-cli` as the first action in every cli-skill run. The prompt named `playwright-cli`, so this is the easy case. Shouldn't-fire prompts were out of scope for this run and were not measured. The skill's `description` ("Automate browser interactions, test web pages and work with Playwright tests") is broad enough that over-triggering on general Playwright-test work is plausible.
- **Output A/B:** compared with-skill and no-skill on the same prompt. The skill raised recall from 36/40 to 39/40; the gain is mostly D8, the missing `alt`, at 4/5 vs 2/5. The skill steers the agent toward `--raw eval` DOM queries, and those are what surface attribute-level a11y defects. The cost was +104% ($0.100 vs $0.049) and +6 s median wall-clock.

```bash
# install (local, no global)
npm i @playwright/cli@0.1.22 @playwright/mcp@0.0.83
./node_modules/.bin/playwright-cli --version          # 0.1.22

# smoke: what the CLI returns to the agent
playwright-cli open http://127.0.0.1:8947/
# ### Page
# - Page URL: http://127.0.0.1:8947/
# - Console: 2 errors, 0 warnings
# ### Snapshot
# - [Snapshot](.playwright-cli/page-2026-10-02T19-25-45-909Z.yml)   <- tree goes to a file, not the context

# one arm-run (cli-skill shown)
claude -p "$PROMPT Use playwright-cli (via Bash) for browser access." --model sonnet \
  --setting-sources project --permission-mode dontAsk --no-session-persistence \
  --output-format stream-json --verbose --mcp-config empty-mcp.json --strict-mcp-config \
  --tools "Bash,Read,Skill" --allowedTools "Bash(playwright-cli:*)" "Read" "Skill"
```

## What worked

- **Recall matched MCP.** CLI + skill found every planted defect in 4/5 runs, the same as MCP. It confirmed D2 and D3 by clicking and reading `#total`, not by guessing. There were no differences on the behavioural defects (D1–D5); both arms got all 25.
- **The file-backed snapshot works as advertised.** `open`/`click` return a short status block plus a snapshot path. Per-call payload to the model is smaller, with tool-result characters 20% under MCP. Agents used `--raw eval "…"` and `head` on the `.yml` to pull only what they needed.
- **It works with no skill at all.** The README's "point your agent at `--help`" mode found 36/40 at the lowest cost of any arm ($0.049). The `--help` output is a usable interface on its own.
- **Commands chain in one shell call.** Agents batched 3–5 interactions per Bash call (`click e20 >/dev/null; click e20; eval …`), which is how the CLI arms needed fewer tool calls than MCP (4–8 median vs 11).

## What didn't work or surprised us

- **The skill outweighs the saving it exists to deliver.** The README's efficiency argument assumes MCP pays for "large tool schemas". Claude Code already defers MCP schemas behind ToolSearch, so the MCP arm started at 4,786 context tokens, below even the no-skill CLI arm (5,192). Meanwhile the skill's ~6K-token body is loaded once and then re-sent every turn. On a 4–16-call verification session, that fixed cost exceeds the per-call snapshot savings. **The token-efficiency claim did not hold end-to-end in Claude Code on this task.** It might hold in a much longer session, where per-step payload savings compound, or in a harness that loads full MCP schemas eagerly. Neither condition was part of this run.
- **Shell access widens the attack surface and adds friction.** With `Bash(playwright-cli:*)` as the only allow rule, **10/10** CLI runs had at least one command denied. Agents reached for `curl` to check link status codes, and some compound `;`-chained lines were rejected by the matcher. Each denial cost a turn. The MCP arm had 0 denials because it has no shell. Granting the CLI broadly (`Bash`) removes the friction but gives a browser-verification agent arbitrary shell access.
- **Defects were sometimes reported from source rather than observed.** In 3/10 CLI runs (`cli-noskill-4`, `cli-skill-4`, and partly `cli-noskill-3`), the agent used `eval` to dump the inline script and reported D3/D4 "from the code" without clicking. MCP runs also used `browser_evaluate`, but in the MCP reports source-derived claims were usually paired with an observed value ("I clicked it once and the total showed 10"). That is a Verifiability concern: "found in the script; not clicked" is a weaker claim than "the total showed 10 after one click".
- **Wall-clock was slower, not faster.** The median was 28.9 s vs 20.7 s for MCP. The extra Skill load turn and the denial retries account for most of the gap.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | 39/40 planted defects found by CLI + skill, the same as Playwright MCP (39/40). Without the skill, 36/40. |
| Speed | − | Median 28.9 s vs 20.7 s for MCP (n=5 each), with the skill-load turn and permission-denial retries adding turns. |
| Maintainability | neutral | Same ref model and Playwright engine as MCP. A shell CLI is easier to script into CI or `Makefile` checks than an MCP session. |
| Safety | − | Needs Bash. A narrow allow rule caused denials in 10/10 runs, and a broad one hands the verifier a shell. The MCP arm needs no shell. |
| Cost Efficiency | − | +54% cost ($0.100 vs $0.065 median) and +55% final context vs MCP, because the ~6K-token skill body outweighs a 20% smaller tool-result payload. Without the skill it was −25%, but with lower recall. |
| Verifiability | − | Snapshots land in files the human can open later, but `eval`-dumping the script let 3/10 CLI runs report defects from the source without observing them. MCP reports usually paired claims with observed values. |

## Verdict

**CONDITIONAL** — adopt-if: your agent harness loads MCP tool schemas eagerly (no deferred tool search), you cannot run an MCP server, or you want browser checks as plain shell commands in scripts/CI. In those cases, use it **without** the bundled skill or with a trimmed one, alongside Playwright MCP rather than replacing it.

It should **not replace Playwright MCP in STACK**. In a measured head-to-head in Claude Code (5 runs per arm, 8 planted defects), CLI + skill matched MCP's recall (39/40 each) while costing 54% more, running 40% slower, and requiring shell access. Microsoft's token-efficiency claim holds only at the per-tool-result level (−20% payload). The skill's own context cost cancels it, and Claude Code's deferred MCP schemas remove the other half of the argument. Apache-2.0 clears the license bar. Re-evaluate on a long multi-page verification session (≥50 browser actions), where the per-step saving has room to compound.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [playwright-cli](https://github.com/microsoft/playwright-cli) | tool | Microsoft's token-efficient Playwright CLI plus agent SKILL.md for browser automation and UI verification | Playwright MCP's accessibility-tree payloads bloat agent context on long browser-verification sessions | playwright, agent-browser, chrome-devtools-mcp |
