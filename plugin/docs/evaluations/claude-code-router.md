# Evaluation: claude-code-router

**Repo:** [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)
**Stars:** 36,419 | **Last updated:** 2026-08-04 | **License:** MIT
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement / Verify (intercepts every model request Claude Code makes; spans the whole inner loop)
**Layer:** Infrastructure

---

## What it does

> **Staleness note (2026-10-16 run):** the description below was written against CCR 2.0.0. The npm package now installs **3.1.3**, which is a different product surface (a UI-managed gateway with Agent Profiles and rule-based routing; see the run below). Read this section as history.

claude-code-router (CCR) is a local proxy that sits between Claude Code and the model. Its catalog one-liner is "Route and customize how you interact with Claude Code while inheriting upstream updates"; the repo's own framing is blunter: "Use Claude Code as the foundation for coding infrastructure, allowing you to decide how to interact with the model while enjoying updates from Anthropic." The mechanism: Claude Code speaks the Anthropic Messages API to a *local* HTTP endpoint (default `http://127.0.0.1:3456`) instead of to api.anthropic.com, and CCR decides — per request — which provider and model actually fulfills it, rewriting the payload as needed.

The routing is rule-based and category-aware. The `Router` config block maps request *categories* to `provider,model` strings: `default` (general tasks), `background` (cheap/local model for trivial work), `think` (reasoning-heavy / Plan Mode), `longContext` (auto-switches when the prompt exceeds `longContextThreshold`, default 60K tokens), `webSearch`, and `image`. So a single Claude Code session can route Plan Mode to DeepSeek-Reasoner, background summarization to a local Ollama `qwen2.5-coder`, and long-context turns to Gemini 2.5 Pro — automatically, by token count and task type. You can override live with `/model provider,model` inside Claude Code, route individual subagents with a `<CCR-SUBAGENT-MODEL>provider,model</CCR-SUBAGENT-MODEL>` prompt prefix, or drop in a `CUSTOM_ROUTER_PATH` JS module that returns the destination from arbitrary logic on the request body.

The second half is **transformers** — small adapters that reshape requests/responses so non-Anthropic APIs (OpenRouter, DeepSeek, Gemini, Volcengine, SiliconFlow, ModelScope, DashScope, Groq, Ollama, and others) behave correctly against Claude Code's Anthropic-shaped traffic. Built-ins include `deepseek`, `gemini`, `openrouter`, `maxtoken`, `tooluse`, `reasoning`, `sampling`, `enhancetool` (tolerance for malformed tool-call JSON), and `cleancache`; custom transformers load from a plugins directory. Supporting surface: `ccr code` (launch CC through the router), `ccr ui` (web config editor), `ccr model` (interactive CLI model picker), `ccr preset` (export/share configs with API keys auto-sanitized to `{{field}}` placeholders), `eval "$(ccr activate)"` (export `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` so the bare `claude` command and Agent-SDK apps route through CCR), a beta status line, and a GitHub Actions recipe (`NON_INTERACTIVE_MODE`) for routing CI Claude tasks to cheaper models during off-peak hours.

## How we tested it

**Evidence:** RUN

**Hands-on** — installed `@musistudio/claude-code-router` with `npm install` into `/tmp/eval-claude-code-router`, started the service with `ccr start --no-open`, configured it through the service's own RPC (`POST /api/ccr/rpc`, methods `getConfig`/`saveConfig`/`restartGateway`), and sent Anthropic Messages requests at the gateway on `127.0.0.1:3456`. Upstreams were two local mock OpenAI-compatible servers (`cheap` on :9101, `strong` on :9102) that log every request they receive, so routing is checked against the upstream logs rather than against CCR's own claims. No model credentials were used, so no real model output was involved.

