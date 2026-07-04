# Evaluation: trigger.dev

**Repo:** [triggerdotdev/trigger.dev](https://github.com/triggerdotdev/trigger.dev)
**Stars:** 15,403 | **Last updated:** 2026-06-19 (pushed; created 2022-11-30) | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Outer Loop (deployment/operations infrastructure for the *thing you build*), not the inner Plan→Implement→Verify→Review→Ship loop over a codebase. It is where your AI agents/workflows *run in production*, not a tool that produces or ships your code.
**Layer:** Infrastructure / platform (a TS/JS SDK — `@trigger.dev/sdk` — plus a managed cloud or self-hostable Docker/Kubernetes runtime that executes, retries, queues, checkpoints, and observes long-running tasks)

---

## What it does

Repo description: "Trigger.dev — build and deploy fully-managed AI agents and workflows." It is an open-source **background-jobs/durable-execution platform** for TypeScript: you write tasks (`task({ id, run })`) in your own codebase, deploy them, and Trigger.dev runs them with no timeouts, automatic retries, queues, concurrency control, checkpoint/resume durability, atomic versioning, multiple environments (DEV/PREVIEW/STAGING/PROD), human-in-the-loop waitpoints, realtime streaming, and full tracing/logging. Think "Inngest/Temporal-class durable execution," now explicitly repositioned around hosting **AI agents**.

The agent positioning is not marketing veneer — the `.changeset/` directory is dense with active AI-agent work (`chat-agent`, `custom-agent-loop-fixes`, `mcp-agent-chat-sessions`, `agent-skills-bundled-in-sdk`, `ai-sdk-7-support`, `chat-system-prompt-caching`). The pitch: bring whatever framework/LLM you like, deploy to Trigger.dev, and get durability, scaling, and observability for free.

Critically, this is infrastructure for **the AI application you build and operate**, not a tool that intervenes in *your* coding loop. You don't reach for trigger.dev to Plan, Implement, Verify, or Review a code change — you reach for it to *run the agentic workflow your product needs* reliably in production. That is app-hosting, adjacent to the dev loop in the same way an agent-application framework is.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No SDK installed, no task deployed, no cloud/self-host instance stood up. Every claim is from the repository surface (GitHub metadata, README, recursive file tree, `.changeset/` entries, release count), not from observed runtime behavior. Throughput/durability/"no timeouts" claims are the authors' README framing, not measured here.

```bash
gh api repos/triggerdotdev/trigger.dev --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
# desc=build/deploy managed AI agents+workflows; stars=15403; forks=1305; created 2022-11-30; Apache-2.0
gh api repos/triggerdotdev/trigger.dev/readme --jq '.content' | base64 -d | head -120  # durable tasks, retries/queues, HITL, observability
gh api "repos/triggerdotdev/trigger.dev/git/trees/HEAD?recursive=1" --jq '.tree[].path' | head -40  # heavy .changeset/ flow, many chat-agent/* entries
gh api repos/triggerdotdev/trigger.dev/releases --jq 'length'   # 30 (page-1 cap) — actively released
```

## What worked

- **Serious, mature durable-execution platform.** ~3.5 years old, Apache-2.0, self-hostable via Docker/Helm, actively released, 15.4K stars. Long-running tasks without timeouts, retries, queues, checkpoint/resume, atomic versioning, and multi-environment support are real production-grade primitives.
- **Tasks live in your codebase.** The "write tasks where they belong — version control, localhost, test, review" model means the agent/workflow definitions are normal code you can diff and review. That's a genuinely developer-friendly deployment ergonomics story.
- **Strong operational surface for AI agents.** Tracing per run, realtime/streaming for LLM responses, human-in-the-loop waitpoints, and run metadata are exactly what production agentic workflows need — and the changeset log shows active investment in agent-specific features (MCP sessions, agent loops, agent skills).
- **No-lock-in escape hatch.** Self-hosting (Docker + official Helm chart) is first-class, mitigating the usual managed-platform lock-in objection.

## What didn't work or surprised us

- **It hosts the app; it doesn't help you build it.** This is the LangGraph/dify scope call applied to deployment infra: trigger.dev runs the AI workflows *your product* defines. It does not Plan, Implement, Verify, Review, or Ship *your code changes* — it's the runtime your shipped artifact targets. That places it outside the dev loop the catalog instruments, at the Outer-Loop/app-hosting boundary.
- **General-purpose background jobs, not coding-agent infra.** Its lineage is Inngest/Temporal-style durable execution; the "AI agent" framing is a (well-executed) repositioning. It is orthogonal to a *coding* harness like Claude Code or to CI tools like claude-code-action that act on a repo.
- **The dev-loop-relevant comparison fails.** `claude-code-action` runs an *AI coding agent in CI to act on your repo* (inside Ship). trigger.dev runs *your application's tasks in production*. Same word "deploy," entirely different target — yours-the-product vs. yours-the-codebase.
- **Commercial cloud is the default path.** Onboarding funnels to cloud.trigger.dev; self-host exists but the primary product is a managed (paid-at-scale) platform — a cost/ops decision for app operators, not a coding-loop lever.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | n/a (out of loop) | Improves runtime *reliability of an AI app you operate* (retries, durability), not the correctness of your code changes during development. |
| Speed | n/a | Affects production task throughput/scaling, not developer iteration speed on a codebase. |
| Maintainability | − (if adopted) | Adopting a durable-execution platform is an architectural dependency for your *application's* runtime, with its own ops surface. |
| Safety | neutral | Runs arbitrary user tasks (browsers, Python, FFmpeg) in its sandboxes; HITL waitpoints help, but risk lives in your app, not the dev loop. |
| Cost Efficiency | − | Managed cloud is metered; self-host shifts cost to ops. A platform-cost concern for operators, not a coding-loop efficiency gain. |

## Verdict

**SKIP — app-hosting / deployment infrastructure, not a dev-loop tool.** trigger.dev is a strong, mature, open-source durable-execution platform that has smartly repositioned around hosting AI agents and workflows. But the question posed — "is it a dev-loop tool or an app-hosting platform?" — resolves cleanly to the latter: it is where the AI workflow *your product* defines runs in production, with no involvement in producing, verifying, reviewing, or shipping *your code*. It sits at the Outer-Loop/app-hosting boundary the catalog treats as adjacent, the same call made for LangGraph/dify on the build side.

Compared to neighbors: the tempting analog is **claude-code-action** (Ship/CI), but that runs a *coding agent against your repo*; trigger.dev runs *your app's tasks in production* — different target entirely, so it is not a substitute or complement within the loop. Its real peers are app-runtime platforms (Inngest/Temporal class) and the agentic-app frameworks already skipped (**CrewAI**, **LangGraph**, **dify**) — trigger.dev is the *deployment* counterpart to those *build* frameworks, and inherits the same out-of-scope verdict.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [trigger.dev](https://github.com/triggerdotdev/trigger.dev) | platform | Open-source TS durable-execution platform to deploy and run AI agents/workflows as long-running tasks with retries, queues, checkpointing, HITL waitpoints, and observability | Running an agentic *application's* workflows reliably in production (out of dev-loop scope; see SKIP verdict) | CrewAI, LangGraph, dify (skipped app frameworks — trigger.dev is their deployment counterpart); not a substitute for claude-code-action (CI-over-repo) |
