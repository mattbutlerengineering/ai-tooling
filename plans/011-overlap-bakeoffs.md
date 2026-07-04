# Plan 011: Establish overlap-cluster bake-offs — protocol plus one pilot (Memory & Context)

> **Executor instructions**: Follow step by step; verify each step. On any
> STOP condition, stop and report. Update this plan's row in `plans/README.md`
> when done. NOTE Step 3 requires actually running two tools hands-on — if
> you are an unattended executor without the ability to run them honestly,
> do Steps 1-2 only and mark the plan BLOCKED(pilot needs attended run).
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- evaluations/ WORKFLOW.md CATALOG.md COMPARISON.md`
> On drift, re-verify "Current state" first.

## Status

- **Priority**: P2
- **Effort**: M (protocol S + pilot M)
- **Risk**: MED (the pilot involves real tool runs; honesty gates will correctly reject a thin result)
- **Depends on**: plans/009-measurement-protocols.md (the pilot measures under its protocols)
- **Category**: direction (methodology)
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

The question users actually face is "A or B for the same job?" — and the repo barely answers it: 2 dedicated head-to-head evals out of 487 (`mattpocock-vs-agent-skills.md`, `mem0-vs-claude-mem.md`), and the latter is Evidence SOURCE-ONLY, resting on unreproduced vendor benchmarks — exactly the pattern `token-savings-protocol.md` was written to prevent. Every catalog row names its "Overlaps with" peers and WORKFLOW.md lists 5 "Overlap groups (compared competitors, picked a winner)", but winners were picked by prose judgment, not a shared-task run. This plan writes the bake-off protocol and runs ONE pilot in the weakest validated category (Memory & Context: 2 validated of 47 catalogued — verified 2026-07-03), producing the repo's first run-backed head-to-head.

## Current state

- Existing comparative surface: `evaluations/mem0-vs-claude-mem.md` — Evidence `SOURCE-ONLY` (line 3), quotes vendor benchmark numbers (e.g. "BEAM (1M tokens): 64.1"). `evaluations/mattpocock-vs-agent-skills.md` exists (check its Evidence line before writing — `grep -n "Evidence" evaluations/mattpocock-vs-agent-skills.md`).
- `WORKFLOW.md:415` area: "Overlap groups (compared competitors, picked a winner)" — 5 groups listed (read that section for the exact list before Step 1).
- Weakest validated stages (ADOPT/KEEP per COMPARISON section, verified): Research & Discovery 1/18, Outer Loop 2/40, **Memory & Context 2/47**. Memory & Context's validated pair includes claude-mem (KEEP, installed — it powers this repo's own session memory), making it the natural pilot: the incumbent is already running, so the A/B has a live baseline.
- After plan 009: `evaluations/measurement-protocols.md` defines the Correctness/Speed with-vs-without method and `TEMPLATE.md` has the Test-design block — the bake-off is two tools run under the SAME Test-design.
- Honesty machinery that will judge the output: detector B (fabrication), K (verdict evidence), the `HONEST` disclaimer vocabulary — a bake-off that wasn't really run must say so or CI fails. This is a feature.
- Eval infrastructure: the `eval-runner` agent type exists ("Runs a hands-on, MEASURED evaluation of a single tool or skill … following TEMPLATE.md").

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| Sync | `./sync-plugin-docs.sh` | exit 0 |
| Verdict distribution | `grep -c "| DEFER |\|| ADOPT |" COMPARISON.md` | sanity numbers |

## Scope

**In scope**:
- `evaluations/bakeoff-protocol.md` (create — the method)
- One pilot bake-off eval file `evaluations/<a>-vs-<b>-bakeoff.md` (create)
- `COMPARISON.md`/`CATALOG.md` verdict updates ONLY if the pilot changes a verdict (via the documented propagation: reconcile → backfill → tier-stack → sync — i.e. `make fix`)
- `WORKFLOW.md` overlap-groups section (add the pilot's result with a link)
- `plans/README.md`

**Out of scope**:
- Running bake-offs for all overlap clusters (one pilot proves the method; the rest join NEXT-EVALS)
- Rewriting `mem0-vs-claude-mem.md` (it stays as the honest SOURCE-ONLY record; the new bake-off supersedes it by link, not deletion)
- Any tool installation requiring paid API keys — pick pilot contestants that run free/local (STOP condition otherwise)

## Steps

### Step 1: Write evaluations/bakeoff-protocol.md (~60-90 lines)

The method, generalizing token-savings-protocol's four moves to head-to-head:

1. **Same job**: name the overlap cluster and the single job description both tools claim (from their catalog "Problem it solves" cells).
2. **Same task set**: one fixed, disclosed task set (3-5 tasks, mechanical oracles) per measurement-protocols.md.
3. **Same harness**: same model, same session shape, tool A vs tool B vs *neither* (three arms — the neither arm catches "both are worse than nothing").
4. **Record per signal**: Correctness pass-rates, Speed medians, Cost tokens — the protocols from plan 009; Maintainability/Safety rubric notes.
5. **Resolve**: winner / split-decision ("A for X, B for Y" is a legitimate outcome — record the condition) / neither. The result updates BOTH evals' "Versus alternatives" sections and the WORKFLOW overlap-groups list, with links.
6. **Honesty**: a bake-off you couldn't complete is recorded as such (the code-on-incus precedent — blocked attempts are committed honestly).

**Verify**: file exists; cites measurement-protocols.md; `make check` exit 0.

### Step 2: Select the pilot pair (bounded choice, not open-ended)

Default: **claude-mem (incumbent KEEP) vs the strongest free/local Memory & Context challenger** in the catalog. Selection procedure: list Memory & Context rows (`awk` the COMPARISON section), filter Free == ✓, exclude discovery-log rows with archived/dead repos, pick the highest overlap-pressure challenger (how many rows cite it in "Overlaps with" — `python3 audit-evals.py --overlaps` output). Record the selection rationale in the pilot eval's header. If claude-mem's top challenger requires paid infra, fall back to the Research & Discovery cluster (last30days incumbent) with the same procedure.

**Verify**: the chosen pair + rationale written into the pilot eval file's "What it does" section; both install commands resolve (detector A will check: `python3 audit-evals.py --installs`).

### Step 3: Run the pilot (attended)

Execute the protocol: define 3-5 memory-recall tasks with mechanical oracles (e.g. "after N sessions containing planted fact X, does a fresh session recall X when asked?" — pass/fail), run the three arms, record per-signal results in the bake-off eval using TEMPLATE.md + the Test-design block. Evidence: MEASURED only if the A/B actually ran; otherwise record honestly what blocked it.

**Verify**: the eval file passes `python3 audit-evals.py --fabrication` (honest) and `make check`; its Test-design section names task set, baseline, metric, reproduce command.

### Step 4: Propagate the result

If a verdict changed (e.g. challenger ADOPT, or incumbent's KEEP condition sharpened): update the eval files' Verdict sections, then `make fix` (runs reconcile → backfill-evidence → tier-stack → sync in order), then `make check`. Add the cluster + result + link to WORKFLOW.md's overlap-groups list.

**Verify**: `make check` → exit 0; WORKFLOW.md overlap-groups section includes the pilot with a link to the bake-off eval.

## Test plan

The honesty detectors ARE the test: `--fabrication`, `--installs`, detector D (verdict sync), K (verdict evidence) must all pass on the new files via `make check`.

## Done criteria

- [ ] `evaluations/bakeoff-protocol.md` exists (6 parts)
- [ ] One pilot bake-off eval exists with a filled Test-design block and honest Evidence value
- [ ] WORKFLOW.md overlap-groups lists the pilot result
- [ ] `make check` → exit 0 (incl. detector A on any new install commands)
- [ ] `plans/README.md` updated (or BLOCKED with reason if Step 3 was unattended-infeasible)

## STOP conditions

- Unattended execution reaches Step 3 → mark BLOCKED(pilot needs attended run), commit Steps 1-2 only. Never simulate a run — detector B exists because that temptation is real.
- Both pilot candidate pairs require paid APIs or unavailable infra (the code-on-incus/macOS precedent) → commit the protocol + a blocked-attempt record, BLOCKED.
- The oracle design turns out non-mechanical (recall quality needs human judgment) → simplify to planted-fact binary recall; if even that fails, STOP and report the design problem.

## Maintenance notes

- Each future bake-off is one NEXT-EVALS queue entry (plan 005); the queue's overlap-pressure term naturally surfaces dense clusters.
- The three-arm design (A/B/neither) is the protocol's teeth — reviewers should reject any bake-off that dropped the neither arm without saying why.
- Deferred: a `--bakeoff-coverage` metric (clusters resolved / dense clusters total) once ≥3 bake-offs exist.
