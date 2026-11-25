# Evaluation: agora-mesh

**Repo:** [kn0sti/agora-mesh](https://github.com/kn0sti/agora-mesh)
**Stars:** 50 | **Last updated:** 2026-11-21 (pushed) | **License:** MIT
**Last verified:** 2026-11-25
**Last triaged:** 2026-11-25  <!-- triaged: bulk -->
**Dev loop stage:** Implement (multi-machine agent coordination)
**Layer:** Infrastructure

---

## What it does

Connects coding agents across a user's own machines (MIT) so they plan together,
split work, and push to separate git branches. Described by its author as an
independent community project.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this
eval offers none.

## Triage note

Newly discovered and catalogued today via the daily discovery pass. Overlaps with
`fleetpost`, `geckobox`, and `myco` (all "coordinate coding agents across your own
machines" tools), but none of those is a STACK pick, so this does not band P2 and
there is no redundancy claim to make. Left at `discovery-log` for a real hands-on
eval — specifically, how it differs from the existing cross-machine coordination
tools already catalogued — rather than a first-day guess.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agora-mesh](https://github.com/kn0sti/agora-mesh) | tool | Connects coding agents across your own machines (MIT) so they plan together, split work, and push to separate branches | Coordinating coding agents across several machines means manual SSH/relay setup with no shared planning layer | fleetpost, geckobox, myco |
