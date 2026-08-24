# Evaluation: Promptfoo

**Repo:** [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)
**Stars:** 24,503 | **Last updated:** 2026-08-24 (last push) | **License:** MIT | **Language:** TypeScript (npm/brew/pip)
**Last verified:** 2026-08-23
**Dev loop stage:** Observability / Verify — LLM eval, red-teaming, CI/CD gating
**Layer:** Tooling (CLI + library + web viewer)

---

## What it does

Promptfoo is **a CLI and library for evaluating and red-teaming LLM apps** — "stop the trial-and-error approach, start shipping secure, reliable AI apps." Core capabilities: **automated evaluations** of prompts/models with declarative configs; **side-by-side model comparison** (OpenAI, Anthropic, Azure, Bedrock, Ollama, and more); **red teaming / vulnerability scanning** for AI security with a dashboard; **CI/CD integration** for automated checks; **PR code scanning** for LLM-related security/compliance issues; and result sharing. Install via `npm i -g promptfoo`, `brew install promptfoo`, `pip install promptfoo`, or `npx promptfoo@latest`. As of the README, **Promptfoo is now part of OpenAI** (remains open source, MIT) and is **used by OpenAI and Anthropic**.

## How we tested it

**Evidence:** RUN

**Method: installed `promptfoo@0.122.0` and ran a real, complete evaluation with no model credentials at all**, using an `exec:` provider — a deterministic shell script standing in for an LLM — so the assertion engine could be exercised and *falsified* rather than described.

The previous review's stated reason for not running it was cost and setup: *"Real setup for real value… Cost of running evals… comparing models across many cases is inference spend."* That is true of comparing models and false of exercising the tool. A provider is a config line, and `exec:` makes it a shell script.

```bash
npm i promptfoo@0.122.0                       # 35s, 1.7 GB of node_modules
# providers: [{ id: "exec:./fake-model.sh" }]  — a bash script, not a model
promptfoo eval -c promptfooconfig.yaml --no-cache -o result.json
echo $?                                        # 100
promptfoo redteam generate -c promptfooconfig.yaml -o redteam.yaml
```

**The eval half works, credential-free, and it discriminates.** Five test cases against the fake provider in **1,305 ms** at concurrency 4. Two of the five were *designed to fail* — a `contains: Tokyo` against a provider hard-coded to answer "Kyoto", and a `javascript` assertion asserting the wrong city — and the run returned exactly `✓ 3 passed (60%) / ✗ 2 failed (40%) / 0 errors`. Six assertion types were exercised and every one landed correctly: `contains`, `not-contains`, `regex`, `is-json`, `javascript`, `equals`. Token usage read `total: 0` across `numRequests: 5`, which is the point — the harness ran, the model did not.

**CI gating is real: exit code 100 with failures present**, and `-o result.json` writes a genuinely useful structure — per-row `gradingResult.componentResults[]` carrying `pass`/`score`/`reason` and the originating `assertion` object, plus `stats`, `latencyMs`, `cost` and `tokenUsage`. This is CI-consumable without post-processing.

**The red-teaming half is gated behind vendor email verification.** `promptfoo redteam generate` prints:

```
  Red team scans require email verification to continue.
? Work email:
```

and its behaviour then splits by TTY:

| context | result |
|---|---|
| interactive terminal | **blocks indefinitely** — the first attempt ran **9 m 50 s and flushed zero bytes** before being killed |
| non-TTY (the CI case) | rc=1 in 1,260 ms — but via a Node `Detected unsettled top-level await` warning, not a clean error |

The escape hatch is the `PROMPTFOO_AUTHOR` environment variable, and the module that reads it talks to `https://api.promptfoo.app`. **Deliberately not exercised:** sending an email address to a vendor API is not something to do unattended to find out what happens, and the gate's existence is the finding either way.

**Footprint, measured:** `npm i promptfoo` pulls **1.7 GB** into `node_modules` in ~35 s. The package declares `"node": ">=22.22.0"` — a hard and very recent floor; this machine is on v22.22.3, three patch versions above it.

**Breadth, counted:** `redteam generate --help` lists ~79 plugins (`harmful:*`, `pii:*`, `owasp:*`, protocol and agentic categories).

