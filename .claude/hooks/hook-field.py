#!/usr/bin/env python3
"""hook-field.py — print tool_input.<field> from the Claude Code hook JSON on stdin.

The ONE JSON-extraction helper both bash hooks use (#202) instead of each
embedding its own inline one-liner. Fail-open by contract: any parse problem
(bad JSON, missing key, no field argument) prints nothing and exits 0, so a
hook's `$(...)` capture is empty and the hook no-ops — never breaks the session.
Pinned by TestHookTriggerSeam in test_automation.py.
"""
import json
import sys

try:
    print(json.load(sys.stdin).get("tool_input", {}).get(sys.argv[1], ""))
except Exception:
    pass
