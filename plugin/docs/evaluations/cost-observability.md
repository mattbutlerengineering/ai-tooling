# Evaluation: Cost Observability Tools

Combined evaluation of three cost observability approaches: tokencost (per-call tracking), Infracost (infrastructure estimates), and abtop (live session monitoring).

---

## tokencost

**Repo:** [AgentOps-AI/tokencost](https://github.com/AgentOps-AI/tokencost)
**Stars:** 1,985 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Outer loop (Observe)
**Layer:** Infrastructure

### What it does

Python library that calculates token costs for 400+ LLMs. Wraps API calls to track input/output tokens and maps them to per-model pricing. Returns per-call cost breakdowns in real time.

### How we tested it

Installed in a Python project making Claude API calls. Wrapped the Anthropic client with tokencost tracking to get per-call cost breakdowns over a multi-step agent workflow.

```
pip install tokencost
# Wrap API calls — each returns cost metadata alongside the response
from tokencost import calculate_prompt_cost, calculate_completion_cost
```

### What worked

- Accurate per-call cost tracking with up-to-date pricing for Claude models
- Easy integration — pip install, wrap client, read costs
- Supports 400+ models across providers for cross-platform cost comparison
- Good for identifying which steps in a pipeline are expensive

### What didn't work or surprised us

- Python-only — doesn't work with Claude Code CLI directly (CLI doesn't expose token counts to external tools)
- Requires you to control the API calls; useless for tools that abstract the LLM layer
- Pricing data can lag behind provider announcements by a few days

### Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | No impact on code quality |
| Speed | neutral | Negligible overhead per call |
| Maintainability | neutral | No code changes beyond instrumentation |
| Safety | neutral | Read-only tracking |
| Cost Efficiency | + | Identifies expensive calls, enables optimization |

### Verdict

**CONDITIONAL**

Adopt if building custom Python agent pipelines where you control API calls directly. Skip for pure Claude Code CLI usage — the CLI doesn't expose hooks for external cost tracking. For CLI users, abtop (below) is the better fit.

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

Ran against a Terraform project defining AWS infrastructure (ECS cluster, RDS, S3 buckets). Generated cost estimates and a cost diff against the current state.

```
infracost breakdown --path .
infracost diff --path . --compare-to infracost-base.json
```

### What worked

- Accurate estimates for standard AWS/GCP/Azure resources
- PR comment integration shows cost delta clearly
- Catches surprise bills before `terraform apply`
- Well-maintained, 12K+ stars, active development

### What didn't work or surprised us

- Not relevant to AI/LLM cost tracking — it estimates infrastructure (compute, storage, network), not token costs
- Requires Terraform/CDK files — no use in projects without IaC
- Pricing for some newer resource types lags behind provider releases

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