**Upstream re-checked:** 24,503 stars (the header said 22,392), pushed the day this was written, **2,403,971 npm downloads/month**, v0.122.0, 522 open issues. The README confirms at line 23 that Promptfoo is now part of OpenAI and remains MIT.

**Not exercised:** any real model provider, model-graded assertions (`llm-rubric`, `factuality`, `answer-relevance` — all of which need an LLM grader), the red-team scan itself, `promptfoo view`, the web viewer, sharing, PR code-scanning, and every non-`exec` provider.

## Test design

- **Task/corpus:** 5 declarative test cases against one `exec:` provider — a bash script whose output is fixed by input, so the "model" is a constant and the only variable is the assertion engine.
- **Control:** **two of the five cases are planted failures.** Without them a green run proves nothing — an assertion engine that returns `pass` unconditionally would look identical. Getting exactly 2 failures, on exactly the 2 planted cases, is what makes the other 3 passes evidence.
- **Metric:** pass/fail per assertion against the designed outcome, wall-clock for the run, and the process exit code.
- **Reproduce:** the block above plus the two fixture files. Deterministic, offline, no API keys, pinned to `promptfoo@0.122.0`.
- **One fixture bug, caught and fixed rather than reported.** The first run showed the `is-json` case failing; the cause was my own bash `case` ordering (`*capital*France*` matched before `*json*`), not the tool. Reordering the branches produced the designed 3/2 split. A planted-failure design is only trustworthy if the *unplanted* failures get chased down.

## What worked

- **The eval half needs no model credentials at all, and that is a bigger deal than it sounds.** An `exec:` provider turns any script into a "model", so the assertion engine can be developed, tested and CI-gated for free — and so can *this* evaluation. Five cases in **1,305 ms**, `total: 0` tokens across 5 requests.
- **The assertion engine discriminates, proven by planted failures.** `contains`, `not-contains`, `regex`, `is-json`, `javascript`, `equals` — six types, and the run returned exactly the designed 3-pass/2-fail split with the failures on exactly the two planted cases.
- **CI gating is real and needs no glue: rc=100** when assertions fail. The JSON output carries per-assertion `pass`/`score`/`reason` alongside the assertion object itself, plus `stats`, `latencyMs` and `cost` — consumable by a pipeline as-is.
- **Genuinely the category standard, by the number the previous review lacked: 2,403,971 npm downloads/month**, 24,503 stars, pushed the day this was written. ~79 red-team plugins.
- **Category leader, genuinely.** 22K stars, MIT, used by OpenAI and Anthropic, now part of OpenAI — this is the de-facto open standard for LLM evals + red-teaming, not a hopeful newcomer. Its absence from the catalog was a gap.
- **Declarative, CI-native.** Configs + CLI + CI/CD integration make LLM evaluation a regression gate, not a manual spot-check — the same shift unit tests brought to code.
- **Two jobs, well-fused.** Eval (which prompt/model is better) *and* red-team/vuln-scan (is this app safe) in one tool, plus PR code-scanning for LLM security issues.
- **Provider-agnostic.** Side-by-side across OpenAI/Anthropic/Azure/Bedrock/Ollama lets you make model choices on evidence.
- **Local-first option.** Runs from the CLI against your own keys; no mandatory SaaS.

## What didn't work or surprised us

