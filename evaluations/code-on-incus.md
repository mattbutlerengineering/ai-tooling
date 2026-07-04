# Evaluation: code-on-incus (coi)

**Repo:** [mensfeld/code-on-incus](https://github.com/mensfeld/code-on-incus)
**Stars:** 554 | **Last updated:** 2026-06-19 (pushed; very active) | **License:** MIT | **Releases:** 10
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
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

**Evidence:** REVIEW

**Source-grounded review — not run hands-on.** A hands-on run was attempted this session and could not be completed: the substrate (Incus/LXD) is not installed and could not be installed in this environment. The claims below come from the repository (GitHub metadata, README, 10 tagged releases, linked wiki) — the project's own documentation, not observed isolation/defense behavior. Per the repo's honesty standard, nothing here asserts a run that did not happen.

**The install attempt (what was actually run, and what blocked it).** The probe results below *are* measured — they are real output from this macOS host, and they establish why the agent-isolation behavior could not be exercised:

```bash
$ uname -sm
Darwin arm64                       # macOS on Apple Silicon — no native Linux kernel

$ which incus lxc lxd limactl docker colima multipass
incus not found                    # the substrate coi orchestrates — ABSENT
lxc not found
lxd not found
limactl not found                  # no Lima VM to host a Linux Incus daemon
/usr/local/bin/docker              # only Docker present (and coi is explicitly NOT Docker-based)
colima not found
multipass not found
```

Three independent blockers, each sufficient on its own:
1. **No Incus/LXD on the host.** `coi` is a thin orchestrator over Incus system containers; with no `incus` binary and no daemon, there is nothing for it to drive. This is the load-bearing prerequisite, and it is absent.
2. **Wrong kernel for the primitive.** Incus/LXD system containers are a **Linux** technology (they share the host's Linux kernel). On macOS arm64 they require a Linux VM underneath (e.g. via Lima/`limactl`) — and no such VM runtime is installed here either. The README's "macOS support" is precisely this VM-backed path; standing it up is a multi-step infra task, not a `pip install`.
3. **No network egress in this sandbox.** Outbound fetches (`gh api`, `WebFetch`, `brew info incus`, `docker info`) were denied by the environment's permission policy, so neither Incus nor `coi` could be downloaded/installed, and the live README install commands could not be re-fetched and verified against a real install here.

Because the active-defense layer (detect reverse shell / credential-scan / exfil, then auto-kill) is the entire reason this tool is interesting for STACK promotion, and that behavior can only be observed by launching a real agent inside a real Incus container under attack, **the distinguishing claim remains unverified.** A trustworthy hands-on validation needs a Linux host (or a Linux VM on macOS) with Incus initialized — infrastructure this environment does not provide.

## What worked

- **Active defense is genuinely differentiated (on paper).** Detecting reverse shells / credential scanning / exfiltration and auto-killing the container is *response*, not just *isolation* — a meaningfully stronger safety posture than vercel-sandbox/sandboxd, and directly relevant given how much autonomy people grant agents. (Documented, not yet observed here.)
- **Default-deny on credentials.** Keeping SSH keys / env / git tokens off the agent machine unless explicitly mounted is exactly the right secrets posture, and the inverse of riskier designs (cf. phantom mounting the Docker socket).
- **Full system container is the right primitive for "let the agent act like it's on a server."** systemd + Docker + package managers + persistence + correct file ownership removes the friction that makes single-process sandboxes leaky or annoying.
- **Parallel isolation + persistence + snapshots** make it practical for real multi-agent workflows, not just demos.
- **MIT, very active, credible author.** Pushed the day of evaluation, 10 releases, by a known OSS/security-minded maintainer.

## What didn't work or surprised us

- **The substrate is a hard, host-level prerequisite — and it stopped this evaluation cold.** The measured probe above confirms it: no `incus`/`lxc`/`lxd`, and on macOS arm64 you must first run a Linux VM before Incus can exist at all. This is real infrastructure, far heavier than "install a CLI," and it is the single biggest barrier to an every-project STACK slot.
- **The headline safety claim is unverified here.** The active-defense detections are heuristic; false negatives (missed novel exfil) and false positives (killing a legitimate long-running task) are both plausible and were **not** testable in this environment. Treat the auto-kill as an unproven safety net until exercised on a Linux host.
- **Smaller/younger** (554★) than the headline sandboxes — less battle-testing behind the active-defense heuristics.
- **Language signal is mixed.** GitHub reports the repo language as Python while the project ships release binaries and centers on Incus orchestration — verify the toolchain before building from source.
- **Scope is isolation, not code quality.** It makes running agents safer; it doesn't review or improve what they produce.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't change agent output; provides a clean, reproducible machine to work in. |
| Speed | + / neutral | Persistent environments + snapshots avoid re-setup each run; Incus overhead is modest vs. full VMs (claimed, not measured here). |
| Maintainability | neutral | Affects your run environment, not your codebase. |
| Safety | + + (claimed) | Per-agent full isolation, host credentials withheld by default, **and active detection+auto-kill** of reverse shells/exfil/credential scanning — the strongest defensive posture in this group on paper. **Not verified hands-on:** the substrate (Incus/LXD) was absent and could not be installed here, so the detect-and-respond behavior was never exercised. |
| Cost Efficiency | + | Free/MIT; self-hosted on your own machines; system containers are lighter than per-agent VMs. |

## Verdict

**CONDITIONAL (and DEFER for STACK promotion).** Adopt *conditionally* if you run coding agents (especially several in parallel, or with high autonomy) **on Linux** and want strong, defense-in-depth isolation: full per-agent machines, host credentials withheld by default, and automated detection-and-response to suspicious agent behavior. The design is the most defensible in this group and the secrets posture is exactly right.

For an **every-project STACK slot, it does not qualify** — and this evaluation's failed install attempt is the concrete reason. STACK membership requires a tool that moves a quality signal *in real testing* and installs cleanly enough to run on every project. `coi`'s value (Safety via active defense) is precisely the part this evaluation could **not** verify, because its load-bearing prerequisite — an Incus/LXD daemon — is absent on the host and unavailable on macOS arm64 without first standing up a Linux VM (also absent). A tool that needs a Linux host or a VM-backed Incus install before it can do anything is by definition not an every-project install; it's a deliberate, Linux-fleet, high-autonomy choice. **Keep it catalogued as the full-machine-isolation + active-response option; re-evaluate for a STACK slot only after a real hands-on run on a Linux host (or VM-backed Incus on macOS) confirms the detect-and-kill behavior fires correctly and without crippling false positives.**

Compared to neighbors: **sandboxd**/**vercel-sandbox** isolate agent execution (the latter cloud-hosted, so no local substrate to install) but focus on containment, not detection; **agentlint** adds rule-based runtime guardrails at the action level. code-on-incus is the **full-machine isolation + active intrusion-response** option — the only one here that watches the sandbox and kills it on attack — but also the heaviest to stand up, which is exactly why it stays CONDITIONAL rather than ADOPT.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [code-on-incus](https://github.com/mensfeld/code-on-incus) | tool | Gives each AI agent its own full Incus/LXD machine (root, systemd, Docker, persistence) with host credentials withheld by default and active defense that auto-kills on reverse shells/exfil/credential scanning | Agents need full machine access without risking your host or credentials, and you want suspicious behavior caught and stopped, not discovered after the fact | sandboxd, vercel-sandbox, agentlint |
