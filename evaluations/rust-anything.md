# Evaluation: rust-anything

**Repo:** [erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything)
**Stars:** 240 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-17
**Last triaged:** 2026-11-17  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Rewrites a whole app into Rust one piece at a time — CLIs, HTTP servers, and libraries
starting from TypeScript, Python, C, Go, Ruby, or Java — checking each piece against the
original's recorded behavior before moving to the next.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual
behavior — it would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read**

A piece-by-piece, behavior-checked language port is a different job from any cataloged
incumbent; worth a real hands-on eval once this lane escalates it.

## Triage note

Banded P2, challenging `stryker-js` (STACK, RUN) purely because both cite
behavior-preservation during a code change in their "Overlaps with" cell. The actual jobs
differ: `stryker-js` is mutation testing — it scores whether an *existing* test suite
would catch an *introduced* bug. `rust-anything` is a whole-application language port,
verifying that *each rewritten piece* reproduces the *original's* recorded behavior before
advancing. Neither displaces the other's install case. Not SKIPped as redundant; left at
`discovery-log` for a real hands-on eval of the behavior-recording/verification mechanism
itself (what counts as "recorded behavior", how it's compared, false-negative rate on a
real migration).

_Triaged 2026-11-17 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rust-anything](https://github.com/erkamyaman/rust-anything) | tool | Rewrites a whole app into Rust one piece at a time (MIT), checked against the original's recorded behavior at every step | Manual language ports drift from the original's behavior with no step-by-step correctness check against it | openrewrite, ts-morph, stryker-js |