```
$ npm install @musistudio/claude-code-router   # -> 3.1.3 (not 2.0.0)
$ ccr start --no-open                          # 2.3s, "CCR service started at http://127.0.0.1:3458/?ccr_web_token=..."
# Providers: cheap -> :9101 (small-model), strong -> :9102 (big-model)
# Router.rules: model-prefix "claude-haiku" -> cheap,small-model ; model-prefix "claude-sonnet" -> strong,big-model
== A. 20 Anthropic-shaped requests (10 haiku, 10 sonnet, 1 tool def each)
anthropic-shaped OK: 20 / 20   median latency ms 9.1
  haiku  -> 200 {"type":"message","model":"small-model","content":[{"type":"text","text":"reply-from-cheap"}],...}
  sonnet -> 200 {"type":"message","model":"big-model","content":[{"type":"text","text":"reply-from-strong"}],...}
upstream logs: cheap received 10 non-streaming + 1 streaming from CCR, strong received 10; tools:1 on every request
== B. no key -> 401 "Missing auth token header"; wrong key -> 401 "Invalid or expired API key"
== C. stream:true -> 200, Anthropic SSE (message_start, content_block_start, content_block_delta ...)
== D. model matching no rule (claude-opus-4-1) -> 400 "All target providers failed ... not configured for target provider"
== E. same mock hit directly, no CCR: median 1.1 ms   (CCR path: 9.1 ms)
== F. saveConfig with 2.x-style Router {default, background, longContext, longContextThreshold:1000}
saveConfig ok:true; then haiku, sonnet and a 30,000-char sonnet prompt -> all three HTTP 400 "All target providers failed"; 0 requests reached either upstream
```

## Test design

- **Task/corpus:** 20 fixed Anthropic `/v1/messages` requests (10 `claude-haiku-4-5`, 10 `claude-sonnet-4-5`, prompts `prompt 0..9`, one `get_weather` tool definition each) plus five single-request probes (auth, streaming, unmatched model, legacy config, direct baseline). Upstreams are mock servers that return a fixed OpenAI `chat.completion` and log model, tool count and auth header.
- **Baseline:** the same mock hit directly with an OpenAI-shaped request, for added latency only. There is no with/without arm for model quality, because no real model was available.
- **Metric:** requests landing on the intended upstream (k/N, read from the upstream logs); response shape (`type: message`, text content); HTTP status for auth and error cases; median wall-clock per request.
- **Reproduce:** the scripts live in `/tmp` only. Rebuild from the Task/corpus line: install the npm package, `ccr start --no-open`, read the token from the printed URL, call `saveConfig` with two `Providers` entries (`api_base_url`, `api_key`, `models`) and two `Router.rules` entries (`type: model-prefix`, `pattern`, `target: "provider,model"`), then POST to `http://127.0.0.1:3456/v1/messages` with an `x-api-key` from `APIKEYS`.

## What worked

- **Rule routing sent every request to the intended upstream.** 20 of 20 requests landed on the provider the `model-prefix` rule named (10 on `cheap`, 10 on `strong`), the provider's own API key and model name were substituted (`Bearer k-cheap`, `small-model`), and the tool definition survived the translation (`tools: 1` on each upstream request).
- **The Anthropic-to-OpenAI translation held for this fixture.** Non-streaming replies came back as valid Anthropic `message` objects with usage mapped to `input_tokens`/`output_tokens`, and `stream: true` came back as Anthropic SSE events.
- **Gateway auth works.** A missing key and a wrong key both returned 401 before anything reached an upstream.
- **Setup is scriptable without the browser.** The management RPC accepted `getConfig`/`saveConfig` with an `x-ccr-web-auth` header, so the whole configuration could be applied from a script; `saveConfig` uses a `configRevision` check and rejects a stale write with a clear message.

## What didn't work or surprised us

