# Evaluation: vercel-sandbox

**Repo:** [vercel/sandbox](https://github.com/vercel/sandbox)
**Stars:** 147 | **Last updated:** 2026-06-16 (pushed; created 2026-01-23) | **License:** Apache-2.0
**Dev loop stage:** Implement / Verify — execution isolation infrastructure. It is where agent-generated code *runs*: install deps, start a dev server, run a build or test, expose a preview URL — all inside a disposable VM rather than on the host. Not an orchestrator and not a harness itself; a primitive a harness calls.
**Layer:** Infrastructure (a hosted Vercel service fronted by an npm SDK `@vercel/sandbox` and a `sandbox` CLI; the VMs run on Vercel's Firecracker fleet, not on your machine)

---

## What it does

The repo description: "Vercel Sandbox is an ephemeral compute primitive designed to safely run untrusted or user-generated code." It spins up isolated, ephemeral **Firecracker MicroVMs** — "the same infrastructure that powers 2M+ builds a day at Vercel" — and lets you run arbitrary commands in them via a TypeScript SDK. The canonical example: `Sandbox.create({ source: { url, type: "git" }, resources: { vcpus: 4 }, ports: [3000], runtime: "node24" })`, then `sandbox.runCommand({ cmd: "npm", args: ["install"] })`, then a detached `npm run dev`, and `sandbox.domain(3000)` returns a public preview URL — all while streaming logs to your local terminal. The repo is a monorepo: `@vercel/sandbox` (SDK), `sandbox` (CLI), plus an `examples/ai-example` Next.js app showing an LLM chat loop that executes generated code in a sandbox, and an `AGENTS.md`. Notably it also ships a Skill (`npx skills add vercel/sandbox`) and serializes across [Workflow DevKit](https://vercel.com/docs/workflow) step boundaries — both signals it is built with agent and durable-workflow use in mind.

System: Amazon Linux 2023 base, code runs as a `vercel-sandbox` user with `/vercel/sandbox` writable, optional `sudo` for `dnf install`, Node 22/24/26 and Python 3.13 runtimes. Limits: 8 vCPUs (Hobby/Pro) / 32 (Enterprise), 2048 MB per vCPU; max runtime 45 min (Hobby) / 24 h (Pro/Enterprise), default 5 min. Auth is via Vercel OIDC token (recommended) or a scoped access token with team/project IDs.

## How we tested it

**Source-grounded inspection — not installed, not run.** No sandbox was created, no command executed, no preview URL opened. I did not provision a Vercel account, pull an OIDC token, or run the `ai-example`. Every claim comes from the repository (metadata, README, file tree, package layout), not from observed isolation behavior. In particular I did **not** verify the strength of the Firecracker isolation, latency to first command, or billing — those are Vercel-side properties I can only relay from the README, not measure. This is a **hosted, paid, vendor-locked** service; that materially shapes the verdict and is the single most load-bearing fact a reader needs.

```bash
gh api repos/vercel/sandbox --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
# "ephemeral compute primitive ... safely run untrusted or user-generated code" | 147 stars | Apache-2.0 | created 2026-01-23
gh api repos/vercel/sandbox/readme --jq '.content' | base64 -d | head -220
gh api "repos/vercel/sandbox/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # SDK + CLI + examples/ai-example + AGENTS.md + Skill
gh api repos/vercel/sandbox/commits --jq 'length'        # 30 (page-1 cap)
gh api repos/vercel/sandbox/releases --jq 'length'       # 30 (changesets-driven, frequent)
gh api repos/vercel/sandbox/contributors --jq '[.[].login]|length'  # 19
```

## What worked

- **Real isolation primitive, not a wrapper.** Firecracker MicroVMs on Vercel's production build fleet give genuine VM-level isolation for untrusted/agent-generated code — the correct security posture for "let the LLM run whatever it wrote." This is meaningfully stronger than a chrooted process or a shared container.
- **Built for agents and previews, end to end.** Seed from a git URL, install, run a dev server, and get a *public* preview URL back (`sandbox.domain(port)`) — exactly the "agent writes an app, show me it running" loop. The bundled `examples/ai-example` and `AGENTS.md` make the agent intent explicit, and Workflow DevKit serialization lets a sandbox survive across durable steps.
- **Clean, typed SDK + CLI + Skill.** `@vercel/sandbox` is ergonomic TypeScript; the `sandbox` CLI and `npx skills add vercel/sandbox` lower the integration bar. Apache-2.0 on the client packages.
- **Honest, detailed operational docs.** Explicit resource/runtime limits, the exact base image package list, the `vercel-sandbox` user model, and the sudo configuration (PATH/HOME/env caveats) are all spelled out — unusually transparent for a hosted service.

## What didn't work or surprised us

- **147 stars, ~5 months old — unproven and tiny mindshare.** This is the honest headline. The *infrastructure* is mature (it's Vercel's build fleet), but this public SDK/CLI repo is new and barely starred. Treating it as a battle-tested community standard would be premature; the adoption signal is essentially absent.
- **Hosted, paid, and fully vendor-locked.** The "primitive" is a Vercel service requiring a Vercel team, project, and OIDC/access token; sandboxes run on Vercel infra and bill against your account. There is no self-host path. That is a hard dependency the neighbors below don't impose.
- **The Apache-2.0 license covers the client, not the engine.** What's open is the SDK/CLI; the Firecracker fleet behind it is closed Vercel infrastructure. "Open source" here is the access layer only.
- **Resource and time ceilings constrain heavy agent work.** 5-minute default (45 min cap on Hobby), 8 vCPU / 2 GB-per-vCPU on Pro — fine for build-and-preview loops, tight for long-running test suites or memory-hungry tooling unless on Enterprise.
- **Couldn't validate the security claim.** "Safely run untrusted code" rests on Firecracker isolation I did not exercise; egress controls, secret exposure, and tenancy boundaries are Vercel-side and unverified here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Safety | + | Firecracker MicroVM isolation + non-root `vercel-sandbox` user is the right model for executing agent-generated/untrusted code off the host; egress/tenancy specifics unverified. |
| Correctness | + | Running real installs/builds/tests in a clean, reproducible VM surfaces failures the model can't predict — closes the agent's verify loop with ground truth. |
| Speed | + / − | Firecracker boots fast and previews are one call; offset by per-create provisioning latency and a 5-min default timeout that interrupts longer tasks. |
| Maintainability | neutral | Infra outside your codebase; a typed SDK is easy to integrate, but adds a Vercel dependency to your build/CI graph. |
| Cost Efficiency | − | Hosted, metered VM compute billed to a Vercel account — recurring spend vs. self-hosted alternatives; no free local path. |

## Verdict

**CONDITIONAL — strong primitive, but hosted/paid/vendor-locked and unproven in public.** Vercel Sandbox is a legitimately good isolation primitive for running agent-generated code: real Firecracker MicroVMs, a clean typed SDK, preview URLs, an agent-oriented example, and a Skill. If you already live in the Vercel ecosystem and want managed, secure execution with public previews — and accept metered cost and lock-in — adopt it. For anyone wanting self-hosted, local, or vendor-neutral isolation, the trade-offs (hosted-only, billed, 147 stars, ~5 months old, isolation unverified by us) argue for waiting or choosing a neighbor. Conditional, not skip: the engineering is sound; the open question is whether you want this specific managed dependency.

Compared to neighbors in Agent Harnesses: **sandboxd** is the closest philosophical opposite — *self-hosted* dev sandboxes with preview URLs, "one command, no Kubernetes," no vendor bill. **sandcastle** orchestrates sandboxed coding agents in TypeScript (programmatic spawning/isolation) and would *consume* a primitive like this rather than compete with it. **forkd** offers fast KVM-isolated agent microVMs with sub-second fork — comparable isolation tech, different (fork-heavy, self-run) model. Vercel Sandbox's distinguishing bet is "managed Firecracker + public previews on the Vercel build fleet"; its distinguishing cost is that you must be on Vercel to use it.

## Catalog entry

Target category: **Agent Harnesses**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vercel-sandbox](https://github.com/vercel/sandbox) | platform | Hosted ephemeral Firecracker MicroVMs (TS SDK + CLI) to run untrusted/agent-generated code with public preview URLs | Agent-generated code needs isolated, disposable execution + a live preview, without running it on the host | sandboxd (self-hosted previews), sandcastle (orchestrates such sandboxes), forkd (KVM agent microVMs) |
