#!/usr/bin/env python3
"""hook-field.py — print tool_input.<field> from the Claude Code hook JSON on stdin.

The ONE JSON-extraction helper both bash hooks use (#202) instead of each
embedding its own inline one-liner. Fail-open by contract: any parse problem
(bad JSON, missing key, no field argument) prints nothing and exits 0, so a
hook's `$(...)` capture is empty and the hook no-ops — never breaks the session.
Pinned by TestHookTriggerSeam in test_automation.py.
"""
import contextlib
import json
import sys

# A hook must never fail the tool call it observes: a malformed payload, a missing
# field, or a closed stdin all mean 'nothing to print', not 'abort'.
with contextlib.suppress(Exception):
    print(json.load(sys.stdin).get("tool_input", {}).get(sys.argv[1], ""))
