# Evaluation: daytona

**Repo:** [daytonaio/daytona](https://github.com/daytonaio/daytona)
**Stars:** ~72,400 | **Last updated:** 2026-06-19 | **License:** AGPL-3.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
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

**SKIP — discontinued upstream, no open-source successor.** Daytona's own README now opens with a
banner this evaluation was written before:

> **This repository is no longer maintained.** As of **June 2026**, Daytona's core development has
> moved to a **private codebase**. This repository will receive no further updates, fixes, or
> releases. It remains public and free to use, fork, and build on under the LICENSE, as is and
> without support or warranty.

Verified independently on 2026-08-04 rather than taken from the banner:

| Check | Result |
|---|---|
| `archived` flag | **false** — which is why band P1 never saw it |
| Last push | 2025-07-24 |
| `GET /repos/daytonaio/daytona/license` | **404** |
| `LICENSE` in the HEAD tree (recursive) | **absent** — the README's own link points at tag `v0.190.0`, not `main` |
| Successor org `github.com/daytona` (34 repos) | SDKs, `legacy-daytona-provider-*`, docs/content — **no successor to the core engine** |

So this is a P1 successor-check in substance that the structural band could not reach. **P1 keys on
`archived == true`, and a project can announce its own discontinuation while staying unarchived.**
Daytona did exactly that two months ago, and nothing in the repo's automation noticed — this row was
sitting in P3 as ordinary backlog.

Applying P1's own rule — "repoint the link to a successor, or SKIP 'archived, no successor'" — there
is no successor to repoint to. The *product* continues as a hosted service at daytona.io, but that is
a different artifact from the self-hostable open-source engine this row recommends, and the catalog
cannot recommend a closed codebase it cannot inspect.

**The license position is worse than the eval recorded.** That eval says "weigh AGPL-3.0 obligations
for productized/networked use". AGPL-3.0 is what the *cache* said; HEAD now carries no LICENSE file at
all. Anyone who takes the README's advice to "fork and build on" is forking from a tag, not from
`main`. Recorded because this cuts the opposite way to the `vercel-labs/skills` case earlier in this
lane, where a cached `NONE` had quietly become MIT — licenses move in both directions and the cache
tracks neither.

**Blast radius.** Daytona is named as the mature, proven option in sibling evals: `agent-sandbox`
("far less proven than Daytona"), `beta9`, `cua` (pair with isolation), `flue`, `axern`,
`agent-governance-toolkit`, and as an execution backend in `harbor`, `cognee` and `omnigent`. The
directly inverted claim in `agent-sandbox.md` has been corrected in this pass; the rest are
comparative mentions that a maintainer should re-read now that the comparator is gone. That
cross-file staleness is invisible to detector D, which only checks an eval against its own
`COMPARISON.md` row.

Re-open if the core engine returns to a public repository under a declared license, or if a maintained
community fork of `v0.190.0` establishes itself — the design was good and the eval's technical read of
it is not in dispute.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [daytona](https://github.com/daytonaio/daytona) | platform | Secure, elastic sandbox infrastructure for running AI-generated code (AGPL-3.0, ★72K) — fully-isolated composable computers (own kernel/fs/network/vCPU) spinning up in <90ms with stateful snapshots; driven via SDK/API/CLI | Running untrusted LLM-generated code is unsafe and non-reproducible; want fast, isolated, persistent execution sandboxes for agents | agent-sandbox, e2b (ext.), opensquilla |
