# Evaluation: openhack

**Repo:** [hadriansecurity/openhack](https://github.com/hadriansecurity/openhack)
**Stars:** 742 | **Last updated:** 2026-06-01 (pushed) | **License:** MIT
**Last verified:** 2026-10-17
**Last triaged:** 2026-10-17  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Hadrian's file-based workspace mimicking how its research team performs automated
vulnerability research — a router agent turns recon into scoped scenarios, independent expert
agents prove or reject each one, and an independent triage agent decides which verified
candidates become final findings. Runs inside Claude Code, Codex, Cursor, or a custom runner;
durable state (recon, scenarios, candidates, triage decisions, findings) lives in plain files,
and the human approves every phase transition.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the repo's
README and license file. That is sufficient to place the lead, not to judge the methodology's
actual finding quality hands-on.

## Verdict

**discovery-log — tentative read** — newly catalogued this pass; not previously examined.

## Triage note

New lead, added today. Not a P2 challenger: no STACK pick does scenario-first, checkpointed
whitebox vulnerability research with a separate proposer/triage split, and the catalog's
existing security-review entries (`cdmx-in/security-review`, `patchbot`) are narrower in scope
(chaining existing scanners, or opening a fix PR from existing findings) rather than a full
agent-driven research methodology. Left at `discovery-log`; a real eval would need to check
whether the scenario/triage split actually reduces false positives in practice.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [openhack](https://github.com/hadriansecurity/openhack) | tool | Hadrian's file-based workspace (MIT) for scenario-first whitebox security review — router, independent expert and triage agents, durable plain-file state | Agent-run vulnerability research lacks a structured, auditable methodology with human approval at each phase | cdmx-in/security-review, patchbot, open-kritt |  |
