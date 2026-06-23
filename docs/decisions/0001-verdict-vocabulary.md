# ADR 0001 — Verdict vocabulary: collapse the CONDITIONAL bucket

- **Status:** Accepted (2026-06-22) · **Implemented** in #69 (2026-06-22)
- **Issue:** #63 (decision) · implemented by #69
- **Deciders:** repo owner

> **Implementation note (#69):** the bucket collapse is done. 404 unexercised
> CONDITIONAL rows (`Evidence` REVIEW/SOURCE-ONLY) were demoted to **discovery-log**;
> only the 12 exercised (MEASURED/RUN) CONDITIONALs remain. `audit-evals.py`
> recognizes `discovery-log` and excludes it from verdict-sync (D) / verdict-evidence
> (K); detector **M (`--clusters`)** surfaces overlap clusters still awaiting an ADOPT
> pick. Remaining/optional follow-ups: per-cluster best-in-class ADOPT picks (point 2)
> and `adopt-if:` condition strings on the 12 surviving CONDITIONALs (point 1).

## Context

`COMPARISON.md` records a verdict per catalogued tool. The current distribution is badly skewed:

| Verdict | Count | Share |
|---------|------:|------:|
| CONDITIONAL | 418 | 83% |
| SKIP | 51 | 10% |
| ADOPT | 24 | 5% |
| KEEP | 9 | 2% |

With 83% of tools in one bucket, the verdict carries almost no discriminating signal. Two distinct problems hide inside CONDITIONAL:

1. **Reflexive hedging on unexercised tools.** Most CONDITIONAL rows are README-skim, source-only entries (`Evidence: SOURCE-ONLY`/`REVIEW`) that were never run. CONDITIONAL there means "we didn't really look," which the separate `Evidence` field (`MEASURED`/`RUN`/`REVIEW`/`SOURCE-ONLY`, #67) already captures. The verdict is doing duplicate duty.
2. **No recommendation among overlapping tools.** When several catalogued tools solve the same problem (an "Overlaps with" cluster), blanket-CONDITIONAL means we never say *which one to use* — even when there is clearly a best-in-class pick. The catalog's job is to recommend, not to hedge on everything.

## Decision

Adopt a **hybrid** vocabulary that (a) requires a machine-readable condition to stay CONDITIONAL, (b) forces a best-in-class pick within each overlap cluster, and (c) demotes the unexercised long tail out of the verdict space entirely.

### 1. CONDITIONAL must carry a machine-readable condition
A row may only remain `CONDITIONAL` if it declares an `adopt-if:` condition string describing the real gate, e.g.:

- `adopt-if: linux-host` (tool is Linux-only)
- `adopt-if: you-lack-X` (only worth it if you don't already run X)
- `adopt-if: self-hosting` (license/ops gate)

No genuine condition ⇒ it is **not** a CONDITIONAL. The condition is a single parseable token + free-text gloss.

### 2. Recommend one tool over its alternatives (the key fix)
Within each overlap cluster (tools sharing a "Problem it solves"), designate **exactly one** best-in-class `ADOPT` — the pick — and resolve the also-rans to `SKIP` (or `KEEP` if already installed) with a one-line "why not the pick" reason. A cluster that is all-CONDITIONAL with no pick is a smell, not a neutral state.

"Best-in-class" is judged on: evidence strength (a MEASURED winner beats a source-only rival), fit to our five quality signals, maintenance/adoption, and **license** (non-permissive tools cannot be the pick — see ADR-adjacent governance below).

### 3. Demote the unexercised long tail to `discovery-log`
Source-only rows that were never exercised and have no real `adopt-if:` condition are **leads, not verdicts**. Reclassify them to an explicit **`discovery-log`** status (backed by `Evidence: SOURCE-ONLY`). A real verdict (ADOPT/KEEP/SKIP/CONDITIONAL) now requires *either* the tool to have been exercised *or* a genuine `adopt-if:` condition.

### Governance interaction (licenses)
Per the standing governance rule (issues #26/#36), only **permissive OSS (MIT or similar)** is adoptable. License-disqualified tools (GPL/AGPL/BSL/no-license) go straight to `SKIP` with a `license: <spdx> (non-permissive)` note, regardless of cluster position — they can never be the pick.

## Migration (the 418 rows → spec for #69)

Partition every current `CONDITIONAL` row into exactly one of:

- **(a) Genuine env/license gate** → keep `CONDITIONAL`, add `adopt-if:` token.
- **(b) Overlap-cluster member with a basis to choose** → `ADOPT` the pick / `SKIP` the rest (with reason).
- **(c) Source-only, never run, no real condition** → demote to `discovery-log`.
- **(d) License-disqualified** → `SKIP` with `license:` note.

## Consequences for `audit-evals.py`

- **New detector:** every `CONDITIONAL` row must have a parseable `adopt-if:` condition; fail otherwise.
- **New (warn-level) detector:** flag overlap clusters that are entirely CONDITIONAL/discovery-log with no ADOPT pick.
- **Detector K (verdict evidence):** `discovery-log` rows are excluded — they are explicitly not recommendations, so they need no run-backing or disclaimer.
- **Detectors D/G** continue to require eval ↔ COMPARISON ↔ CATALOG agreement under the new vocabulary.
- Characterization tests (`test_automation.py`) updated for the new tokens.

## Alternatives considered

- **Pure discovery-log demotion (no condition strings):** simpler, but loses the genuine "adopt only if Linux/self-hosting" nuance that some real CONDITIONALs carry.
- **Sub-states without demotion:** splits CONDITIONAL into named sub-states but leaves the 83% bulk in verdict space, so the signal stays diluted.
- The hybrid was chosen because it reuses machinery that already exists (the `Evidence` field) and directly fixes the "we never recommend one tool over another" failure mode.
