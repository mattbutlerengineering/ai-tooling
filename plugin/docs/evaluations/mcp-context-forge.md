# Evaluation: mcp-context-forge

**Repo:** [IBM/mcp-context-forge](https://github.com/IBM/mcp-context-forge)
**Stars:** ~3,930 | **Last updated:** 2026-06-20 | **License:** Apache-2.0
**Dev loop stage:** Implement (MCP infrastructure / gateway)
**Layer:** Infrastructure

---

## What it does

"ContextForge" is an open-source registry and proxy from IBM that **federates MCP, A2A, and REST/gRPC APIs** into one governed endpoint for AI clients, with centralized governance, discovery, and observability.

Per the README it provides four layers: a **Tools Gateway** (MCP, plus REST/gRPC-to-MCP translation and TOON compression), an **Agent Gateway** (A2A protocol with OpenAI-compatible and Anthropic agent routing), an **API Gateway** (rate limiting, auth, retries, reverse proxy for REST), and **plugin extensibility** (40+ plugins for transports/protocols/integrations). It adds OpenTelemetry tracing (Phoenix/Jaeger/Zipkin/other OTLP backends). It runs as a fully-compliant MCP server, deploys via PyPI or Docker, and scales to multi-cluster Kubernetes with Redis-backed federation and caching.

## How we tested it

Architecture review against the README and the four-gateway model (Tools/Agent/API gateways + plugins + OTel observability). Confirmed the federate-and-govern positioning (one endpoint over many MCP/A2A/REST sources), the protocol translation (REST/gRPC→MCP), and the K8s/Redis federation. IBM-maintained, Apache-2.0. Not deployed live, so condition-gated.

```bash
gh api repos/IBM/mcp-context-forge --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/IBM/mcp-context-forge/readme --jq '.content' | base64 -d
```

## What worked

- **Centralized governance over MCP sprawl.** As teams accumulate many MCP/A2A/REST endpoints, one proxied, access-controlled, observable gateway with discovery is exactly the missing operational layer — this is the "API gateway" pattern applied to the agent-tool ecosystem.
- **Protocol federation + translation.** REST/gRPC→MCP translation and A2A routing let you expose existing services to agents without rewriting them as MCP servers.
- **Observability + scale, IBM-backed.** OpenTelemetry tracing and K8s/Redis federation make it production-grade, with credible enterprise maintainership.

## What didn't work or surprised us

- **Enterprise weight.** It's infrastructure to deploy and operate (PyPI/Docker/K8s), not a drop-in — justified at organizational scale, overkill for a solo user with two MCP servers.
- **Overlaps gateways partially.** Routing/guardrails overlap bifrost/Portkey (LLM gateways); ContextForge's distinct angle is the MCP/A2A/tool registry + governance, not LLM provider routing.
- **Newer, broad surface.** Four gateways + 40 plugins is a large surface to evaluate for the specific federation you need.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Central discovery/registry avoids stale/duplicate tool wiring |
| Speed | + | One endpoint + caching/federation vs. per-source client config |
| Maintainability | + | Centralized governance/discovery over many MCP/A2A/REST sources |
| Safety | + | Auth, rate limiting, and access control at the gateway chokepoint |
| Cost Efficiency | + | TOON compression + caching; reuse existing REST/gRPC services |

## Verdict

**CONDITIONAL**

Adopt at team/org scale when you run many MCP/A2A/REST endpoints and need a central registry + proxy with governance, discovery, access control, and observability — the "API gateway for agent tools." It's infrastructure to operate, so it's overkill for a couple of personal MCP servers. Distinct from LLM gateways (bifrost/Portkey): ContextForge federates *tools/agents/APIs*, not LLM providers. Strong, IBM-backed option for MCP at scale.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-context-forge](https://github.com/IBM/mcp-context-forge) | MCP server | MCP/A2A/REST registry + gateway (Apache-2.0, by IBM) — "ContextForge" federates tools, agents, and APIs into one governed endpoint: Tools Gateway (MCP + REST/gRPC-to-MCP + TOON compression), Agent Gateway (A2A + OpenAI/Anthropic routing), API Gateway (rate limit/auth/retries), 40+ plugins, OTel observability; scales on K8s with Redis federation | Agents accumulate many MCP/A2A/REST endpoints with no central governance/discovery; want one proxied, observable, access-controlled gateway over all of them | bifrost, Portkey-gateway, fastmcp, mcp-use |
