# Evaluation: Opik

**Repo:** [comet-ml/opik](https://github.com/comet-ml/opik)
**Stars:** 21,115 | **Last updated:** 2026-08-05 (pushed) | **License:** Apache-2.0 | **Language:** Python + TS (by Comet)
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Observability / Verify — LLM tracing, evaluation, optimization
**Layer:** Infrastructure (self-hostable server + client SDKs)

---

## What it does

Opik is **open-source AI observability, evaluation, and optimization** — "build, test, and optimize generative AI applications from prototype to production." For RAG chatbots, code assistants, and complex agentic systems it provides **comprehensive tracing**, **LLM-as-a-judge metrics**, **evaluation datasets/experiments**, and **automatic prompt and tool optimization**. Self-hostable server + Python/TS client SDKs, with integrations across most LLM frameworks. From Comet (the ML experiment-tracking company).

## How we tested it

**Evidence:** RUN

**Hands-on** — installed the Python SDK via `pip install opik` (v2.2.103, 43 s) into a fresh venv and ran its heuristic metrics and `@track` tracing against a local stub HTTP server standing in for the Opik backend (`OPIK_URL_OVERRIDE`). No Docker, API key or Comet account was involved, so the arms below cover the SDK only.

```bash
python3 -m venv v && v/bin/pip install opik        # opik 2.2.103
v/bin/python t1.py     # 5 heuristic metrics vs stdlib equivalents on a 20-case fixture
v/bin/python t2.py stub   # @track nested agent->inner x5 against a recording stub server
v/bin/python t2.py dead   # same, with nothing listening on the target port
```

Output (abridged):

```
'Hello World' 'hello world' {'eq': (1.0, 0.0), 'lv': (1.0, 0.818)}
'OK' 'ok' {'eq': (1.0, 0.0), 'lv': (1.0, 0.0)}
agreement with stdlib baseline /20: {'eq': 18, 'ct': 20, 'js': 20, 'rx': 20, 'lv': 18} total sec 0.009
stub results [1, 3, 5, 7, 9] call_time 0.271s flush 0.034s
  POST /api/v1/private/spans/batch 687
  POST /api/v1/private/traces/batch 360
  POST /api/v1/private/spans/batch 302
  POST /api/v1/private/traces/batch 203
dead results [1, 3, 5, 7, 9] call_time 0.077s flush 11.052s   # "Failed to process message ... will be retried"
plain (undecorated) 5 calls: 0.000005s
Equals(case_sensitive=True).score('OK','ok') = 0.0 ; LevenshteinRatio(case_sensitive=True) = 0.818
```

## Test design

- **Task/corpus:** a 20-pair (output, expected) fixture of code-agent-style outputs (JSON valid/invalid, trailing commas, whitespace, case, unicode, 50-char strings, empty string), built in `/tmp/eval-opik/fx.py`; plus a 2-level nested `@track` function called 5 times.
- **Baseline:** Python stdlib equivalents (`==`, `in`, `json.loads`, `re.search`, `difflib.SequenceMatcher`) for the metrics; undecorated functions for tracing overhead.
- **Metric:** per-case agreement between the Opik metric and the stdlib baseline (k/20); wall-clock for 5 traced calls and flush; HTTP requests received by the stub server.
- **Reproduce:** the three commands above in the fenced block (scripts are small and only described here, not committed).

## What worked

- **Three concerns in one tool.** Tracing (what happened), evaluation (was it good), and **optimization** (make the prompts/tools better) — most tools cover one or two; Opik's automatic prompt/tool optimization is the differentiator.
- **Agent-aware tracing.** Built for RAG and "complex agentic systems," not just single calls — the right granularity for debugging multi-step agents.
- **LLM-as-a-judge + datasets.** Metrics and eval datasets make subjective behavior measurable and regression-testable.
- **Self-hostable + Apache-2.0.** Run it yourself; open license; broad framework integrations.
- **Serious vendor.** Comet has years in ML experiment tracking; Opik is a credible, actively-developed product (19.7K stars, daily pushes).

## What didn't work or surprised us

- **Observes the AI app you build, not the coding agent.** Like langfuse/promptfoo/giskard, the object is the *agentic system you ship*; catalog-relevant as the obs/eval layer, tangential to authoring code.
- **It's a platform to run.** Self-hosting a tracing/eval server + DB is real infra; the hosted Comet option is the easy path (vendor gravity).
- **Crowded LLMOps field.** Overlaps langfuse (tracing-first), promptfoo (declarative evals/red-team), giskard (agent red-team), ragas (RAG metrics). The wedge is tracing + eval + *optimization* unified.
- **Instrumentation effort.** Real value needs wiring SDK tracing through your app and authoring eval datasets.
- **Case-insensitive by default.** `Equals` and `LevenshteinRatio` default to `case_sensitive=False`: `Equals('OK','ok')` scores 1.0 where `==` says no — 2 of the 20 fixture cases disagreed with stdlib until `case_sensitive=True`. A surprise for code-output checks where case matters.
- **Unreachable backend is noisy and slow to flush.** With nothing listening, the app code kept working (results identical), but `flush_tracker()` blocked 11.05 s and printed one "Failed to process message" line per batch.
- **Not exercised here:** the self-hosted server and UI, the LLM-as-judge metrics (Hallucination, GEval, AnswerRelevance — each needs a model key), datasets/experiments, and the automatic prompt optimizer. Those are the platform's differentiators, so this run says nothing about them.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Heuristic metrics matched stdlib on 18/20 (all 20 once case-sensitivity was set); judge metrics unmeasured. Tracing + LLM-as-judge evals surface where an agent goes wrong and catch regressions. |
| Speed | + / neutral | Tracing is async-batched: 5 traced calls took 0.077-0.271 s vs 5 µs undecorated; unreachable backend adds an 11 s flush. |
| Maintainability | + | Versioned eval datasets/experiments are repeatable regression tests for AI behavior. |
| Safety | + (indirect) | Visibility + eval gates reduce shipping silently-wrong agent behavior. |
| Cost Efficiency | + | Trace-level cost/token tracking and prompt optimization reduce spend (claim not measured; SDK itself is free). |
| Verifiability | + | Traces are inspectable per call and the metrics are deterministic and re-runnable (stub received 4 batch POSTs for 5 calls); LLM-judge scores would need spot-checking. |

## Verdict

**discovery-log — tentative read** — The SDK installs cleanly, traces nested calls to a backend without altering results, and its heuristic metrics match stdlib checks (18/20 by default, 20/20 with `case_sensitive=True`); but the server, LLM-judge metrics and optimizer that justify the platform were never exercised (no Docker or model key), so there is no basis yet to promote or eliminate it. Next step for a human: run the self-hosted stack and one judge metric.

Compared to neighbors: **langfuse** is tracing/observability + prompt management; **promptfoo** is declarative eval + red-teaming; **giskard-oss** is agent red-teaming; **ragas** is RAG metrics. Opik's distinguishing pitch is **unified tracing + evaluation + automatic prompt/tool optimization for agentic systems.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opik](https://github.com/comet-ml/opik) | platform | Open-source LLM observability, evaluation, and optimization (Apache-2.0, by Comet) — end-to-end tracing of RAG/agentic systems, LLM-as-judge metrics, eval datasets, and automatic prompt/tool optimization; self-host or hosted, integrates with most frameworks | Can't see, score, or improve what an LLM app/agent does in dev and prod; need tracing + evals + optimization in one place | langfuse, promptfoo, giskard-oss, ragas |