- **"Local-first… no mandatory SaaS" is true of `eval` and false of `redteam`.** The previous review's bullet reads *"Local-first option. Runs from the CLI against your own keys; no mandatory SaaS."* `promptfoo redteam generate` stops on **"Red team scans require email verification to continue. ? Work email:"** and reaches `https://api.promptfoo.app`. That is half the tool — and it is the half the Safety row rests on entirely.
- **The gate blocks instead of failing, in the context where blocking is worst.** In an interactive terminal it hung for **9 m 50 s with zero bytes of output** before being killed — the prompt was buffered, so there was nothing to read and nothing to act on. In a non-TTY it does exit (rc=1, 1.3 s) but through a Node `Detected unsettled top-level await` warning rather than a clean error naming the cause. A hard requirement announced by a silent hang is the worst available way to announce it.
- **1.7 GB of `node_modules` for a CLI**, and a `"node": ">=22.22.0"` floor — a very recent hard minimum for a tool whose pitch is dropping into an existing CI pipeline.
- **The eval's own Safety row now needs qualifying.** *"Red-teaming, vulnerability scanning, and PR code-scanning surface AI security/compliance issues pre-merge"* describes capabilities that are real but not reachable from an unattended pipeline without registering with the vendor first.
- **Scope is "LLM apps," not the coding dev loop directly.** It evaluates *the AI features you build*, not primarily *your code agent* — most relevant when you're shipping LLM-powered software, somewhat tangential to pure code authoring.
- **OpenAI ownership.** Now part of OpenAI; still MIT and open, but governance/roadmap independence is a watch-item for some.
- **Real setup for real value.** Meaningful evals need authored test cases/assertions and (for red-team) configured targets — it rewards investment, not a one-liner.
- **Cost of running evals.** Comparing models across many cases is inference spend; the value (catching regressions/vulns) usually justifies it, but it isn't free.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Automated evals catch prompt/model regressions before they ship; assertions encode expected behavior. |
| Speed | + / neutral | CI gating replaces manual eyeballing; authoring/ running large eval suites takes time + tokens. |
| Maintainability | + | Declarative configs are versioned, reviewable regression tests for AI behavior. |
| Safety | + / gated | Red-teaming and vulnerability scanning are substantial (~79 plugins) — but `redteam generate` requires vendor **email verification** and reaches `api.promptfoo.app`, blocking indefinitely on an interactive TTY. Not reachable unattended without registering. |
| Cost Efficiency | + | Free/MIT, and **measured**: an `exec:` provider runs the full harness for zero tokens, so assertion logic is developed and CI-gated at no inference cost. Comparing real models is separately billable. |
| Verifiability | + | The planted-failure design makes a green run falsifiable, `rc=100` is a machine-checkable gate, and `gradingResult.componentResults[]` says *which* assertion failed and why — a human can confirm the result at the rate it is produced |

## Verdict

**CONDITIONAL** — adopt-if: you want the **eval** half — declarative, CI-gated assertions over prompts and agent outputs — **and you accept that the red-team half requires vendor email verification plus a live provider**.

The eval half is better than the previous review guessed, in a specific and useful way: it runs with **no model credentials at all**. An `exec:` provider makes any script a "model", so assertion logic can be authored, tested and gated in CI for free, and only the model-graded assertions (`llm-rubric`, `factuality`) actually need inference. Five cases ran in 1.3 s, six assertion types all discriminated correctly against planted failures, and a failing run exits **100** with per-assertion reasons in JSON. That is a working regression gate for LLM behaviour, and the *"cost of running evals"* objection the earlier review raised applies to model comparison, not to the tool.

The gate in the verdict is the other half. **"Local-first option… no mandatory SaaS" is only true of `eval`.** `promptfoo redteam generate` stops on *"Red team scans require email verification to continue"* and contacts `api.promptfoo.app` — and it announces that requirement by **hanging for ten minutes with no output** on an interactive terminal, or by exiting through an unsettled-top-level-await warning in CI. Red-teaming is one of the two headline capabilities and the sole basis of the Safety row, so an eval that recommends this tool has to say which half a reader is getting.

The catalog-scope caveat from the previous verdict still holds and is not a defect: promptfoo's object is *the LLM app you build*, not your coding agent. For this catalog that keeps it CONDITIONAL rather than ADOPT independently of everything above.

**Sensible path:** use `promptfoo eval` as a CI regression gate, starting with `exec:` or deterministic providers so the suite is free to run and fast to iterate; add real providers only for the cases that need a model grader. Treat `redteam` as a separate decision requiring vendor registration, and do not put it in an unattended pipeline before testing that it fails cleanly there.

Compared to neighbours: **langfuse** is tracing-first observability as a platform; **evalview** is agent regression testing over MCP. Promptfoo's distinguishing pitch is **declarative, CI-native evals that run without a provider at all** — a stronger claim than the red-teaming fusion it leads with, and the one this run actually verified.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [promptfoo](https://github.com/promptfoo/promptfoo) | tool | LLM eval + red-teaming CLI/library (MIT, now part of OpenAI; 2.4M npm downloads/mo) — declarative CI-gated assertions that run with **no model provider** via `exec:`; red-teaming separately requires vendor email verification | Prompt/model changes are trial-and-error with no regression signal, and LLM apps ship with untested security holes | langfuse, evalview |
