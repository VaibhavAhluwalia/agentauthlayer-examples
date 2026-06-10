"""
Step 6: Understand create-or-update sync.

This file explains the expected behavior of smart sync when code-defined
state already exists in the control plane.
"""

from __future__ import annotations

print("Step 6, understand create-or-update sync")
print(
    {
        "first_sync": "Create missing tools and agents.",
        "second_sync": "Skip unchanged tools and agents instead of recreating them.",
        "after_code_change": "Update only the fields or tool definitions that changed.",
        "try_this": [
            "Run: agentauth sync --module examples.getting_started.03_sync_agent --project agent-examples",
            "Run the same command again to observe the unchanged path.",
            "Change a role, scope, or description, then sync again to observe an update-only path.",
        ],
    }
)
