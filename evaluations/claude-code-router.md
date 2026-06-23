# Evaluation: claude-code-router

**Repo:** [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)
**Stars:** 35,136 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Implement / Verify (intercepts every model request Claude Code makes; spans the whole inner loop)
**Layer:** Infrastructure

---

## What it does

claude-code-router (CCR) is a local proxy that sits between Claude Code and the model. Its catalog one-liner is "Route and customize how you interact with Claude Code while inheriting upstream updates"; the repo's own framing is blunter: "Use Claude Code as the foundation for coding infrastructure, allowing you to decide how to interact with the model while enjoying updates from Anthropic." The mechanism: Claude Code speaks the Anthropic Messages API to a *local* HTTP endpoint (default `http://127.0.0.1:3456`) instead of to api.anthropic.com, and CCR decides — per request — which provider and model actually fulfills it, rewriting the payload as needed.

The routing is rule-based and category-aware. The `Router` config block maps request *categories* to `provider,model` strings: `default` (general tasks), `background` (cheap/local model for trivial work), `think` (reasoning-heavy / Plan Mode), `longContext` (auto-switches when the prompt exceeds `longContextThreshold`, default 60K tokens), `webSearch`, and `image`. So a single Claude Code session can route Plan Mode to DeepSeek-Reasoner, background summarization to a local Ollama `qwen2.5-coder`, and long-context turns to Gemini 2.5 Pro — automatically, by token count and task type. You can override live with `/model provider,model` inside Claude Code, route individual subagents with a `<CCR-SUBAGENT-MODEL>provider,model</CCR-SUBAGENT-MODEL>` prompt prefix, or drop in a `CUSTOM_ROUTER_PATH` JS module that returns the destination from arbitrary logic on the request body.

The second half is **transformers** — small adapters that reshape requests/responses so non-Anthropic APIs (OpenRouter, DeepSeek, Gemini, Volcengine, SiliconFlow, ModelScope, DashScope, Groq, Ollama, and others) behave correctly against Claude Code's Anthropic-shaped traffic. Built-ins include `deepseek`, `gemini`, `openrouter`, `maxtoken`, `tooluse`, `reasoning`, `sampling`, `enhancetool` (tolerance for malformed tool-call JSON), and `cleancache`; custom transformers load from a plugins directory. Supporting surface: `ccr code` (launch CC through the router), `ccr ui` (web config editor), `ccr model` (interactive CLI model picker), `ccr preset` (export/share configs with API keys auto-sanitized to `{{field}}` placeholders), `eval "$(ccr activate)"` (export `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` so the bare `claude` command and Agent-SDK apps route through CCR), a beta status line, and a GitHub Actions recipe (`NON_INTERACTIVE_MODE`) for routing CI Claude tasks to cheaper models during off-peak hours.

## How we tested it

**Evidence:** REVIEW

Architecture/surface-area review. Inspected the GitHub repo via the API: the full README, the repo tree, `config.example.json` structure, `custom-router.example.js`, the `docs/` site tree (CLI command + config reference), and version metadata. Confirmed the published npm version (`@musistudio/claude-code-router` = **2.0.0**) and latest git tag (**v2.0.0**). **Did NOT install or run it** — no live Claude Code session was routed through CCR, so no latency, no cost-savings percentages, and no model-quality comparisons are reported below. Any such number would be fabricated. This evaluation decides catalog placement from documented capability and maturity, the same lens applied to the headroom and fast-agent calibration evals.

```bash
gh api repos/musistudio/claude-code-router --jq '{stars,license,description,pushed_at,open_issues,forks}'
gh api repos/musistudio/claude-code-router/readme --jq '.content' | base64 -d
gh api "repos/musistudio/claude-code-router/git/trees/main?recursive=1" --jq '.tree[].path'
npm view @musistudio/claude-code-router version          # -> 2.0.0
gh api repos/musistudio/claude-code-router/tags --jq '.[0].name'   # -> v2.0.0
```

Reviewed: the `Router` category model (default/background/think/longContext/webSearch/image + `longContextThreshold`), the transformer pipeline and built-in adapter list, `/model` live switching, `<CCR-SUBAGENT-MODEL>` subagent routing, `CUSTOM_ROUTER_PATH`, `ccr activate`/`ccr preset`/`ccr ui`/`ccr model`, env-var interpolation (`$VAR`/`${VAR}`), the `APIKEY`/`HOST` security coupling, and the GitHub Actions integration.

## What worked

- **Category-aware, token-threshold routing is the differentiator.** Routing `background` to a local Ollama model, `think` to a reasoning model, and `longContext` to a high-context model *automatically* — keyed off task type and a `longContextThreshold` — is more granular than "pick one cheaper model for everything." This is the core Cost-Efficiency lever: expensive reasoning stays on a strong model while cheap turns fall to a local one.
- **Broad provider + transformer coverage.** OpenRouter, DeepSeek, Gemini, Volcengine, SiliconFlow, ModelScope, DashScope, Groq, Ollama, and Vertex are documented with working transformer configs, including pragmatic adapters (`enhancetool` for flaky tool-call JSON, `maxtoken`, `reasoning`) that address the real failure modes of pointing Claude Code at non-Anthropic APIs.
- **Escape hatches at every level.** Static `Router` rules, live `/model`, per-subagent prefix routing, and a full `CUSTOM_ROUTER_PATH` JS module mean routing logic can be as simple or as arbitrary as needed without forking the tool.
- **Zero-code integration path.** `ccr code` launches Claude Code through the proxy and `eval "$(ccr activate)"` redirects the bare `claude` command and Agent-SDK apps — no edits to Claude Code's own config. The "inherit upstream Anthropic updates" promise holds because CC itself is unmodified; CCR only intercepts the API endpoint.
- **Sane secret handling.** Env-var interpolation (`$OPENAI_API_KEY`) keeps keys out of `config.json`; `ccr preset export` auto-sanitizes keys to `{{field}}` placeholders for sharing; and `HOST` is force-pinned to `127.0.0.1` whenever `APIKEY` is unset, preventing an accidentally world-exposed unauthenticated proxy.
- **Strong maturity signals.** 35.1K stars, 2.9K forks, MIT, pushed the day of evaluation, just shipped a **2.0.0** major release, has a real docs site and a UI. Clearly the dominant tool in its niche.

