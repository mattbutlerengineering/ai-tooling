# Evaluation: vps-forge

**Repo:** [mountain-beaver/vps-forge](https://github.com/mountain-beaver/vps-forge)
**Stars:** 35 | **Last updated:** 2026-10-26 (pushed) | **License:** MIT
**Last verified:** 2026-10-31
**Last triaged:** 2026-10-31  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (VPS/server provisioning and hardening, not application code)
**Layer:** Infrastructure

---

## What it does

An agent skill (MIT) that lets Claude Code, Codex, Cursor, Copilot, and other AI agents set up and harden a Debian/Ubuntu VPS without locking the operator out — SSH, firewall, fail2ban, updates, Docker, TLS, backups, phone alerts — benchmarked on 120 VM runs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (cc-safety-net, your-cto-jev, agent-governance-toolkit). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead.

## Triage note

P3 backlog. Left at `discovery-log`; its overlaps (cc-safety-net, your-cto-jev, agent-governance-toolkit) are a loose safety-net/governance theme, not a direct competitor on the same job — none is a STACK ADOPT/KEEP pick, so it doesn't land in P2. No existing catalog entry covers agent-driven VPS hardening specifically, and the repo's own "benchmarked on 120 VM runs" claim is worth verifying hands-on before any disposition.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vps-forge](https://github.com/mountain-beaver/vps-forge) | skill | Agent skill (MIT) hardening a Debian/Ubuntu VPS — SSH, firewall, fail2ban, Docker, TLS, backups, benchmarked on 120 VM runs | Agents setting up or hardening a VPS have no curated, benchmarked hardening skill and can lock the operator out | cc-safety-net, your-cto-jev, agent-governance-toolkit |
