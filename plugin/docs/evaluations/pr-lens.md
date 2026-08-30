# Evaluation: pr-lens

**Repo:** [coldteadotai/pr-lens](https://github.com/coldteadotai/pr-lens)
**Stars:** 32 | **Last updated:** 2026-08-29 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Draws every PR as animated architecture and data-flow diagrams, rendered inside the pull request itself. Ships as a GitHub App, GitHub Action, CLI, or a skill for a coding agent.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`spotpatch`, `code-review`, `herdr-hunk-diff`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` (P2 challenger: cites `code-review` in "Overlaps with"). Not SKIPped as redundant — `code-review` is a multi-agent review/scoring plugin, while pr-lens is a diagram-generation tool for visualizing a diff's architectural/data-flow impact; the two are complementary review inputs rather than competing on the same job. Whether the diagrams are accurate/useful enough to earn a seat needs a real look.

_Triaged 2026-08-30 by the P2 challenger band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pr-lens](https://github.com/coldteadotai/pr-lens) | tool | Draws every PR as animated architecture and data-flow diagrams inside the PR itself (MIT) | Reviewers can't see a diff's architectural or data-flow impact without tracing it by hand | spotpatch, code-review, herdr-hunk-diff |
