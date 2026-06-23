# Evaluation: agent-vault

**Repo:** [Infisical/agent-vault](https://github.com/Infisical/agent-vault)
**Stars:** 1,699 | **Last updated:** 2026-06-19 | **License:** MIT (Expat; `ee/` dir reserved for enterprise)
**Dev loop stage:** Ship / Implement (runtime infrastructure that wraps the agent process during any outbound API call)
**Layer:** Infrastructure

---

## What it does

HTTP credential proxy and vault for AI coding agents. Agent Vault is a single Go binary (server + CLI) that sits as a man-in-the-middle (MITM) forward proxy between an agent and the public APIs it calls (Anthropic, GitHub, Stripe, etc.). You store the real secrets in the vault (`ANTHROPIC_API_KEY`, `GITHUB_PAT`, …) and the agent's environment only ever holds **dummy placeholder values** like `__anthropic_api_key__`. The agent makes normal HTTPS calls; the proxy intercepts each outbound request and **substitutes the placeholder header value (or replaces the auth header entirely) with the real credential before forwarding** to the upstream. The real key never enters the agent's process, environment, or context window.

The mechanism, from the README and source (`cmd/run.go`, `cmd/server.go`):
- Server runs an HTTP management API/UI on `:14321` and a MITM proxy on `:14322` (one listener handling both `CONNECT` for HTTPS upstreams and absolute-form forward-proxy for HTTP).
- The agent is bootstrapped with `HTTPS_PROXY=agent-vault:14322` plus a mounted CA certificate so the agent trusts the proxy's TLS interception.
- `agent-vault run -- claude` (and `… -- codex / opencode / agent`) wraps the agent process: it mints a vault-scoped session token, sets the proxy env vars, and execs the child. There is explicit first-class Claude Code support, including macOS Keychain bridging (`cmd/claude_credentials.go`) that extracts the host's Claude Code OAuth credential into a file the container bind-mount can carry.
- Additional controls layered on the proxy choke point: **egress filtering** (allow/deny which agents reach which services/endpoints), **request logging** (inspect authenticated traffic), and `unmatched_host_policy=deny` (strict mode rejecting any unmatched host with 403). Pluggable credential stores let it back onto Infisical for dynamic/rotating secrets.
- A TypeScript SDK (`@infisical/agent-vault-sdk`) lets an orchestrator mint short-lived, vault-scoped tokens and `buildProxyEnv()` for ephemeral sandboxes (Docker, Daytona, E2B, Firecracker).

The intended deployment is the load-bearing security assumption: Agent Vault must run **on a separate host from the agent** so a compromised agent cannot read the vault's local store. Co-located on one box, the guarantee weakens to "not in the agent's context" rather than "not on the agent's machine."

## How we tested it

**Evidence:** REVIEW

**Method: inspected the GitHub repo, full README, repo file tree, and selected Go source; did not install or run the proxy.** No live credential interception, latency, or egress-filter behavior was exercised; all behavior below is read from the README and source, not measured. The decisive catalog questions — what the mechanism actually is, whether Claude Code is a first-class target, and the maturity/credibility of the project — are answerable from source and metadata, which is sufficient to settle the verdict. The "no hands-on install" caveat means I cannot report setup time, false-positive egress rules, or proxy overhead from observation.

```bash
gh api repos/Infisical/agent-vault --jq '{stars,license:.license.spdx_id,description,pushed_at,created_at,archived,open_issues,forks,homepage}'
gh api repos/Infisical/agent-vault/contents/README.md --jq '.content' | base64 -d
gh api "repos/Infisical/agent-vault/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/Infisical/agent-vault/contents/cmd/run.go --jq '.content' | base64 -d | head -50
gh api repos/Infisical/agent-vault/contents/cmd/claude_credentials.go --jq '.content' | base64 -d
gh api repos/Infisical/agent-vault/contributors --jq '.[] | {login,contributions}'
gh api repos/Infisical/agent-vault/releases --jq '.[0:3]'   # v0.36.1, 30 tags
```

Confirmed: first-class agent wrapping (`cmd/run.go` `run -- <agent>` with admin and agent/token modes), explicit Claude Code Keychain bridging (`cmd/claude_credentials.go`), ~50 `cmd/*.go` files plus `internal/` packages, CI workflow, dependabot, goreleaser release pipeline with **build-provenance attestation + cosign signing** of release binaries (`gh attestation verify`), `SECURITY.md`, and a docs site (docs.agent-vault.dev). Maintained by Infisical (lead `dangtony98` = Infisical co-founder, 155 commits; multiple Infisical staff contributors). Created 2026-03-27, pushed same day as evaluation. Versioned `v0.36.1` and README explicitly labels it **"Preview … API subject to change."**

## What worked

- **The mechanism actually removes raw credentials from the agent's reach, not just its prompt.** Placeholder-substitution at the proxy means the agent's env holds `__anthropic_api_key__`, never the real key. This directly defeats the named threat — prompt-injection-driven credential exfiltration — because there is no real secret on the agent host to exfiltrate (when deployed on a separate host as recommended).
- **First-class coding-agent integration, Claude Code included.** `agent-vault run -- claude` is a documented one-liner; `codex`, `opencode`, and generic `agent` are equally supported. The macOS Keychain bridge shows real attention to the Claude Code auth path, not just generic proxying.
- **Defense-in-depth at one choke point.** Because all authenticated traffic flows through the proxy, the same component gives egress filtering (which services/endpoints an agent may reach), strict deny mode (403 unmatched hosts), and full request logging for audit — capabilities a sandbox or deny-rule hook cannot offer.
- **High engineering maturity for the category and strong vendor credibility.** Single Go binary, install script, Docker image, TS SDK, CI, dependabot, goreleaser, and **cryptographically attested + cosigned release binaries** — supply-chain hygiene most catalog safety tools lack. Backed by Infisical, an established open-source secrets-management company, which materially lowers abandonment and trust risk versus a solo-maintainer project.
- **Honest threat-model framing.** The README is candid that the security guarantee depends on running Agent Vault on a *separate host* from the agent, and that the proxy port must stay private. It does not oversell a co-located deployment.
- **Built for ephemeral sandboxes.** The SDK's short-lived, vault-scoped token minting (`sessions.create`) plus `buildProxyEnv()` fit the remote/sandboxed coding-agent pattern cleanly — mint a token, pass proxy env + CA cert into the sandbox, agent calls APIs normally.

## What didn't work or surprised us

- **MITM TLS interception is the cost of entry.** The agent must trust Agent Vault's CA certificate for the proxy to read and rewrite HTTPS requests. That is a real, deliberate weakening of TLS end-to-end integrity inside the agent's environment, and it requires mounting/installing a CA in every agent runtime (`SSL_CERT_FILE`, `NODE_EXTRA_CA_CERTS`, `REQUESTS_CA_BUNDLE`, `GIT_SSL_CAINFO`, …). Workable, but non-trivial setup friction.
- **Correct deployment is a two-host operational commitment.** The headline guarantee ("agents never possess credentials") only fully holds when the vault runs on a separate machine. The simplest local setup (one box) degrades the guarantee and is easy to get subtly wrong. This is infrastructure, not a drop-in hook — there is a server to run, secure, and keep up.
- **"Preview" status, pre-1.0, fast-moving API.** 30 tags in under three months and an explicit "API subject to change" warning. Adopting now means tracking breaking changes; the project is young (created 2026-03-27) despite the high star count.
- **Overkill for the common solo/local dev loop.** For a developer running Claude Code on their own laptop with their own keys, standing up a separate-host MITM proxy is disproportionate. The payoff concentrates in remote/sandboxed/multi-tenant/team deployments where the agent host is untrusted.
- **Not installed here, so setup-time, egress-rule ergonomics, and proxy latency are unverified.** The README claims purpose-built ergonomics over `mitmproxy`/`squid`; I could not confirm this hands-on.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Does not change the code the agent produces; purely controls credential access |
| Speed | - (minor) | Adds a MITM proxy hop on every outbound API call; README recommends co-locating to limit latency; overhead unmeasured here |
| Maintainability | neutral | No effect on codebase structure; centralizes credential config/rotation but adds a service to operate |
| Safety | ++ | Removes raw credentials from the agent's environment/context entirely, defeating prompt-injection exfiltration; adds egress filtering, strict deny mode, and audit logging at one choke point |
| Cost Efficiency | + | Centralized broker enables short-lived/scoped tokens and rotation; preventing one leaked long-lived API key or PAT pays for the operational cost; running a separate host is the standing cost |

## Verdict

**CONDITIONAL**

Adopt when an agent runs somewhere you do not fully trust — remote coding agents, ephemeral/sandboxed agents, CI runners, or any multi-tenant/team setup where a credential leak via prompt injection is a real and consequential risk. In those settings Agent Vault is the strongest fit in the catalog: it removes raw secrets from the agent's reach (not merely its prompt) and adds egress filtering plus audit logging at the proxy choke point, with Infisical's credibility and genuinely good supply-chain hygiene (attested, cosigned binaries) behind it. It does not clear the ADOPT ("use everywhere") bar because the value depends on a two-host deployment, requires CA-trust/MITM setup in every agent runtime, and is "Preview"/pre-1.0 with a fast-changing API — disproportionate for a solo developer running Claude Code locally with their own keys.

Keeping secrets out of agent context is a real and increasingly common dev-loop need (it is exactly why Anthropic and others warn about prompt-injection exfiltration), but it is acute mainly once the agent host is untrusted; for the local single-developer case the friction outweighs the payoff, which is what keeps this CONDITIONAL rather than ADOPT.

**Differentiation from overlaps.** Genuinely unique in the catalog — it is the only **credential-proxy / brokered-access** entry. It is a different axis from the other Safety tools: **cc-safety-net** (CONDITIONAL) blocks destructive *git/filesystem commands* pre-execution via a PreToolUse hook; **hol-guard** vets *what runs* (extensions/packages) at harness launch; **agentlint** broadly constrains *agent actions* with rule packs. None of them touch the *credential-access* problem. Agent Vault is complementary to all three: it governs the secrets the agent can use and where its authenticated traffic may go, while the others govern the commands and code the agent executes. Its closest conceptual cousins are general forward proxies (`mitmproxy`, `squid`), which it positions itself against by being purpose-built for agent ergonomics with a CLI, multi-tenancy, and credential-substitution semantics.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-vault](https://github.com/Infisical/agent-vault) | tool | HTTP credential proxy and vault for AI coding agents (1.7K stars) | AI agents need access to secrets but shouldn't have direct credential access | — (unique: credential proxy for agents) |
