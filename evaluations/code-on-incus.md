# Evaluation: code-on-incus (coi)

**Repo:** [mensfeld/code-on-incus](https://github.com/mensfeld/code-on-incus)
**Stars:** 554 | **Last updated:** 2026-06-19 (pushed; very active) | **License:** MIT | **Releases:** 10
**Dev loop stage:** Cross-cutting / Safety (isolation substrate for running coding agents; touches Implement)
**Layer:** Infrastructure (CLI over Incus/LXD system containers; GitHub-reported language Python, ships tagged release binaries)

---

## What it does

code-on-incus (`coi`) gives **each AI coding agent its own full machine** — an Incus (LXD) **system container** with root access, systemd, Docker, and the ability to install anything. Agents work as they would on a real server (run services, manage packages, use cron) without touching your host, and files stay correctly owned (no permission hacks). It's by Maciej Mensfeld (author of Karafka), framed explicitly as "a tool that does the job, not a product."

Two things distinguish it from generic container sandboxing:
- **Credentials stay on the host.** SSH keys, environment variables, and Git tokens are never exposed to the agent unless you explicitly mount them — a default-deny posture for secrets.
- **Active defense / security monitoring.** COI watches the container for suspicious behavior — reverse shells, credential scanning, data exfiltration — and **automatically pauses or kills** the container when it sees them, with no manual intervention. This is the standout: most sandboxes isolate but don't *detect and respond*.

It also supports running **multiple agents isolated from each other** in parallel, and **persistent dev environments** that survive restarts/reboots (snapshots, session resume, profiles, resource/time limits, network isolation) — not throwaway containers that lose setup each run. Supported agents today: Claude Code (default), opencode, pi; Aider/Cursor "coming soon." The README argues for **Incus over Docker** specifically because a full system container behaves like a real machine (systemd, Docker-in-container, persistence) rather than a single-process sandbox. macOS support is documented.

## How we tested it

**Source-grounded inspection — not installed, not run.** No Incus host set up, no agent containerized. Claims come from the repository (GitHub metadata, README, 10 tagged releases, linked wiki) — the project's own documentation, not observed isolation/defense behavior.

```bash
gh api repos/mensfeld/code-on-incus --jq '{stars,pushed_at,license:.license.spdx_id}'
gh api repos/mensfeld/code-on-incus/readme --jq '.content' | base64 -d   # isolation model, active defense, Incus rationale
gh api repos/mensfeld/code-on-incus/releases --jq 'length'              # 10
```

## What worked

- **Active defense is genuinely differentiated.** Detecting reverse shells / credential scanning / exfiltration and auto-killing the container is *response*, not just *isolation* — a meaningfully stronger safety posture than vercel-sandbox/sandboxd, and directly relevant given how much autonomy people grant agents.
- **Default-deny on credentials.** Keeping SSH keys / env / git tokens off the agent machine unless explicitly mounted is exactly the right secrets posture, and the inverse of riskier designs (cf. phantom mounting the Docker socket).
- **Full system container is the right primitive for "let the agent act like it's on a server."** systemd + Docker + package managers + persistence + correct file ownership removes the friction that makes single-process sandboxes leaky or annoying.
- **Parallel isolation + persistence + snapshots** make it practical for real multi-agent workflows, not just demos.
- **MIT, very active, credible author.** Pushed the day of evaluation, 10 releases, by a known OSS/security-minded maintainer.

## What didn't work or surprised us

- **Incus/LXD is a real prerequisite.** This is a Linux-container substrate; adopting it means running Incus (macOS support exists but adds a layer). Heavier setup than "pip install," and not a fit if you can't run Incus.
- **Smaller/younger** (554★) than the headline sandboxes; the active-defense detections are heuristic and unverified here — false negatives (missed novel exfil) and false positives (killing a legitimate long task) are both plausible and untested.
- **Language signal is mixed.** GitHub reports the repo language as Python while the project ships release binaries and centers on Incus orchestration — verify the toolchain before building from source.
- **Scope is isolation, not code quality.** It makes running agents safer; it doesn't review or improve what they produce.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't change agent output; provides a clean, reproducible machine to work in. |
| Speed | + / neutral | Persistent environments + snapshots avoid re-setup each run; Incus overhead is modest vs. full VMs. |
| Maintainability | neutral | Affects your run environment, not your codebase. |
| Safety | + + | Per-agent full isolation, host credentials withheld by default, **and active detection+auto-kill** of reverse shells/exfil/credential scanning — the strongest defensive posture in this group. |
| Cost Efficiency | + | Free/MIT; self-hosted on your own machines; system containers are lighter than per-agent VMs. |

## Verdict

**CONDITIONAL** — adopt if you run coding agents (especially several in parallel, or with high autonomy) on Linux and want strong, defense-in-depth isolation: full per-agent machines, host credentials withheld by default, and **automated detection-and-response** to suspicious agent behavior. The active-defense layer is a real step beyond passive sandboxing and the secrets posture is exactly right. Gated by the Incus/LXD requirement and its relative youth — the heuristic detections are unverified, so treat auto-kill as a safety net, not a guarantee. If you can't run Incus, vercel-sandbox (cloud) or sandboxd are the alternatives; if you specifically want *response*, this is the one.

Compared to neighbors: **sandboxd**/**vercel-sandbox** isolate agent execution (the latter cloud-hosted) but focus on containment, not detection; **agentlint** adds rule-based runtime guardrails at the action level. code-on-incus is the **full-machine isolation + active intrusion-response** option — the only one here that watches the sandbox and kills it on attack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [code-on-incus](https://github.com/mensfeld/code-on-incus) | tool | Gives each AI agent its own full Incus/LXD machine (root, systemd, Docker, persistence) with host credentials withheld by default and active defense that auto-kills on reverse shells/exfil/credential scanning | Agents need full machine access without risking your host or credentials, and you want suspicious behavior caught and stopped, not discovered after the fact | sandboxd, vercel-sandbox, agentlint |
