# Evaluation: MergeProof

**Repo:** [bukacdan/MergeProof](https://github.com/bukacdan/MergeProof)
**Stars:** 3 | **Last updated:** 2026-09-02 (pushed) | **License:** MIT
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

Agent skill that records a browser demo of a UI change and attaches it to the pull
request via `gh --attach`, so a reviewer can see the change actually work without pulling
the branch.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on
redundancy with a catalogued incumbent, not on the tool's behaviour — a question the overlap
answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`: no structural disposition applies. It cites ship-it/vet/spotpatch
as conceptual neighbors, but none of those are STACK picks and none produce an attached
browser-demo artifact specifically — ship-it catches UX details before shipping, vet verifies
correctness/intent, spotpatch traces React source. MergeProof's narrow job (proof-of-behavior
attached to the PR itself) is a real, small, distinct niche. Very early (3★) — worth a look if
PR review artifacts become a priority.

_Triaged 2026-09-09 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [MergeProof](https://github.com/bukacdan/MergeProof) | skill | Agent skill (MIT) that records a browser demo of a change and attaches it to the pull request via `gh --attach` | Reviewers can't see a UI change actually work without pulling the branch; want behavioral proof attached to the PR itself | ship-it, vet, spotpatch |
