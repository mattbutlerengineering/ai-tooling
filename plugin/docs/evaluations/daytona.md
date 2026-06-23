# Evaluation: daytona

**Repo:** [daytonaio/daytona](https://github.com/daytonaio/daytona)
**Stars:** ~72,400 | **Last updated:** 2026-06-19 | **License:** AGPL-3.0
**Dev loop stage:** Implement (code-execution infrastructure)
**Layer:** Infrastructure

---

## What it does

Secure, elastic infrastructure for running AI-generated code. Daytona's core primitive is the **sandbox**: a fully-isolated "composable computer" with a dedicated kernel, filesystem, network stack, and allocated vCPU/RAM/disk.

Mechanically, sandboxes spin up in under 90ms from code to execution, run Python/TypeScript/JavaScript, and are built on OCI/Docker compatibility for massive parallelization and unlimited persistence. Agents and developers drive them programmatically via Daytona SDKs, an API, and a CLI — covering sandbox lifecycle management, filesystem operations, and process/code execution, with runtime configuration through base images and packages. Stateful **snapshots** persist a sandbox's environment across sessions, enabling long-running agent operations. There's a self-hostable open-source platform plus a managed cloud, with organizational governance/operational controls.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README, the sandbox model (isolation, <90ms cold start, snapshots), and the SDK/API/CLI surface. Confirmed the OCI/Docker foundation, the per-sandbox isolation guarantees, and the stateful-snapshot persistence story. Did not provision live sandboxes (needs an account/self-host deploy and a real agent workload), so verdict is condition-gated.

```bash
gh api repos/daytonaio/daytona --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/daytonaio/daytona/readme --jq '.content' | base64 -d
```

## What worked

- **Real isolation for untrusted code.** Dedicated kernel + filesystem + network per sandbox is the right safety posture for executing LLM-generated code — far stronger than running it on the host or in a shared container.
- **Fast + persistent.** <90ms cold start makes per-task sandboxes practical, and snapshots give agents durable state across sessions — a hard combination to get right.
- **Programmatic-first.** SDK/API/CLI designed for agents to manage lifecycle/filesystem/execution makes it a clean foundation for agentic architectures, not just a human dev-env tool.

## What didn't work or surprised us

- **AGPL-3.0.** The strong copyleft license matters if you embed Daytona in a networked service — review obligations before building a product on the self-hosted platform (or use the cloud).
- **Infrastructure weight.** This is a platform to operate (or pay for), not a drop-in library; justified only when you actually run untrusted/parallel agent code.
- **Overlaps E2B / agent-sandbox.** The hosted-sandbox space is competitive; Daytona's edge is scale, cold-start speed, and snapshot persistence.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Consistent, reproducible environments for agent execution |
| Speed | + | <90ms sandbox cold start enables fast per-task isolation |
| Maintainability | + | Snapshots + IaC-style base images make environments repeatable |
| Safety | + | Full per-sandbox isolation contains untrusted LLM-generated code |
| Cost Efficiency | ✓/$ | Self-host free (AGPL); managed cloud and compute cost at scale |

## Verdict

**CONDITIONAL**

Adopt when you run untrusted or parallel AI-generated code and need real isolation with fast cold starts and persistent state — the canonical foundation for agent code-execution. Weigh AGPL-3.0 obligations for productized/networked use, and prefer it over running LLM code on the host. For lighter, E2B-protocol needs, agent-sandbox is a self-hosted alternative.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [daytona](https://github.com/daytonaio/daytona) | platform | Secure, elastic sandbox infrastructure for running AI-generated code (AGPL-3.0, ★72K) — fully-isolated composable computers (own kernel/fs/network/vCPU) spinning up in <90ms with stateful snapshots; driven via SDK/API/CLI | Running untrusted LLM-generated code is unsafe and non-reproducible; want fast, isolated, persistent execution sandboxes for agents | agent-sandbox, e2b (ext.), opensquilla |
