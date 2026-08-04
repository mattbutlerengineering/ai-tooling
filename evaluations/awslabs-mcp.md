# Evaluation: awslabs/mcp

**Repo:** [awslabs/mcp](https://github.com/awslabs/mcp)
**Stars:** 9,296 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A monorepo of 60+ official AWS MCP servers covering the full breadth of AWS services: compute (Lambda, ECS, EKS), databases (DynamoDB, Aurora DSQL, DocumentDB, PostgreSQL, MySQL, Keyspaces, Neptune, Redshift), storage (S3 Tables), infrastructure-as-code (CloudFormation, CDK), observability (CloudWatch, CloudTrail, Prometheus), AI/ML (SageMaker, Bedrock KB), networking, pricing, billing, security, and domain-specific verticals (HealthOmics, HealthLake, IoT SiteWise). Each server is published as a separate `uvx` package (`awslabs.<name>@latest`), runs over stdio, and installs with a single `claude mcp add` command.

The collection also includes `aws-knowledge-mcp` — a fully-managed remote MCP server hosted by AWS that provides docs, API references, What's New posts, Builder Center, blog posts, and Well-Architected guidance without any local setup.

## How we tested it

**Evidence:** REVIEW

Architecture review of the monorepo structure, README quality, security model, and Claude Code integration documentation. Examined three representative servers in depth: `aws-api-mcp-server` (general AWS CLI bridge), `aws-documentation-mcp-server` (docs lookup), and `aws-serverless-mcp-server` (Lambda/SAM lifecycle).

```bash
gh api repos/awslabs/mcp --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api 'repos/awslabs/mcp/git/trees/main?recursive=1' --jq '.tree[].path' | grep -E '^src/[^/]+$' | wc -l
# Read README, aws-api-mcp-server README, aws-serverless-mcp-server README
```

Not hands-on installed (requires AWS account and configured credentials).

## What worked

- **Scope**: 60+ servers is the most comprehensive cloud-provider MCP collection in the catalog — dwarfs cloudflare-mcp
- **Security model**: `aws-api-mcp-server` has read-only mode (`READ_OPERATIONS_ONLY`), mutation consent gates (`REQUIRE_MUTATION_CONSENT`), file access controls (workdir/unrestricted/no-access), command validation with hallucination protection, and single-tenant enforcement
- **Claude Code first-class**: dedicated setup section with `claude mcp add` commands, `.mcp.json` examples, and per-server install instructions
- **Each server is independently installable** via `uvx awslabs.<name>@latest` — install only what you need
- **OSSF Scorecard badge** in README — security-conscious development practices
- **`aws-knowledge-mcp`** is a hosted remote server requiring zero local setup — just `claude mcp add aws-knowledge-mcp --url https://knowledge-mcp.global.api.aws`

## What didn't work or surprised us

- **Python/uv dependency**: every server requires Python 3.10+ and `uv`, unlike Node-based MCP servers that run with `npx`
- **No SSE transport** — SSE was removed in May 2025, only stdio and experimental Streamable HTTP remain
- **Agent Toolkit for AWS** is positioned as the production successor — the README recommends it for "production software using coding agents", which signals this collection may become maintenance-mode
- **Telemetry enabled by default** (`AWS_API_MCP_TELEMETRY=true`) — opt-out, not opt-in
- **Kiro-first branding** — AWS's own editor (Kiro) gets top billing in install buttons; Claude Code is documented but not prioritized in the UI

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Live AWS API access prevents hallucinated resource state; command validation blocks invalid operations |
| Speed | + | 60+ servers cover nearly every AWS service — no need to build custom integrations |
| Maintainability | neutral | Well-organized monorepo but Python/uv dependency adds setup friction |
| Safety | + | Read-only mode, mutation consent, file access controls, hallucination protection, OSSF scorecard |
| Cost Efficiency | neutral | Each server is lightweight but the Python runtime is heavier than Node-based alternatives |

## Verdict

**discovery-log — tentative read**

Use when building on AWS. The collection is the definitive MCP integration for AWS services — 60+ servers with the strongest security model of any cloud-provider MCP in the catalog. The `aws-api-mcp-server` alone provides a validated bridge to every AWS CLI command with read-only and mutation-consent gates. Requires AWS account and Python/uv; the Agent Toolkit for AWS may supersede this collection for production use, but the open-source servers remain the best option for development workflows today.

## Triage note

Left at `discovery-log`. 60+ official servers with what the read above calls the strongest security
model of any cloud-provider MCP in the catalog — read-only and mutation-consent gates on a validated
bridge to the AWS CLI. Not a row a bulk lane disposes.

Checked against `cloudflare-mcp`: same shape for a different cloud, complementary by construction, and
both were left. Value is fully conditional on running on AWS, which is the standard vendor-integration
shape and neither ADOPT-everywhere nor SKIP.

The flag worth re-checking at promotion time is a succession question rather than a quality one: the
eval notes the **Agent Toolkit for AWS** may supersede this collection for production use, while the
open-source servers remain the better development-workflow option today. That is a 2026-06 read of a
moving target and is exactly the kind of claim a fresh look should verify first.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awslabs/mcp](https://github.com/awslabs/mcp) | MCP server | 60+ official AWS MCP servers: compute, databases, IaC, observability, AI/ML, and more | Need agents to interact with AWS services during development | cloudflare-mcp |
