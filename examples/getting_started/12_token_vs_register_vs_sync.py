"""
Step 12: Understand token vs register vs sync.

This file explains three different responsibilities that are easy to confuse:
- token authentication
- local registration in code
- sync to the control plane
"""

from __future__ import annotations

print("Step 12, understand token vs register vs sync")
print(
    {
        "token": "Authenticates SDK and CLI calls to the control plane.",
        "register_tool": "Declares tool metadata locally in code so sync can discover it later.",
        "register_agent": "Declares agent metadata locally in code so sync can discover it later.",
        "sync": "Creates missing state, updates changed state, and skips unchanged state in the control plane.",
        "policy": "Decides whether an authenticated caller is allowed to perform a specific action.",
    }
)
