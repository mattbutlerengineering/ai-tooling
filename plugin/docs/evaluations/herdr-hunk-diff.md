# Evaluation: herdr-hunk-diff

**Repo:** [jhochenbaum/herdr-hunk-diff](https://github.com/jhochenbaum/herdr-hunk-diff)
**Stars:** 72 | **Last updated:** 2026-08-14 (pushed) | **License:** MIT
**Last verified:** 2026-08-18
**Last triaged:** 2026-08-18  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A companion plugin for `herdr` (the terminal agent multiplexer) that reviews
agent-authored changes hunk-by-hunk from inside herdr and sends inline comments back to
the responsible agent, mid-session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. It would not support an ADOPT, and this
eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped. It cites `code-review`/`pr-review-toolkit`
(both in STACK) in Overlaps, but the actual job is a live, mid-session hunk-review loop
tied to `herdr` sessions — routing comments back to the agent that wrote the diff, not a
post-hoc PR review. `herdr` itself is not yet in STACK, so this component's fate is tied
to whether `herdr` gets adopted; not a mechanical redundancy call today.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [herdr-hunk-diff](https://github.com/jhochenbaum/herdr-hunk-diff) | plugin | Reviews agent-authored diffs hunk-by-hunk inside herdr and sends inline comments back to the responsible agent (MIT) | herdr shows agent terminals but has no structured way to review and comment on the diffs those agents produce | herdr, code-review, pr-review-toolkit |