- **The product changed under the existing eval.** The prior eval described 2.0.0 and its `default`/`background`/`think`/`longContext` categories. The npm package is now 3.1.3, the README has no `Router` category keys, and `ccr code`, `ccr model`, `ccr preset` and `ccr activate` are not in `ccr --help`; the help shows `start|ui|serve|stop|<profile>`. Any reader following the old eval's config would be configuring a different tool.
- **The old category routing did not work under 3.1.3 in this run.** A config using `Router.default`, `background` and `longContext` was accepted by `saveConfig` (`ok: true`) and then every request returned HTTP 400 with nothing reaching either upstream. We did not print the stored `Router` back, so we cannot say whether the keys were dropped or stored and ignored; only the 400s are observed. The 3.x equivalent is explicit `Router.rules` (condition or `model-prefix`); the `longContextThreshold` behaviour was not re-tested in rule form.
- **No default route.** A model name that matches no rule returns 400 rather than falling to a default provider, so a rule set has to cover every model name Claude Code sends.
- **Added latency was small but not zero.** Median 9.1 ms through CCR against 1.1 ms direct to a local mock (about 8 ms over 20 requests per arm); this says nothing about a real remote provider.
- **The model-quality risk the old eval flagged is untouched.** We had no model credentials, so we ran nothing on tool-call fidelity, instruction following or real cost. The mock always returns text, so tool-call translation in the response direction was not exercised.
- **Config UX is heavier than the old CLI.** Provider setup needs a management token, a client API key and the RPC or UI; the README's quick start assumes the browser UI.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Routing and request/response translation were right on a 20-request fixture (20/20), but nothing about real-model tool-call quality was measured |
| Speed | neutral | Median 9.1 ms through CCR vs 1.1 ms direct to a local mock; real provider latency dominates and was not measured |
| Maintainability | - | The product moved from 2.0.0 to 3.1.3 and the old category config stopped routing; an eval, and a user's config, can go stale in weeks |
| Safety | + | Gateway rejected missing and wrong client keys with 401; provider keys stay in CCR and the client only holds a CCR key |
| Cost Efficiency | neutral | Rules can send chosen model names to a cheaper provider (verified mechanically), but no spend or token numbers were measured |
| Verifiability | + | Routing outcome is checkable from the upstream request logs, which the tool does not control |

## Verdict

**discovery-log — tentative read** — the 3.1.3 gateway routes Anthropic-shaped requests to the rule's provider correctly (20/20 on a mock fixture), but the old eval's category config no longer routes, no real model was available to test quality or cost, and so no adoption read is supported yet. A real-model run (tool-call fidelity, spend per session) is what would turn this into a verdict.

## Triage note

Left at `discovery-log`. MIT, ★36.4K, pushed today.

Its eval makes the affirmative case cleanly — category-aware routing (`background`/`think`/
`longContext` with a token threshold) is "the strongest [lever] in its catalog cluster for keeping the
Claude Code UX while paying less per token", which "earns it a real place in the dev loop as an
Infrastructure layer" — and the reservations that hold it below ADOPT are unquantified correctness
cost, 968 open issues on the critical path of every request, and ToS gray areas. All conditions, none
a disposal.

**One drift worth recording.** The repository now describes itself as "**One local control plane for
every AI agent** — route across models, fuse new capabilities, orchestrate tools", where the eval was
written against a Claude-Code-specific router. If the scope has genuinely broadened to any agent, the
comparison against `CLIProxyAPI` and `bifrost` in that eval is measuring a narrower tool than the one
that ships today. Flagged for the re-check, not resolved here.

**Re-check confirmed, 2026-09-21 (5-oldest-untriaged pass):** the repo's current About/README tagline
reads verbatim "One local control plane for every AI agent: route across models, fuse new
capabilities, orchestrate tools, and stay fully in control," and the README lists Claude Design,
Codex, Grok CLI, Kimi CLI, Kilo Code, OpenCode, Pi, ZCode, and WorkBuddy alongside Claude Code as
supported agents. The scope broadening flagged above is real, not stale phrasing. This is source-only
confirmation (repo page only, not installed), so it does not change the verdict — re-running the
`CLIProxyAPI`/`bifrost` comparison against the current, broader tool is P0/eval-runner work, not
something this bulk pass can do. Left at `discovery-log`; ★37.4K, MIT, still actively pushed.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268)); re-stamped 2026-09-21._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-router](https://github.com/musistudio/claude-code-router) | tool | Local proxy that routes Claude Code requests to other models/providers by task category, with transformers for API compatibility | Want to build coding infrastructure on Claude Code as a foundation layer (use cheaper/local/alt models while keeping the Claude Code UX) | claude-code-templates, CLIProxyAPI |
