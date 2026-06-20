# Evaluation: Cost Observability Tools

Combined evaluation of three cost observability approaches: tokencost (per-call tracking), Infracost (infrastructure estimates), and abtop (live session monitoring).

---

## tokencost

**Repo:** [AgentOps-AI/tokencost](https://github.com/AgentOps-AI/tokencost)
**Stars:** 1,985 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Outer loop (Observe)
**Layer:** Infrastructure

### What it does

Python library that estimates token counts and dollar costs for 400+ LLMs from a built-in pricing table — *before or after* a call, without needing the provider's usage response. You pass it a prompt/completion string (or a token count) and a model name; it returns the cost.

### How we tested it

Installed it (`pip install tokencost`) and ran the count + cost functions directly on a sample prompt/completion across several models — no live API calls, to test the offline estimation path.

```python
from tokencost import count_string_tokens, calculate_prompt_cost, calculate_completion_cost
prompt = "Write a haiku about rate limiting in distributed systems."
count_string_tokens(prompt, model="gpt-4o")                 # -> 11
calculate_prompt_cost(prompt, model="gpt-4o")               # -> $0.00002750
calculate_completion_cost(completion, model="gpt-4o")       # -> $0.00018000
calculate_prompt_cost(prompt, model="gpt-4o-mini")          # -> $0.00000165
calculate_prompt_cost(prompt, model="claude-3-5-sonnet-20241022")  # -> raises (see below)
```

Pricing checked out exactly: 11 prompt tokens × $2.50/1M (gpt-4o input) = $0.0000275, matching the returned value; gpt-4o-mini came out ~17× cheaper as expected.

### What worked

- **Accurate offline estimation for OpenAI/tiktoken models.** Token counts and costs are computed locally from a bundled pricing table — the gpt-4o numbers matched hand-calculated pricing to the cent, and switching to gpt-4o-mini reflected the cheaper rate. No API key, no network.
- **Useful for pre-flight budgeting** — you can price a prompt before sending it, not just after, which `abtop`/usage-response approaches can't do.
- **Broad model coverage** (400+) for cross-provider cost comparison.

### What didn't work or surprised us

- **Claude costing is NOT offline — and failed without credentials.** `calculate_prompt_cost(..., model="claude-3-5-sonnet-20241022")` raised `Could not resolve authentication method. Expected either api_key or auth_token...`, and the import emitted `Warning: Anthropic token counting API is currently in beta`. For Claude models tokencost calls Anthropic's **remote** token-counting API (needs an API key), so the "just wrap it and read Claude costs" path does **not** work out of the box — a real gap for Claude Code users specifically.
- **Library, not a CLI hook** — you must control the call site; it can't observe Claude Code CLI sessions (use `abtop` for that).

### Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | No impact on code quality. |
| Speed | neutral | Local table lookup for OpenAI; a network call for Claude. |
| Maintainability | neutral | No code changes beyond instrumentation. |
| Safety | neutral | Read-only; but Claude path sends text to Anthropic's counting API. |
| Cost Efficiency | + | Prices prompts ahead of time for OpenAI models; enables pre-flight budgeting. |

### Verdict

**CONDITIONAL**

Verified: accurate, fully-offline token/cost estimation for OpenAI-family models (pricing matched to the cent). Adopt for custom Python pipelines where you control the calls and want pre-flight budgeting. Two caveats from the hands-on run: it's a library (not a Claude Code CLI hook — `abtop` covers that), and **Claude token counting requires an Anthropic API key** because it routes to Anthropic's beta counting API rather than a local tokenizer.

### Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tokencost](https://github.com/AgentOps-AI/tokencost) | tool | Per-call LLM cost tracking for 400+ models | Can't tell which API calls are burning money | abtop, langfuse |

---

## Infracost

**Repo:** [infracost/infracost](https://github.com/infracost/infracost)
**Stars:** 12,369 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Dev loop stage:** Ship (pre-deploy gate)
**Layer:** Infrastructure

### What it does

CLI that estimates cloud infrastructure costs from Terraform/CDK/Pulumi files before deployment. Shows cost diffs in PRs so teams catch expensive changes before they merge.

### How we tested it

**README/scope review — not run hands-on.** Running it meaningfully needs a Terraform/CDK/Pulumi project plus an Infracost API key and cloud pricing config — out of scope for a throwaway test here, and tangential to AI dev tooling (see verdict). The commands below are the documented usage, not an observed run:

```
infracost breakdown --path .
infracost diff --path . --compare-to infracost-base.json
```

### What worked (from the docs/positioning)

- Estimates standard AWS/GCP/Azure resource costs from IaC before deploy.
- PR-comment integration surfaces the cost delta of a change.
- Catches surprise bills before `terraform apply`; well-maintained (12K+ stars).

### What didn't work or surprised us

- **Wrong domain for this catalog** — it estimates *infrastructure* (compute, storage, network), not LLM/token costs, which is the cost axis that matters for AI dev work.
- Requires Terraform/CDK/Pulumi files — no use in projects without IaC.

### Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't affect code |
| Speed | neutral | Runs in seconds on typical configs |
| Maintainability | neutral | No code changes |
| Safety | + | Prevents surprise infrastructure bills |
| Cost Efficiency | + | Catches expensive infra changes pre-deploy |

### Verdict

**SKIP**

Solves infrastructure cost estimation, not AI/LLM cost observability. Wrong domain for this workflow unless you're deploying cloud resources alongside your AI services. If you have Terraform, it's excellent — but it doesn't belong in an AI dev tooling evaluation.

### Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Infracost](https://github.com/infracost/infracost) | tool | Cloud infrastructure cost estimates from Terraform/CDK | Surprise cloud bills from unreviewed infra changes | — |

---

## abtop

**Repo:** [graykode/abtop](https://github.com/graykode/abtop)
**Stars:** 2,946 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Outer loop (Observe)
**Layer:** Infrastructure

### What it does

Terminal UI (htop-style) that monitors Claude Code and Codex CLI sessions in real time. Shows tokens consumed, context window usage, rate limits, and active ports per session.

### How we tested it

**Repo/README review — not run hands-on** (it's an interactive TUI, not a scriptable one-shot). Note the install: abtop is a **Rust** tool — `cargo install abtop` (crates.io v0.4.8), or the `abtop-installer.sh` release script. It is **not** an npm package; an earlier draft of this eval said `npx abtop`, which 404s.

```
cargo install abtop      # Rust/crates.io — NOT `npx abtop` (no such npm package)
abtop                    # launches the TUI; discovers active sessions
```

### What worked

- Zero-config — just run it and it discovers active sessions
- Live token/cost counters per session make it easy to spot an expensive run
- Context window fill indicator prevents surprise compactions
- Rate limit visibility helps understand throttling behavior
- Lightweight — doesn't interfere with the sessions it monitors

### What didn't work or surprised us

- **Install was misdocumented** — listed as `npx abtop` (an npm package that doesn't exist); it's actually a Rust/cargo tool. A sign the original entry wasn't run.
- Only monitors Claude Code and Codex (per README) — doesn't cover other agent frameworks.
- No historical data or export — it's purely live, no after-the-fact analysis.

### Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Read-only monitoring |
| Speed | neutral | No overhead on monitored sessions |
| Maintainability | neutral | No code changes |
| Safety | neutral | Passive observer |
| Cost Efficiency | + | Shows where tokens go in real time, enables mid-session decisions |

### Verdict

**CONDITIONAL** (review-based)

On its design, abtop is a lightweight htop-style monitor that shows where tokens go in live Claude Code/Codex sessions — a sensible fit for catching runaway usage before context exhaustion. Held at CONDITIONAL rather than ADOPT because this is a README review, not a run, and the original install command was wrong (it's `cargo install abtop`, a Rust tool, not `npx abtop`). Confirm the live session-discovery behavior before treating it as a default.

### Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [abtop](https://github.com/graykode/abtop) | tool | htop for AI coding agents — live token and context monitoring | Can't see which sessions are expensive or near context limits | tokencost, langfuse |