## What didn't work or surprised us

- **Quality drop from weaker models is the unmeasured central risk.** The entire value proposition routes Claude Code's agentic traffic to non-Claude models. DeepSeek/Qwen/GLM are capable but differ from Claude on instruction-following, tool-call discipline, and long-horizon agentic coherence — the exact things Claude Code is tuned for. The `enhancetool` transformer existing *at all* (error tolerance for malformed tool-call JSON, which disables tool-call streaming) is direct evidence that weaker models misbehave on CC's tool protocol. No accuracy/retention benchmarks are published, unlike headroom's GSM8K/BFCL tables.
- **It is on the critical path of every request.** A CCR bug, transformer mismatch, or crash breaks the agent entirely, not just one turn. **968 open issues** (very high) reflect the surface area of being a live interception/translation layer across a dozen heterogeneous provider APIs that drift independently.
- **ToS / "inherit upstream updates" tension.** Routing Claude Code — an Anthropic product — to third-party and local models is squarely a gray area, and several transformers are explicitly *unofficial* CLI-bridge hacks (`gemini-cli`, `qwen-cli`, `rovo-cli`, loaded from gists). The "enjoy updates from Anthropic" framing is real for CC's binary, but each CC release can also break CCR's payload assumptions; maintenance is a treadmill against both Anthropic and N providers.
- **Configuration complexity scales with ambition.** A single-cheap-model setup is trivial, but the full promise (per-category routing, per-model transformers with options, custom routers, subagent prefixes) is a meaningful JSON surface. The `ccr ui`/`ccr model` helpers mitigate this but don't remove it.
- **Maintainer concentration + sponsorship dependence.** Effectively `musistudio`'s project, prominently sponsored by Z.ai/GLM — a soft incentive in a tool whose job is to choose models. Not disqualifying (it is the de-facto standard), but a concentration/independence note for something on the critical path.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | - | Routing agentic traffic to weaker non-Claude models risks degraded tool-calling and instruction-following; `enhancetool` exists precisely to paper over malformed tool calls; no accuracy benchmarks published |
| Speed | neutral | Could be faster (Groq/local) or slower (extra proxy hop + transform, remote provider latency); not measured, genuinely workload-dependent |
| Maintainability | - | Adds a critical-path layer that must track Claude Code releases AND a dozen provider APIs; 968 open issues; unofficial CLI-bridge transformers |
| Safety | neutral | Good defaults (env-var keys, preset sanitization, `127.0.0.1`-pin when no APIKEY) offset by ToS gray area and traffic leaving for third-party providers |
| Cost Efficiency | + | The core value: category/threshold routing sends expensive reasoning to strong models and cheap/background turns to local or low-cost models, cutting per-session spend |

## Verdict

**CONDITIONAL**

claude-code-router is the dominant, mature (35K stars, MIT, just hit 2.0.0) way to make Claude Code talk to models other than Claude, and its category-aware routing (`background`/`think`/`longContext` with a token threshold) is a genuinely good Cost-Efficiency lever — the strongest in its catalog cluster for *keeping the Claude Code UX while paying less per token*. That earns it a real place in the dev loop as an Infrastructure layer.

It is CONDITIONAL, not ADOPT, because the value comes from routing Claude Code's carefully-tuned agentic traffic to weaker models, and the correctness cost of that is real and unquantified (the `enhancetool` adapter is a tell), it sits on the critical path of every request with 968 open issues, and it lives in a ToS gray area with unofficial provider bridges. **Adopt it when** cost or provider-flexibility outweighs peak quality: heavy long-session users wanting cheap `background`/local routing, teams on a GLM/DeepSeek/Qwen subscription or air-gapped/local-only models, or CI pipelines routing `@claude` tasks to cheap models off-peak. **Skip it when** you are on a flat-rate Claude plan, do quality-sensitive agentic coding where Claude's tool discipline matters, or want to minimize critical-path moving parts — in which case run Claude Code natively. It differs from its overlaps: claude-code-templates ships *configs/agents/skills* for stock Claude Code (no model redirection); CLIProxyAPI is a general multi-CLI LLM proxy, whereas CCR is purpose-built for Claude Code's request shape with CC-specific routing categories and subagent prefixes.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-router](https://github.com/musistudio/claude-code-router) | tool | Local proxy that routes Claude Code requests to other models/providers by task category, with transformers for API compatibility | Want to build coding infrastructure on Claude Code as a foundation layer (use cheaper/local/alt models while keeping the Claude Code UX) | claude-code-templates, CLIProxyAPI |
