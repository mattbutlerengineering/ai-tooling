# Evaluation: agent-sandbox

**Repo:** [agent-sandbox/agent-sandbox](https://github.com/agent-sandbox/agent-sandbox)
**Stars:** ~150 | **Last updated:** 2026-06-08 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (code-execution infrastructure)
**Layer:** Infrastructure

---

## What it does

An open-source, self-hosted sandbox runtime for AI agents that is **fully compatible with the E2B protocol and SDKs** (positioned as an E2B / Blaxel Sandbox alternative). It combines Kubernetes with container isolation to let agents securely run untrusted LLM-generated code, browser use, computer use, and shell commands.

Mechanically, it exposes a RESTful API and an **MCP server** to manage the sandbox lifecycle (create/access/delete), abstracting away raw Kubernetes. Sandboxes are stateful, long-running, and explicitly **multi-session and multi-tenant** — isolated on a per-agent or even per-user basis so different conversations/tasks can't interfere with each other. The README frames the motivation against `kubernetes-sigs/agent-sandbox` + AIO Sandbox (powerful but Kubernetes-facing and not agent-friendly), aiming to provide the same isolation with a simpler API/MCP interface plus a web UI.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the stated design (E2B-compatible API/SDKs, MCP-managed lifecycle, K8s + container isolation, multi-session/multi-tenant per-agent/per-user isolation). Confirmed the E2B-protocol compatibility claim and the RESTful-API + MCP-server management surface. Note: the README ships a default UI admin token in plaintext — fine for a demo, but a deployment hardening item. Not deployed live (needs a Kubernetes cluster), so condition-gated.

```bash
gh api repos/agent-sandbox/agent-sandbox --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/agent-sandbox/agent-sandbox/readme --jq '.content' | base64 -d
```

## What worked

- **Drop-in E2B alternative, self-hosted.** Full E2B protocol/SDK compatibility means you can move off hosted E2B to your own infra without rewriting agent code — a clear lock-in escape hatch.
- **Per-user/per-agent isolation.** Multi-session, multi-tenant isolation is exactly the requirement for safely running untrusted code across concurrent users/agents.
- **MCP-managed lifecycle.** Exposing sandbox management as an MCP server lets agents create/destroy sandboxes natively, and hides Kubernetes complexity.

## What didn't work or surprised us

- **Young and small.** ~150 stars; far less proven than Daytona or hosted E2B — evaluate stability before production reliance.
- **Kubernetes required.** Self-hosting means operating a K8s cluster; the abstraction helps users but not operators.
- **Security hygiene in docs.** A plaintext default admin token in the README is a yellow flag — rotate/secure on deploy.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Isolated, stateful environments give reproducible execution |
| Speed | neutral | Performance unverified; K8s scheduling adds startup variance |
| Maintainability | + | E2B compatibility avoids SDK rewrites; MCP-managed lifecycle |
| Safety | + | Per-agent/per-user multi-tenant isolation for untrusted code |
| Cost Efficiency | + | Self-hosted, free (Apache-2.0); you own the compute |

## Verdict

**CONDITIONAL**

Adopt when you specifically want a self-hosted, E2B-compatible sandbox to escape hosted-E2B lock-in and run untrusted agent code with per-user isolation — and you already operate Kubernetes. For broader, more proven execution infra, Daytona is the heavier-but-mature option. Given the small footprint, pilot it and harden defaults (admin token) before production.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-sandbox](https://github.com/agent-sandbox/agent-sandbox) | tool | Self-hosted, E2B-compatible agent sandboxes (Apache-2.0) — K8s + container isolation with a RESTful API and MCP server for per-agent/per-user, multi-session, multi-tenant sandboxes running untrusted LLM code/browser/shell | Want an open-source, self-hosted E2B/Blaxel alternative with per-user isolation and MCP-managed lifecycle, without raw Kubernetes | daytona, e2b (ext.), chrome-devtools-mcp |
