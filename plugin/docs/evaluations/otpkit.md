# Evaluation: otpkit

**Repo:** [SecFathy/otpkit](https://github.com/SecFathy/otpkit)
**Stars:** 72 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-21
**Last triaged:** 2026-11-21  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

An MCP server that receives temporary email and SMS — OTPs, verification links,
confirmation codes — with no API keys required, so a coding agent testing a
signup/verification flow can read the real code instead of a human relaying it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata. Sufficient to place the lead, not to
confirm delivery reliability or provider coverage.

## Triage note

Banded P2 (challenges `playwright`), but that's an artifact of listing `playwright`
as a same-flavor testing-infra peer in the CATALOG "Overlaps with" cell, not a real
capability overlap: `playwright` automates the browser, otpkit supplies the OTP/SMS
a flow needs to get past — complementary, not redundant. Left at discovery-log.

_Triaged 2026-11-21 by the P2 challenger band._
