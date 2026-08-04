# Evaluation: babysitter

**Repo:** [a5c-ai/babysitter](https://github.com/a5c-ai/babysitter)
**Stars:** 1,643 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (workflow discipline)
**Layer:** Process

---

## What it does

A harness that enforces agent obedience — self-orchestration for complex workflows, pitched as
deterministic and hallucination-free.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`orchestkit`, `ECC`, `superpowers`). Sufficient for
a SKIP that turns on *redundancy with a catalogued incumbent*; not sufficient for a positive
verdict, and none is offered.

## Verdict

**SKIP** — redundant with [`superpowers`/GSD](https://github.com/obra/superpowers) (STACK,
`MEASURED`). Keeping an agent on a declared plan instead of improvising is the discipline the
incumbent enforces through milestones, phases and discovery discussion, and methodology layers do
not compose — two of them contending for the same turn is worse than either alone. This pass
disposed `claude-code-harness`, `Aegis`, `KARIMO`, `aidlc-workflows` and `vibecode-pro-max-kit`
against the same incumbent for the same structural reason.

The framing is the second half of the call. "Hallucination-free" is not a property a workflow layer
can confer — the model still generates every token, and an orchestrator can constrain *what runs*,
never *what is believed*. A claim that strong on the tin, with no measurement behind it, is a
reason for more scepticism about the rest, not less.

★1.6K against the incumbent's ★251K, and MIT with pushes today — a live project, just not one that
displaces a measured incumbent on a description.

Re-open if it publishes a with/without measurement of plan adherence, which is the claim that would
actually distinguish it.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [babysitter](https://github.com/a5c-ai/babysitter) | harness | Enforces agent obedience — deterministic, hallucination-free self-orchestration for complex workflows | Agents drift off the declared plan on long multi-step work | orchestkit, ECC, superpowers |
